# def calcu(num1, operator, num2):
#     if operator == "+":
#         return num1 + num2
#     elif operator == "-":
#         return num1 - num2
#     elif operator == "*":
#         return num1 * num2
#     elif operator == "/":
#         return num1 / num2
#     else:
#         return "Invalid operator"


# print("CALCULATOR PROGRAM \n\n")
# history = []


# while True:
#     quest = input("\nWhat are you want?")
#     if quest == "q".lower():
#         break
#     elif quest == "h".lower():
#         print(history)
#         continue
#     else:
#         pass
#     num1, operator, num2 = input("Enter an exsample: ").split()
#     num1 = float(num1)
#     num2 = float(num2)
#     result = calcu(num1=num1, operator=operator, num2=num2)
#     history.append(result)
#     if history.count("Invalid operator" == True:
#         history.remove("Invalid operator")
#         continue
#     print("\nYour answer is:\n")
#     print(result)
#     print("\n")


# users=[
#     {"Id.user": 1,
#      "Name.user": "Kostya", },
#     {"Id.user": 2,
#      "Name.user": "Jasmin"},
#     {"Id.user": 3,
#      "Name.user": "Vera"},
#     {"Id.user": 4,
#      "Name.user": "Lena"},
# ]

# print(len(users))
# print(
#     f"User ID from Name: {users[0]['Name.user'].upper()} is {users[0]["Id.user"]}")
# print(f"Hi! ", users[0]["Name.user"])


# elemts_list=[1, 1.5, 'str', True, []]  # task1
# print(elemts_list)

# del elemts_list[2]  # task2
# print(elemts_list)

# print(len(elemts_list))  # task3

# elemts_list.reverse()  # print(elemts_list[::-1])  # task4
# print(elemts_list)


# secondelements_list=['one', 'two']    # task5
# print(secondelements_list)

# elemts_list.extend(secondelements_list)  # task6
# print(elemts_list)  # task7
# print(len(elemts_list))

# first_list=['one', 'two', 'three', {'b': 123}]
# second_list=['two']
# sum_list=first_list + second_list
# print(sum_list)
# print(first_list.__add__(second_list))
# sum_list.pop(1)
# print(sum_list)
# first_list.extend(second_list)
# print(first_list)

# users=[
#     {'id_user': 0,
#      'name_user': 'Kostya',
#      'surname_user': 'Lysenko',
#      'age': 18,
#      },
#     {'id_user': 1,
#      'name_user': 'Jasmin',
#      'surname_user': 'Kwadri',
#      'age': 15,
#      },
#     {'id_user': 2,
#      'name_user': 'Lena',
#      'surname_user': 'Kwadri',
#      'age': 36,
#      },
#     {'id_user': 3,
#      'name_user': 'Misha',
#      'surname_user': 'Becker',
#      'age': 16,
#      },
#     {'id_user': 4,
#      'name_user': 'Alisa',
#      'surname_user': 'Becker',
#      'age': 21,
#      },
#     {'id_user': 5,
#      'name_user': 'Vera',
#      'surname_user': 'Lysenko',
#      'age': 53,
#      },
#     dict(
#         id_user=6,
#         name_user='Yarik',
#         surname_user='Hristian',
#         age=18,
#     ),
#     dict([('id_user', 7),
#           ('name_user', 'Denis'),
#           ('surname_user', 'Poplavskiy'),
#           ('age', 41)]),
#     dict(zip(['id_user', 'name_user', 'surname_user', 'age'],
#              [8, 'Nastya', 'Tihonova', 16])),
# ]

# for user in users:
#     age=user.get("age")
#     if age < 18:
#         print(f"!{user.get("name_user")} {user.get('surname_user', "неизвестно")}. --> You can't enter, because you are too young!")
#     else:
#         print(
#             f"!{user.get("name_user")} {user.get('surname_user', "неизвестно")}. --> Welcome!")

# print("Ключей в словаре:", len(users[0]))


# numbrs=dict(zip(["a", "b", "c"], [1, 2, 3]))
# print(numbrs)
# numbrs2=dict(a=1, b=2, c=3)
# print(numbrs2)
# numbrs3=dict([("a", 1), ("b", 2), ("c", 3)])
# print(numbrs3)

