import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_ITERS


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    user_prompt = " ".join(args)
    
    if verbose:
        print(f"User prompt: {user_prompt}\n")
        
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    
    iters = 0
    while True:
        iters += 1 
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)
            
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(client, messages, verbose=False):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )

    if verbose and hasattr(response, "usage_metadata"):
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # Final response text from the model (if it gives one)
    final_text = None

    for candidate in response.candidates:
        if verbose:
            print(f"Candidate role: {candidate.content.role}")

        # Add the model's content to our running conversation
        messages.append(candidate.content)

        for part in candidate.content.parts:
            # ✅ Safely handle text
            text_value = getattr(part, "text", None)
            if isinstance(text_value, str):
                stripped = text_value.strip()
                if stripped:
                    final_text = stripped

            # ✅ Handle function calls
            func_call = getattr(part, "function_call", None)
            if func_call is not None:
                if verbose:
                    print(f"Function call requested: {func_call.name}({func_call.args})")

                func_response = call_function(func_call, verbose)

                if not (func_response.parts and func_response.parts[0].function_response):
                    raise Exception("Function call returned no valid response.")

                if verbose:
                    print(f"-> {func_response.parts[0].function_response.response}")

                # Append the tool output back to conversation
                messages.append(func_response)

    return final_text


if __name__ == "__main__":
    main()
