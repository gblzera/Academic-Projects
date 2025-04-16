# Python credit card validator program

# 1. Remove any '-' or ' '
# 2. Add all digits in odd positions (from the right to left)
# 3. Double every second digit from right to left.
#          (If result is a two-digit number,
#           add the two-digit number together to get a single digit.)
# 4. Sum all totals of steps 2 & 3.
# 5. If sum is divisible by 10, the credit card # is valid.

sum_odd_digits = 0
sim_even_digits = 0
total = 0

# Step 1
card_number = input("Enter a credit card number: ").replace("-", "").replace(" ", "")
card_number = card_number[::-1]  # Reverse the string

# Step 2
for x in card_number[::2]:
    sum_odd_digits += int(x) #has to be a int because x is a string

# Step 3
for x in card_number[1::2]:
    double = int(x) * 2
    if double > 9:
        double = double - 9
    sim_even_digits += double

# Step 4
total = sum_odd_digits + sim_even_digits
print("Sum of odd digits: ", sum_odd_digits)
print("Sum of even digits: ", sim_even_digits)
print("Total: ", total)

# Step 5
if total % 10 == 0:
    print("The credit card number is valid.")
else:
    print("The credit card number is invalid.")
    