# name_list=['Kostya', 'Jasmin', 'Lena', 'Misha', 'Alisa', 'Vera']
# name_dict=dict(zip(range(len(name_list)), name_list))
# print("NAME ___ ", name_dict)
# sname_dict=dict(enumerate(name_list))
# print("SNAME ___ ", sname_dict)
# nname_dict={a: name_list[a] for a in range(len(name_list))}
# print("NNAME ___ ", nname_dict)

# just_dict={}

# for x in range(3):
#     requst_key=input(f"{x + 1} Enter a name of key: ")
#     requst_value=input(f"{x + 1} Enter a value of key: ")
#     just_dict[requst_key]=requst_value

# print(just_dict)
# just_dict['tryone']="testone"
# just_dict['trytwo']="testtwo"
# print(just_dict)
# del just_dict['tryone'], just_dict['trytwo']
# print(just_dict)

# m=(1, 2, 3, 4, 5,  2, 3, 2, 2)
# res=[]
# for x in range(len(m)):
#     if m[x] == 2:
#         res.append(x)
# print(res)


# first_set={1, 2, 3, 4, 5}
# second_set={3, 4, 5, 6, 7}

# all_set=first_set.union(second_set)  # first_set | second_set
# print(all_set)

# new_set=first_set.intersection(second_set  # first_set & second_set
# print(new_set)

# diff_set=first_set.difference(second_set  # first_set - second_set
# print(diff_set)

# sym_diff_set=first_set.symmetric_difference(second_set)  # first_set ^
# print(sym_diff_set)

# iss_set=first_set.issubset(second_set  # first_set <= second_set
# print(iss_set)

# iss_set=first_set.issuperset(second_set  # first_set >= second_set
# print(iss_set)

# print(dir(set))

# just_list=(1, 2, 3)
# just_dict=dict.fromkeys(just_list, "test")
# # print(just_dict)
# # print(just_dict.get("1", "nothing"))
# # for key, value in just_dict.items():
# #     print(key, "=", value)

# # print(just_dict)

# # print(just_dict.setdefault(4, "netest"))
# print(just_dict)

# friends_set={'Yarik', 'Dima', 'Max'}
# friendstwo_set={'Yarik', 'Kiril', 'Max'}

# common_friends=friends_set.intersection(friendstwo_set)
# print(common_friends)
# not_followed_back=friends_set.difference(friendstwo_set)
# print(not_followed_back)

# f_set={'a', 'b', 'c', 'a', 'c'}
# s_set={'e', 'f', 'g', 'b', 'c'}

# print(f_set.symmetric_difference(s_set))

# nums_set={1, 2, 3, 4}
# print(nums_set)  # t1

# nums_set.add(5)
# print(nums_set  # t2

# other_nums_set={1, 4, 6, 7}
# print(other_nums_set)  # t3

# intersection_set=nums_set.intersection(other_nums_set)
# print(intersection_set)
# print(id(intersection_set))  # t4

# intersection_set=list(intersection_set)
# print(intersection_set)
# print(id(intersection_set))

# phones=set()
# quantity=[]
# phones_quantity={}
# while True:
#     phones_name_input=input("Enter a model name of phone: ")
#     if phones_name_input == "q".lower():
#         break
#     else:
#         pass

#     try:
#         quantity_input=int(input("Enter a quantity: "))
#     except ValueError:
#         print("Enter a number!")
#         continue

#     phones.add(phones_name_input)
#     quantity.append(quantity_input)
#     phones_quantity=dict(zip(phones, quantity))

# print(phones_quantity)

# def merge_lists_to_dict(list1, list2):
#     return dict(zip(list1, list2))


# fruits=['apple', 'orange', 'kiwi']
# quantity=[10, 5, 9]

# print(merge_lists_to_dict(list1=fruits, list2=quantity))
# print(fruits, quantity)


# def sum_nums(*args):  # 1tast
#     return sum(args)


# def print_profile(**kwargs):  # 2tast
#     for k, v in kwargs.items():
#         print(f"{k} = {v}")


# def merge_lists(*lists):  # 3tast
#     return list(set().union(*lists))


# def common_elements(*sets):  # 4tast
#     return set.intersection(*sets)


# print(common_elements({1, 2, 3}, {2, 3, 4}, {3, 4, 5}))
# print(merge_lists([1, 2], [1, 2], [3, 4], [5, 6]))
# print(sum_nums(10, 20, 30, 40, 50))
# print_profile(name='Kostya', age=18, city='Odessa')


