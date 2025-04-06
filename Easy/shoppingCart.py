foods = []
prices = []

print("🛒 Welcome to Python Market!\n")

while True:
    food = input("Enter a food to buy (q to quit): ")
    if food.lower() == "q":
        break
    try:
        price = float(input(f"Enter the price of {food}: $ "))
        foods.append(food)
        prices.append(price)
    except ValueError:
        print("⚠️ Invalid price! Please enter a numeric value.")

print("\n------- YOUR RECEIPT -------")
print("{:<20} {:>10}".format("Item", "Price"))

print("-" * 32)

for food, price in zip(foods, prices):
    print("{:<20} ${:>8.2f}".format(food, price))

total = sum(prices)

print("-" * 32)
print("{:<20} ${:>8.2f}".format("TOTAL", total))
print("\n🧾 Thank you for shopping with us!\n🕶️ Come back anytime!")
