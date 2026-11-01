"""
WRITE A PYTHON PRAOGRAM TO CHECK WETHER A PHONE NUMBER CONTAINS 10 DIGITS.
IF VALID MASK THE FIRST SIX DIGITS AND DISPLAY THE LAST FOUR DIGITS. IF INVALID, DISPLAY AN INAPPROPRIATE  ERROR MESSAGE
"""

phone =  input("Enter Phone Number: ")
count = len(phone)

if count == 10:
    ph = "XXXXXX" + phone[-4:]
    print(f"The Phone Number is valid.\nNum: {ph}")
else:
    print("The number is invalid.")