# def merge_lists_to_dict(list1, list2):
#     return dict(zip(list1, list2))


# fruits=['apple', 'orange', 'kiwi']
# quantity=[10, 5, 9]

# print(merge_lists_to_dict(list1=fruits, list2=quantity))
# print(merge_lists_to_dict(fruits, list2=quantity))


# def update_car_info(**car):
#     car['is_available']=True
#     return car


# res=update_car_info(brand="BMW", price=10000)
# print(res)


# def mlt(value, mul=1, pr=print("defualt value")):
#     return value * mul


# print(mlt(11, 10000))

# from datetime import date


# def get_weekday():
#     return date.today().strftime('%A')


# def create_new_post(post, weekday=get_weekday()):
#     post_copy=post.copy()
#     post_copy['weekday']=weekday
#     return post_copy


# initial_post={
#     'id': 234,
#     'author': 'Kostya'
# }

# post_with_weekday=create_new_post(post=initial_post)
# print(f"{post_with_weekday}\n{initial_post}")

# def ot():
#     print('ot')
#     pass


# def fwc(collback_fn):
#     print("fwc")
#     collback_fn()


# fwc(ot)


# def print_number_info(num):
#     if (num % 2) == 0:
#         print(f"{num} is even")
#     else:
#         print(f"{num} is odd")


# def squere_number(num):
#     print("Square of the num is ", num * num)


# def process_number(num, callback):
#     callback(num)


# entered_num=int(input("Enter a number: "))
# process_number(num=entered_num, callback=print_number_info)
# squere_number(entered_num)


# def cook_pizza(flavor, callback):
#     res=flavor.upper()
#     callback(res)


# def eat_pizza(pizza):
#     print(f"Im eating {pizza} pizza")


# def instagram_post(pizza):
#     print(f"im posted {pizza} pizza on instagram")


# cook_pizza("Papironi", instagram_post)


# def process_list(lst, callback):
#     return [callback(n) for n in lst]


# def square(n):
#     return n*n


# def double(n):
#     return n*2


# print(process_list([2, 4, 5, 10], double))
# print(process_list([2, 4, 5, 10], square))


# def process_info(info, users_id, callback):
#     info_copy=info.copy()
#     callback(info_copy, users_id)
#     return info_copy


# def sent_info(info_copy, users_id):
#     print("sent info from user to server...")
#     print("info from user saved in server")
#     info_copy['id']=len(users_id) + 1
#     users_id.add(info_copy['id'])
#     print(info_copy)


# def print_info(info_user, users_id):
#     print("user entered:")
#     print(info_user)


# users={1, 2, 3, 4, 5, 6}

# info={
#     'name': 'Dima',
#     'surname': 'Laptev',
#     'age': 18
# }

# info_two={
#     'name': 'Kostya',
#     'surname': 'Lysenko',
#     'age': 18
# }

# entered_info=process_info(info=info, users_id=users, callback=print_info)
# print(users)

# new_user_info=process_info(info=info, users_id=users, callback=sent_info)
# print(users)

# entered_info=process_info(info=info_two, users_id=users, callback=print_info)
# print(users)

# new_usertwo_info=process_info(
#     info=info_two, users_id=users, callback=sent_info)
# print(users)
# def process_info(info, users_id, callback):
#     info_copy=info.copy()
#     callback(info_copy, users_id)
#     return info_copy


# def sent_info(info_copy, users_id):
#     print("📤 Sent info from user to server...")
#     info_copy['id']=len(users_id) + 1
#     users_id.add(info_copy['id'])
#     print("✅ Info saved:", info_copy)


# def print_info(info_copy, users_id):
#     print("📝 User entered:")
#     for key, value in info_copy.items():
#         print(f"{key}: {value}")


# users={1, 2, 3, 4, 5, 6}

# while True:
#     print("\n--- Menu ---")
#     print("1. Enter new user")
#     print("2. Quit")
#     choice=input("Select action: ")

#     if choice == "2":
#         print("Bye! 👋")
#         break

#     if choice == "1":
#         name=input("Enter name: ")
#         surname=input("Enter surname: ")
#         age=input("Enter age: ")

#         info={"name": name, "surname": surname, "age": age}

