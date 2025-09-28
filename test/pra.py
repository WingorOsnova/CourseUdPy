# def print_even_numbers(numbers):
#     result = [] # task 1
#     for num in numbers:
#         if num % 2 == 0:
#             result.append(num)
#     return result
#


# input_text_fromuser = "hello today is Sunday and i writing code, cool cool"


# def count_word_instr(text):  # task 2
#     word_count = {}
#     words = text.split()
#     for word in words:
#         word_count[word] = word_count.get(word, 0) + 1
#     return word_count


# print(count_word_instr(input_text_fromuser))


# def list_uniquel_elements(lst):  # task 3
#     return list(set(lst))


# test_list = [1, 3, 4, 2, 3, 4, 5, 19, 10, 20, 100, 100]
# print(list_uniquel_elements(test_list))

# name_list = []

# while True:  # task4
#     print("""
#     1. Add a name
#     2. Show all name
#     0. Quit
# """)
#     try:
#         choise = int(input("Enter a choise: "))
#         if choise == 0:
#             print("Bye!")
#             break
#         if choise == 1:
#             name = input("Enter a name: ")
#             name_list.append(name)
#             continue
#         if choise == 2:
#             print(name_list)
#             continue
#     except ValueError as e:
#         print(e)
#         print("Enter a number!")
#         continue


# str_list = ["hello", "hi", "bob", "Dima"]


# def filter_str(str_list): #task 5
#     return list(filter(lambda x: len(x) > 3, str_list))


# print(filter_str(str_list))

print(__name__)
