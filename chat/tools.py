from .models import Item
from decimal import Decimal


def check_stock(name):
    """Look up how many of an item we have."""
    item = Item.objects.filter(name__iexact=name).first()
    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}
    return {"name": item.name, "quantity": item.quantity,"price": float(item.price),}


def list_items():
    """Return every item in the inventory."""
    items = Item.objects.all()
    return {"items": [{"name": i.name, "quantity": i.quantity} for i in items]}


def add_item(name, quantity):
    """Create a new item, or add to an existing one's stock."""
    item = Item.objects.filter(name__iexact=name).first()
    if item is not None:
        item.quantity += quantity
        item.save()
        return {"name": item.name, "quantity": item.quantity, "created": False}
    item = Item.objects.create(name=name, quantity=quantity)
    return {"name": item.name, "quantity": item.quantity, "created": True}


def remove_stock(name, quantity):
    """Take a quantity out of stock."""
    item = Item.objects.filter(name__iexact=name).first()
    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}
    if quantity > item.quantity:
        return {
            "error": f"Cannot remove {quantity}. Only {item.quantity} in stock.",
            "name": item.name,
            "quantity": item.quantity,
        }
    item.quantity -= quantity
    item.save()
    return {"name": item.name, "quantity": item.quantity}


def delete_item(name):
    """Remove an item from the inventory entirely."""
    item = Item.objects.filter(name__iexact=name).first()
    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}
    item.delete()
    return {"deleted": name}

def update_price(name, percentage):
    """Increase or decrease an item's price by a percentage."""
    item = Item.objects.filter(name__iexact=name).first()

    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}

    old_price = item.price

    multiplier = Decimal("1") + Decimal(str(percentage)) / Decimal("100")
    new_price = old_price * multiplier

    if new_price < 0:
        return {"error": "The price cannot become negative."}

    item.price = new_price
    item.save()

    return {
        "name": item.name,
        "old_price": float(old_price),
        "new_price": float(item.price),
        "percentage_change": percentage,
    }

TOOL_DECLARATIONS = [
    {
        "type": "function",
        "name": "check_stock",
        "description": "Look up the current quantity and price of a single item in the inventory. Use this whenever the user asks about an item's stock, quantity, price, or cost.",        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item, e.g. 'Hammer'.",
                },
            },
            "required": ["name"],
        },
    },
    {
        "type": "function",
        "name": "list_items",
        "description": "Return every item in the inventory with its quantity. Use this when the user asks what is in stock generally, or asks for a list, rather than about one specific item.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "add_item",
        "description": "Add stock to the inventory. If the item does not exist it is created; if it already exists the quantity is added to the existing total. Use this for restocking and for new deliveries.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item, e.g. 'Hammer'.",
                },
                "quantity": {
                    "type": "integer",
                    "description": "How many units to add. Must be positive.",
                },
            },
            "required": ["name", "quantity"],
        },
    },
    {
        "type": "function",
        "name": "remove_stock",
        "description": "Reduce the quantity of an existing item. Use this when items are sold, shipped or used. This does NOT delete the item; it only lowers the number.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item, e.g. 'Hammer'.",
                },
                "quantity": {
                    "type": "integer",
                    "description": "How many units to remove. Must be positive.",
                },
            },
            "required": ["name", "quantity"],
        },
    },
    {
        "type": "function",
        "name": "delete_item",
        "description": "Permanently remove an item and its record from the inventory entirely. This is destructive. Only use it when the user clearly wants the item gone, not when they want to reduce its quantity.",
        "parameters": {
            "type": "object",
            "properties": {

                "name": {
                    "type": "string",
                    "description": "The name of the item to delete.",
                },
            },
            "required": ["name"],
        },
    },
    {
    "type": "function",
    "name": "update_price",
    "description": "Increase or decrease the price of an existing inventory item by a percentage. Use this when the user asks to raise, lower, increase, decrease, or change an item's price by a percentage.",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The name of the item, e.g. 'Chocolate Bar'.",
            },
            "percentage": {
                "type": "number",
                "description": "The percentage change. Use a positive value to increase the price and a negative value to decrease it. For example, 50 means increase by 50%, and -20 means decrease by 20%.",
            },
        },
        "required": ["name", "percentage"],
    },
},
]

TOOL_FUNCTIONS = {
    "check_stock": check_stock,
    "list_items": list_items,
    "add_item": add_item,
    "remove_stock": remove_stock,
    "delete_item": delete_item,
    "update_price": update_price,
}