#         action=input("Choose action (print / send): ").strip().lower()
#         if action == "print":
#             process_info(info, users, print_info)
#         elif action == "send":
#             process_info(info, users, sent_info)
#         else:
#             print("❌ Unknown action")

#     print(f"Current users ID: {users}")

# ###### TASK OPERATION########

# set_one={1, 2, 3, 4, 5}
# set_two={1, 3, 2, 4, 5}
# set_three=set_two

# print("set one: ", set_one == set_two)  # True

# print("set one is: ", set_one is set_two)   # False

# print("set three is: ", set_three is set_two)  # True

# print(10 in set_one)  # False
# print(10 not in set_one)  # True
# print(1 in set_one)  # True

# #### LAMBDA FUNCTION####
# def greeting(greet):
#     return lambda name: f"{greet}, {name}"


# m_g=greeting("Good Morning")
# print(m_g("Kostya"))
# a_g=greeting("Good Afternoon")
# print(a_g("Kostya"))
# e_g=greeting("Good Evening")
# print(e_g("Kostya"))
# n_g=greeting("Good Night")
# print(n_g("Kostya"))

# try:
#     print(int(1 / "0"))
# except BaseException as e:
#     print(e)
# else:
#     print("no error")
# finally:
#     print("End of program")

# print("continue...")


# class PasswordError(Exception):
#     pass


# def login(login, password):
#     if password != 123456:
#         raise PasswordError("Неверный пароль")
#     print("Успешная авторизация")


# login("kostya", 1234567)


# def image_info(img):
#     new_dict=img.copy()
#     if "image_id" not in new_dict or "image_title" not in new_dict:
#         raise KeyError("Ключа image_id или image_title нет в словаре")
#     print(
#         f"Image {new_dict.get('image_title', 'unknown')} has id {new_dict.get('image_id', 'unknown')}")
#     return new_dict


# img_one={
#     "image_id": 1,
#     "image_title": "My_boy"
# }
# img_two={
#     "image_id": 1,
# }

# try:
#     new_dict=image_info(img_one)
#     dict_two=image_info(img_two)
# except KeyError as e:
#     print(e)

# class LoginError(Exception):
#     pass


# class PasswordError(Exception):
#     pass


# def login(login, password):
#     if login != "admin":
#         raise LoginError("Неверный логин")
#     if password != 123456:
#         raise LoginError("Неверный пароль")
#     print("Успешная авторизация")


# try:
#     login("admin", 123456)
# except (LoginError, PasswordError) as e:
#     print(e)
# else:
#     print("Welcome!")
# finally:
#     print("End of program")

# def zero_division(a, b):
#     if b == 0:
#         raise ZeroDivisionError("Деление на ноль")
#     return a / b


# try:
#     result = zero_division(10, 1)
# except ZeroDivisionError as e:
#     print(e)
# else:
#     print(int(result))
# finally:
#     print("End of program")

# def image_info(img):
#     new_dict = img.copy()
#     if "image_id" not in new_dict or "image_title" not in new_dict:
#         raise KeyError("Ключа image_id или image_title нет в словаре")
#     print(
#         f"Image {new_dict.get('image_title')} has id {new_dict.get('image_id')}")


# img = {
#     "image_id": 1,
#     "image_title": "My_boy",
#     'age': 18
# }

# img_two = {
#     "image_id": 1,
# }^
# try:
#     image_info(img)
#     image_info(img_two)
# except KeyError as e:
#     print(e)
# finally:
#     print("End of program")

###### UNPICKING ######

# fruits = ['cherry', 'kiwi', "strawbarry"]

# cherry, *other_fruits = fruits
# cherry_two, kiwi, strawbarry = fruits

# print(cherry_two, kiwi, strawbarry)
# print(cherry)
# print(other_fruits)


# user_profile = {
#     'name': 'Admin',
#     'comments_qty': 22,
# }


# def user_info(name, comments_qty=0):
#     if not comments_qty:
#         return f"{name} has no comments"
#     return f"{name} has {comments_qty} comments"


# print(user_info(**user_profile))


# list_dict = [
#     {
#         'name': 'Kostya',
#         'age': 18,
#     },
#     {
#         'name': 'Jasmin',
#         'age': 15,
#     },
#     {
#         'name': 'Lena',
#         'age': 36,

