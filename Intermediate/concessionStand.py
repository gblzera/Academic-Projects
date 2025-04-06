menu = {"popcorn": 5.00, 
        "soda": 3.00, 
        "candy": 2.50, 
        "nachos": 4.00,
        "hotdog": 3.50,
        "pretzel": 2.00,
        "icecream": 4.50,
        "water": 1.50,
        "chips": 2.50,
        "cookies": 3.00,
        "brownies": 2.50,
        "pizza": 8.00,
        "burger": 7.00}

cart = []
total = 0

print("------- MENU -------")

for key, value in menu.items():
    print(f"{key:10}: ${value:.2f}")

print("--------------------")

while True:
    item = input("Enter the item you want to buy (or 'done' to finish): ").lower()
    
    if item.lower() == "done":
        break
    elif item in menu:
        cart.append(item)
        total += menu[item]
        print(f"Added {item} to your cart. Current total: ${total:.2f}")
    else:
        print("Item not found in the menu. Please try again.")