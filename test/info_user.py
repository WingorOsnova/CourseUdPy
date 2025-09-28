def process_info(info, users_id, callback):
    info_copy = info.copy()
    callback(info_copy, users_id)
    return info_copy


def sent_info(info_copy, user_id):
    print("📤 Sent info from user to server...")
    info_copy['id'] = len(user_id) + 1
    user_id.add(info_copy['id'])
    print("✅ Info saved:", info_copy)


def print_info(info_user, user_id):
    print("📝 User entered:")
    for key, value in info_user.items():
        print(f"{key}: {value}")


users = {1, 2, 3, 4, 5, 6}

while True:
    print("""
    1. Enter new user
    2. Quit
    """)
    try:
        action = int(input("Enter an action: "))
    except ValueError:
        print("Enter a number!")
        continue
    if action == 2:
        print("Bye!")
        break
    if action == 1:
        name = input("Enter a name: ")
        surname = input("Enter a surname: ")
        age = int(input("Enter an age: "))
        info = dict(
            name=name,
            surname=surname,
            age=age
        )
        process_info(info=info, users_id=users, callback=print_info)
        process_info(info=info, users_id=users, callback=sent_info)
    else:
        print("Invalid action")
    print(f"Current users ID: {users}")
