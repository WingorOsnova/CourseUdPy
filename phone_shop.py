# PHONE SHOP
from tabulate import tabulate

model_phone_set = set()
quantity_phone = []
model_phone_quantity = {"Iphone 14 pro max": 2,
                        "Samsung Ultra 22": 1, 'Motorola G22': 3}
model_phone_price = {"Iphone 14 pro max": 800, "Samsung Ultra 22": 1000}

while True:
    print("---------------------")
    print("1. Add device")
    print("2. List devices")
    print("3. Add price for device")
    print("4. All info about device")
    print("0. Quit")
    print("--------------------- \n")

    try:
        select_action = int(input("Select action: "))
    except ValueError:
        print("Enter a number!")
    if select_action == 0:
        break
    elif select_action == 1:
        while True:
            print(
                "\nYou're selected the action 1\nIf you want Back to menu, enter 'q or Q'\n")
            model_phone = input("Enter a model name of phone: ")
            if model_phone == "q".lower():
                break
            else:
                pass
            try:
                quantity_input = int(input("Enter a quantity: "))
            except ValueError:
                print("Enter a number!")
                continue
            model_phone_set.add(model_phone)
            quantity_phone.append(quantity_input)
            model_phone_quantity = dict(zip(model_phone_set, quantity_phone))
    elif select_action == 2:
        print("You're selected the action 2\n")
        for model, quantity in model_phone_quantity.items():
            print(f"MODEL: {model}")
            print(f"QUANTITY: {quantity}\n")
    elif select_action == 3:
        print("You're selected the action 3\n")
        for model1 in model_phone_quantity.keys():
            print(f"MODEL: {model1}")
        set_price = input("Enter a model name of phone: ")
        if set_price in model_phone_quantity.keys():
            try:
                price_input = int(input("Enter a price: $"))
            except ValueError:
                print("Enter a number!")
                continue
            model_phone_price[set_price] = price_input

    elif select_action == 4:
        print("You're selected the action 4\n")
        table = []
        for model, quantity in model_phone_quantity.items():
            # берём цену, если нет — пишем "Not set"
            price = model_phone_price.get(model, "Not set")
            table.append([model, quantity, price])
        print(tabulate(table, headers=[
              "Model", "Quantity", "Price"], tablefmt="simple_grid"))
    else:
        print("Invalid action")
