import json


def printer(name):
    print(name)


class Forum():
    db_users = {}

    def dump_user(self):
        with open("f_user.json", 'w', encoding='utf-8') as f:
            json.dump(self.db_users, f, indent=2, ensure_ascii=False)

    def load_users(self):
        with open("f_user.json", 'r', encoding='utf-8') as f:
            self.db_users = json.load(f)

    def register_user(self, name, surname, password, email, username):
        for user in self.db_users.values():
            if user["email"] == email:
                print("This email is already registered")
                return
        user = User(name, surname, password, email, username)
        user_id = len(self.db_users) + 1
        user.role = "user"
        self.db_users[user_id] = {
            "name": user.name,
            "surname": user.surname,
            "password": user.password,
            "email": user.email,
            "username": user.username,
            "role": user.role
        }
        if user.username in self.db_users.values():
            print("the name is alredy taken")
            return
        self.dump_user()
        print("User registered successfully")

    def login_user(self, username, password):
        for user in self.db_users.values():
            if user["username"] == username and user["password"] == password:
                print("User logged in successfully")
                return
        print("Invalid username or password")
        return


class User():
    def __init__(self, name, surname, password, email, username):
        self.name = name
        self.surname = surname
        self.password = password
        self.email = email
        self.username = username


class Admin():
    pass


forum = Forum()

forum.register_user(name='Kostya', surname='Lysenko',
                    password='123456', email='kk@gmail.com', username='wingor')
forum.register_user(name='Dima', surname='Laptev',
                    password='234425', email='dm@gmail.com', username='propovich')

while True:
    print("""
    1. Registriren
    2. Log in
    0. Exit
""")
    action_input = int(input("Enter an action: "))
    if action_input == 1:
        name = input("Enter a name: ")
        surname = input("Enter a surname: ")
        password = input("Enter a password: ")
        email = input("Enter a email: ")
        username = input("Enter a username: ")
        if name in forum.db_users.values():
            print("the name is alredy taken")
            continue
        forum.register_user(name=name, surname=surname,
                            password=password, email=email, username=username)
    elif action_input == 2:
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        forum.login_user(username=username, password=password)
    elif action_input == 0:
        print("Bye")
        exit()
