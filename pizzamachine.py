def take_order():
    print("\n" + "="*45)
    print("      🍕 WELCOME TO PIZZA MACHINE 🍕      ")
    print("="*45)

    # 1. Size selection with validation
    while True:
        size = input("\nWhat size pizza do you want? (S, M, or L): ").strip().upper()
        if size in ["S", "M", "L"]:
            break
        print("⚠️ Invalid size! Please choose S, M, or L.")

    # 2. Pepperoni selection with validation
    while True:
        pepperoni = input("Do you want pepperoni? (Y or N): ").strip().upper()
        if pepperoni in ["Y", "N"]:
            break
        print("⚠️ Invalid input! Please enter Y or N.")

    # 3. Extra cheese selection with validation
    while True:
        extra_cheese = input("Do you want extra cheese? (Y or N): ").strip().upper()
        if extra_cheese in ["Y", "N"]:
            break
        print("⚠️ Invalid input! Please enter Y or N.")

    # 4. Drink selection with validation
    print("\n🥤 Drink Options:")
    print("  1. Pepsi ($3)")
    print("  2. Iced Tea ($3)")
    print("  3. No Drink ($0)")
    
    while True:
        drink_choice = input("Select a drink (1, 2, or 3): ").strip()
        if drink_choice in ["1", "2", "3"]:
            break
        print("⚠️ Invalid choice! Please enter 1, 2, or 3.")

    # Calculate Bill
    bill = 0
    size_name = ""
    
    if size == "S":
        bill += 15
        size_name = "Small Pizza"
    elif size == "M":
        bill += 20
        size_name = "Medium Pizza"
    elif size == "L":
        bill += 25
        size_name = "Large Pizza"

    # Add Pepperoni
    pep_cost = 0
    if pepperoni == "Y":
        pep_cost = 2 if size == "S" else 3
        bill += pep_cost

    # Add Cheese
    cheese_cost = 0
    if extra_cheese == "Y":
        cheese_cost = 1
        bill += cheese_cost

    # Add Drink
    drink_name = "No Drink"
    drink_cost = 0
    if drink_choice == "1":
        drink_name = "Pepsi"
        drink_cost = 3
    elif drink_choice == "2":
        drink_name = "Iced Tea"
        drink_cost = 3

    bill += drink_cost

    # Print Receipt / Bill
    print("\n" + "-"*45)
    print("               🧾 ORDER RECEIPT              ")
    print("-"*45)
    print(f" Item: {size_name:<22} ${bill - pep_cost - cheese_cost - drink_cost:>5}")
    if pepperoni == "Y":
        print(f" Pepperoni Topping:{'':<11} ${pep_cost:>5}")
    if extra_cheese == "Y":
        print(f" Extra Cheese:{'':<16} ${cheese_cost:>5}")
    if drink_cost > 0:
        print(f" Drink: {drink_name:<19} ${drink_cost:>5}")
    print("-"*45)
    print(f" TOTAL BILL:{'':<18} ${bill:>5}")
    print("="*45)
    print("   Thank you for your order! Enjoy your meal! 🍕🥤\n")


def main():
    while True:
        take_order()
        
        # Ask if another customer wants to order
        next_customer = input("Is there another customer waiting to order? (Y/N): ").strip().upper()
        if next_customer != "Y":
            print("\n" + "="*45)
            print("  🔒 Pizza Machine closed. Have a great day!")
            print("="*45)
            break


if __name__ == "__main__":
    main()
    main()