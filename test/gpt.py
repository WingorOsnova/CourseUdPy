devices = {}

while True:
    print("""
    1. Add device
    2. List devices
    3. Add price
    4. Show all info
    0. Quit
    """)

    try:
        action = int(input("Select action: "))
    except ValueError:
        print("Enter a number!")
        continue

    if action == 0:
        break
    elif action == 1:
        model = input("Enter model (q to cancel): ")
        if model.lower() == 'q':
            continue
        qty = input("Enter quantity: ")
        if not qty.isdigit():
            print("Enter a number!")
            continue
        devices[model] = {"quantity": int(
            qty), "price": devices.get(model, {}).get("price")}
    elif action == 2:
        print(devices)
    elif action == 3:
        print("Available models:", list(devices))
        model = input("Enter model: ")
        if model in devices:
            price = input("Enter price: ")
            if price.isdigit():
                devices[model]["price"] = int(price)
    elif action == 4:
        for model, data in devices.items():
            print(
                f"MODEL: {model}, QUANTITY: {data['quantity']}, PRICE: {data.get('price', 'N/A')}")
    else:
        print("Invalid action")
