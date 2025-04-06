weight = float(input("Enter weight: "))
unit = input("Kilograms or Pounds? (K or L): ")

if unit == "K":
    weight = weight * 2.205
    unit = "Lbs."
    print(f"Weight: {weight:.2f} {unit}")
elif unit == "L":
    weight = weight / 2.205
    unit = "Kgs."
    print(f"Weight: {weight:.2f} {unit}")
else:
    print(f"Invalid unit: {unit}")