class InventoryItem:
    """ A class to demostrate operator overloading for inventory management. """
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
    
    def __repr__(self):
        return f"InventoryItem(name='{self.name}', quantity={self.quantity})"
    
    # Arithmetic operators
    def __add__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            return InventoryItem(self.name, self.quantity + other.quantity)
        raise ValueError("Cannot add items with different types.")
    
    def __sub__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            if self.quantity >= other.quantity:
                return InventoryItem(self.name, self.quantity - other.quantity)
            raise ValueError("Not enough items to subtract.")
        raise ValueError("Cannot subtract items with different types.")
    
    def __mul__(self, other):
        if isinstance(other, int):
            return InventoryItem(self.name, self.quantity * other)
        raise ValueError("Cannot multiply by non-integer value.")
    
    def __truediv__(self, other):
        if isinstance(other, int):
            return InventoryItem(self.name, self.quantity // other)
        raise ValueError("Cannot divide by non-integer value.")
    
    
    # Comparison operators
    def __eq__(self, other):
        if isinstance(other, InventoryItem):
            return self.name == other.name and self.quantity == other.quantity
        return False
    
    def __lt__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            return self.quantity < other.quantity
        raise ValueError("Cannot compare items with different types.")
    
    def __gt__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            return self.quantity > other.quantity
        raise ValueError("Cannot compare items with different types.")