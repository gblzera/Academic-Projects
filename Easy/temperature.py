unit = input("Is this temperature in Celsius or Fahrenheit? (C/F): ")
temp = float(input("Enter the temperature: "))

if unit == "C":
    # Convert Celsius to Fahrenheit
    converted_temp = (temp * 9/5) + 32
    unit = "Fahrenheit"
    print(f"{temp} Celsius is {converted_temp} Fahrenheit.")
elif unit == "F":
    # Convert Fahrenheit to Celsius
    converted_temp = (temp - 32) * 5/9
    unit = "Celsius"
    print(f"{temp} Fahrenheit is {converted_temp} Celsius.")
else:
    print("Invalid unit. Please enter 'C' for Celsius or 'F' for Fahrenheit.")
    exit()