#     },
# ]

# firts_dict, second_dict, third_dict = list_dict


# def info(name, age):
#     return f"{name} is {age} years old"


# print(info(**firts_dict))
# print(info(**second_dict))
# print(info(**third_dict))


# def nums_info(a, b):
#     if (type(a) is not int) or (type(b) is not int):
#         return "One arguments is not INTEGER"
#     elif a >= b:
#         return "A is bigger than B"
#     return "B is bigger than A"


# print(nums_info(a=1, b=2))


# def numss_info(a, b):
#     if (type(a) is not int) or (type(b) is not int):
#         return "One arguments is not INTEGER"
#     if a >= b:
#         return "A is bigger than B"
#     return "B is bigger than A"


# print(numss_info(a=1, b=2))


# def route_inf(info):
#     if ("distance" in info) and (isinstance(info["distance"], int)):
#         return f"Distance to your destination is {info['distance']} km"
#     elif ("speed" in info) and ('time' in info):
#         return f"Distance to your destination is {info['speed'] * info['time']} km"
#     return "No distance info is available"


# info_all = dict(
#     distance=600,
#     speed=60,
#     time=10,
# )
# info_without_distance = dict(
#     speed=60,
#     time=10,
# )
# info_without_ds = dict(
#     time=10,
# )
# any_info = {
#     'time': 20,
#     'speed': 90,
# }
# print(route_inf(info_all))
# print(route_inf(info_without_distance))
# print(route_inf(info_without_ds))
# print(route_inf(any_info))

#### REMEMBER IT ####
# test_dict = {}

# test_dict = {input("Enter a kay: "): input("Enter a value: ")
#              for x in range(3)}
# print(test_dict)

# def sent_img(img):
#     print("Img is sent")


# def process_img(img):
#     print("Img is processing")
#     img_copy = img.copy()
#     img_copy["id"] = 1
#     print("sent umg after processing")


# img = {
#     "image_title": "My_boy",
#     'age': 18
# }
# sent_img(img) if "id" in img else process_img(img)

# str_input = "dpjowhfojfjsd,asf"
# print("the text has more 79 elements") if len(
#     str_input) > 79 else print("the text has less 79 elements")

# import json

# ll = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# dd = {
#     'a': 1,
#     'b': 2,
#     'c': 3,
#     'd': 4,
#     'e': 5,
# }
# for key, value in dd.items():
#     print(key, value)

# nemes = ['Dima', 'Igor', 'Danya', 'Vlad', 'Nastya', 'Lena']

# for id, name in enumerate(nemes):
#     print(id + 1, name)

# with open("test.json", "w", encoding="utf-8") as f:
#     json.dump(dd, f, indent=2, ensure_ascii=False)
# print("DONE")

# with open("test.json", "r", encoding="utf-8") as f:
#     data = json.load(f)
# print(data)

# data["name"] = "Kostya"
# print(data)

# with open("test.json", "w", encoding="utf-8") as f:
#     json.dump(data, f, indent=2, ensure_ascii=False)
# print("DONE")
# print(dir(list))


# def load_json(file_path):
#     with open(file_path, "r", encoding="utf-8") as f:
#         return json.load(f)


# def save_json(file_path, data):
#     with open(file_path, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=2, ensure_ascii=False)
#     print("DONE")


# data = load_json("test.json")
# print(data)
# del data["skills"][0]
# save_json("test.json", data)
# print(data)

# TASK 1 for FORIN
# dd = {
#     'name': 'Kostya',
#     'age': 18,
#     'city': 'Odessa',
# }


# def dict_to_list(dict):
#     list_tuple = []
#     for k, v in dict.items():
#         if isinstance(v, int):
#             v *= 2
#         tuples = (k, v)‚
#         list_tuple.append((k, v))
#     return list_tuple


# print(dict_to_list(dd))
# #########

# l_list = [10, "asb", True, False, True, 10.2, 23.4, "asü", "aodfk"]


# def filter_list(list, value_filter):
#     result = []
#     for x in list:
#         if type(x) == value_filter:
#             result.append(x)
#     return result


# print(filter_list(l_list, str))
# print(filter_list(l_list, float))
# print(filter_list(l_list, bool))
# ####

# f = filter(lambda x: type(x) == float, l_list)
# print(list(f))


