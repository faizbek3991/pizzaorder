total = 0
while True:
    size = input("Enter the size of the pizza (S, M, or L): ")
    if size == "S":
        total = total + 15
        print("You ordered a small sized pizza. That would cost $15.")
        break
    elif size == "M":
        total = total + 20
        print("You ordered a medium sized pizza. That would cost $20.")
        break
    elif size == "L":
        total = total + 25
        print("You ordered a large sized pizza. That would cost $25.")
        break
    else:
        print("Invalid size. Please enter S, M, or L.")
 
while True:
    pepperoni = input("Do you want pepperoni on your pizza (Y or N): ")
    if pepperoni == "Y":
        if size == "S":
            total = total + 2
            print("That would be an additional $2.")
            break
        if size == "M" or size == "L":
            total = total + 3
            print("That would be an additional $3.")
            break
    elif pepperoni == "N":
        print("There will be no pepperoni on your pizza.")
        break
    else:
        print("Invalid input. Please enter Y or N.")
 
while True:
    extraCheese = input("Do you want extra cheese (Y or N): ")
    if extraCheese == "Y":
        total = total + 1
        print("That would be an additional $1.")
        break
    elif extraCheese == "N":
        print("There will be no extra cheese on your pizza.")
        break
 
print(f"Your total is: {total}")