# def filter_list(list_to_filter, value_type):
#     return list(filter(lambda x: type(x) == value_type, list_to_filter))


# res = filter_list([1, 2, 34, 5, "sa", "asda", True], bool)
# print(res)

# # print(Exception.__subclasses__())

# litelers = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]

# for i, v in enumerate(litelers):
#     print(i + 1, v)

# 06.09.2025

# x = 10

# while x < 110:
#     print(x)
#     x += 10

# import random

# random_num = random.randint(1, 10)
# while True:
#     num = int(input("Enter a number: "))
#     if num != random_num:
#         print("Try again...")
#         continue
#     print("You win!", random_num)
#     break

### Task about while loop ###

# while True:
#     try:
#         num_one = int(input("Enter a first number: "))
#         num_two = int(input("Enter a second number: "))
#         print(num_one / num_two)
#     except ValueError:
#         print("Enter a number!")
#         continue
#     except ZeroDivisionError as e:
#         print(e)
#         continue
#     while True:
#         ask_cont = input("Do you want continue: (y or n) ")
#         if ask_cont == "y":
#             break
#         elif ask_cont == "n":
#             print("Bye!")
#             exit()
#         else:
#             print("Enter only y or n")
#             continue

# nums = [-1, -2, -3, 4, 5, 10, 23, -214, 123, -2222, -12, -123, 220]

# absolute_nums = [abs(x)for x in nums] # впервые узнал об функции abs()
# print(absolute_nums)

# positive_nums = [x for x in nums if x > 0]
# print(positive_nums)

# my_set = set(positive_nums)
# print(my_set)
# new_set = set(i*i for i in my_set)
# print(new_set)

# my_scores = dict(
#     a=10,
#     b=20,
#     c=30
# )

# scores = {k: v*2 for k, v in my_scores.items()}
# print(scores)  # 4.05 min

# literes = ["a", "b", "c", "d", "e", "f", "g"]

# dd = {k: v for k, v in enumerate(literes)}
# print(dd)   #1.30 min это все время выполнения.

# task about list confirenschen то есть фор ин в одной строке
# task1
# dictr = {
#     '1': 'a',
#     '2': 'b',
#     '3': 'c'
# }

# dictr_upper = {k: v.upper() for k, v in dictr.items()}
# print(dictr_upper)  # 2min

# # task2

# task_list = ['a', 'b', 'boba', 'big', 'i love mum', 'im Kostya']

# list_more_three_elem = [elem for elem in task_list if len(elem) >= 3]
# print(list_more_three_elem)  # 3 min
# finish saction for in, in one string

# start topic for in generation

# from sys import getsizeof
# squares = (num * num for num in range(1, 11))

# for num in squares:
#     print(num)

# print()
# squares_gen = (num * num for num in range(1, 1000000))
# print(getsizeof(squares_gen))
# squares_list = list(squares_gen)
# print(getsizeof(squares_list))


# def infinity_id():
#     id = 0
#     while True:
#         yield id
#         id += 1


# g_i = infinity_id()  # g_i = generation_id
# print(next(g_i))
# print(next(g_i))

# user_one = {
#     'name': 'Kostya',
#     'id': None,
# }
# user_one['id'] = next(g_i)
# print(user_one)
# user_two = user_one.copy()
# user_two['name'] = 'Jasmin'
# user_two['id'] = next(g_i)
# print(user_two)
# g = (num for num in range(1, 100))
# u = {
#     'name': 'Kostya',
#     'id': None
# }
# u['id'] = next(g)
# print(u)

# # и так отчет ну вообщем прикольно просто не понимаю где использовать и изза этого могу забыть.


# # сегодня 08.09.2025 начал модуль ооп в моем курсе

# # class Car:
# #     def move(self):
# #         print("Car is moving")

# #     def stop(self):
# #         print("Car is stopped")


# # my_car = Car()
# # my_car.move()
# # my_car.stop()

# # class User:
# #     def __init__(self, name, age, city):
# #         self.name = name
# #         self.age = age
# #         self.city = city

# #     def show_info(self):
# #         print(f"""
# #     User_name: {self.name}
# #     User_age: {self.age}
# #     User_city: {self.city}
# # """)


# # user_one = User('Kostya', 18, 'Odessa')
# # user_one.show_info()

# # class Car:
# #     def __init__(self, brand, year, price):
# #         self.brand = brand
# #         self.year = year
# #         self.price = price

# #     def show_info(self):
# #         print(f"""
# #         Brand: {self.brand}.
# #         Year: {self.year}.
# #         Price: {self.price}$.""")


# # car_one = Car("BMW", 2020, 10000)
# # car_one.show_info()
# # print(car_one.__dict__)

# # class ZeroError(Exception):  # самоястоятельная проверка не забыл ли я исключения
# #     pass


# # def zero_division(a, b):
# #     if b == 0:
# #         raise ZeroError("Деление на ноль")
# #     return a / b


# # try:
# #     result = zero_division(10, 0)
# # except ZeroError as e:
# #     print(e)
# # else:
# #     print(int(result))
# # finally:
# #     print("End of program")


# # class Comment:
# #     def __init__(self, text):
# #         self.text = text
# #         self.votes_qty = 0

# #     def add_vote(self):
# #         self.votes_qty += 1
# #         print(f"{self.votes_qty} votes added")


# # comment_one = Comment("First comment")
# # comment_one.add_vote()
# # comment_one.add_vote()


# class Image():      # task from cource
#     def __init__(self, resolution, title, comment):
#         self.resilution = resolution
#         self.title = title
#         self.comment = comment

#     def resize(self, new_resolution):
#         self.resilution = new_resolution
#         print("Image is resized")

#     def __str__(self):
#         return f"""
#         Resolution: {self.resilution}.
#         Title: {self.title.upper()}.
#         Comment: {self.comment}."""

#     def __repr__(self):
#         return f"""Atrebuts: {self.__dict__}"""

#     def change_comment(self, new_comment):
#         self.comment = new_comment
#         print("Comment is changed")

#     def change_title(self, new_title):
#         self.title = new_title
#         print("Title is changed")


# image_one = Image('1980x1020', 'my_dog', "This my dog Bobi, i very like him!")
# image_one.resize('1020x1020')
# print(image_one)
# image_one.change_comment("I VERY LIKE MY DOG BOBI!!")
# print(image_one)


# class Comment():
#     total_comments = 0

#     def __init__(self, text):
#         self.text = text
#         self.votes_qty = 0
#         Comment.total_comments += 1

#     @staticmethod
#     def merge_comments(firts, second):
#         return f"{firts.text} {second.text}"


# comment_one = Comment("First comment")
# comment_two = Comment("Second comment")
# print(Comment.merge_comments(comment_one, comment_two))
# merge_comment = Comment('avavasvs')
# print(merge_comment.merge_comments(comment_one, comment_two))
# print(Comment.total_comments)


# class Proba(Comment):
#     def __init__(self, text):
#         self.text = text
#         self.votes_qty = 0
#         Comment.total_comments += 1


# tirty_comment = Proba("acada")
# print(tirty_comment.total_comments)
# Comment.total_comments = 100
# print(tirty_comment.total_comments)
# print(Comment.total_comments)
# закончил раздел ООП классы и объекты.
# начал раздел магические методы в классах
# class Comment():

#     def __init__(self, text):
#         self.text = text
#         self.votes_qty = 0

#     def up_votes(self):
#         self.votes_qty += 1

#     def __add__(self, other):
#         return (f"{self.text} {other.text}", self.votes_qty + other.votes_qty)

#     def __eq__(self, other):
#         return (self.text == other.text and
#                 self.votes_qty == other.votes_qty)


# comment_one = Comment("First comment")
# comment_two = Comment("Second comment")
# comment_one.up_votes()
# comment_two.up_votes()
# print(comment_one == comment_two)

# сегодня 10.09.2025 продалождаю разде маг методы.

# class ExtendedList(list):
#     def print_element_info(self):
#         print(f"List has {len(self)} elements.")

#     def print_element_type(self):
#         self.dictwithtype = {}
#         for id, v in enumerate(self):
#             if isinstance(v, int):
#                 self.dictwithtype[id] = "int"
#         for id, v in enumerate(self):
#             if isinstance(v, str):
#                 self.dictwithtype[id] = "str"
#         print(self.dictwithtype)


# test_list = [1, 2, 3, 4, 5, 6, 'asdasd']
# mm = ExtendedList(test_list)
# mm.print_element_info()
# mm.print_element_type()
