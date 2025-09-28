import tkinter as tk

OPS = set("+-*/")
ALLOWED = set("0123456789.+-*/() ")  # что разрешаем в выражении


# created window
root = tk.Tk()
root.title("Calculator by Wingor")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


window_width = 500
window_height = 500
x = (screen_width / 2) - (window_width / 2)
y = (screen_height / 2) - (window_height / 2)
root.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")
root.resizable(False, False)

expr = tk.StringVar(value="")
display = tk.Entry(root, textvariable=expr, font=(
    "SF Mono", 24), justify="right", bd=8, relief="groove", state="readonly")
display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=12, pady=12)

for c in range(4):
    root.columnconfigure(index=c, weight=1)
for r in range(6):
    root.rowconfigure(index=r, weight=1)


def on_click(ch: str):
    s = expr.get()

    # 1) Операторы
    if ch in OPS:
        if not s:
            # начинать с оператора нельзя, кроме унарного минуса
            if ch == "-":
                expr.set("-")
            return
        # если последний символ тоже оператор — заменяем
        if s[-1] in OPS:
            s = s[:-1]
            expr.set(s + ch)
            return
        expr.set(s + ch)
        return

    # 2) Точка: одна в текущем числе
    if ch == ".":
        num = _current_number_fragment(s)
        if "." in num:
            return  # игнорируем вторую точку
        # если точка после оператора или в начале — добавим ведущий 0
        if not s or s[-1] in OPS or s[-1] == "(":
            s += "0"
        expr.set(s + ".")
        return

    # 3) Скобки (если решишь добавить кнопки "(" и ")")
    if ch == "(":
        # перед "(" обычно либо начало, либо оператор, либо "("
        if not s or s[-1] in OPS or s[-1] == "(":
            expr.set(s + "(")
        return

    if ch == ")":
        # закрывающую скобку можно ставить, если есть хоть одна незакрытая
        # и последний символ — число или ")"
        if _balanced_parens(s + ")") and (s and (s[-1].isdigit() or s[-1] == ")")):
            expr.set(s + ")")
        return

    # 4) Цифры
    if ch.isdigit():
        expr.set(s + ch)
        return

    # 5) На всякий случай — игнор всего остального
    return


def on_clear():
    expr.set("")


def on_backspace():
    s = expr.get()
    if s:
        expr.set(s[:-1])


def on_calc():
    s = expr.get().strip()
    # простая фильтрация: только разрешённые символы
    if not s or any(ch not in ALLOWED for ch in s):
        expr.set("Error")
        return
    # баланс скобок (если используешь скобки)
    if not _balanced_parens(s):
        expr.set("Error")
        return
    try:
        # отключаем встроенные функции
        result = eval(s, {"__builtins__": None}, {})
        # доп. нормализация результата
        if isinstance(result, float):
            # убираем лишние .0 и округляем
            result = round(result, 10)
            # преобразуем -0.0 в 0
            if result == -0.0:
                result = 0.0
        expr.set(str(result))
    except ZeroDivisionError:
        expr.set("Error")  # можешь поставить "Division by 0"
    except Exception:
        expr.set("Error")


def _balanced_parens(s: str) -> bool:
    """Проверка баланса скобок () — на будущее (можешь не ставить скобки в UI сразу)."""
    bal = 0
    for ch in s:
        if ch == "(":
            bal += 1
        elif ch == ")":
            bal -= 1
            if bal < 0:
                return False
    return bal == 0


def _current_number_fragment(s: str) -> str:
    """Возвращает часть строки справа до ближайшего оператора (текущее число)."""
    i = len(s) - 1
    while i >= 0 and (s[i].isdigit() or s[i] == "."):
        i -= 1
    return s[i+1:]


def handle_key(event):
    ch = event.char
    if ch and (ch.isdigit() or ch in OPS or ch in "()".strip()):
        on_click(ch)
        return
    if ch == ".":
        on_click(".")
        return
    if event.keysym in ("Return", "KP_Enter"):
        on_calc()
        return
    if event.keysym == "BackSpace":
        on_backspace()
        return
    if event.keysym == "Escape":
        on_clear()
        return


root.bind("<Key>", handle_key)


root.bind("<Key>", handle_key)
2

buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
]

extra = [("C", 5, 0), ("⌫", 5, 1)]

for (text, r, c) in extra:
    cmd = on_clear if text == "C" else on_backspace
    tk.Button(
        root, text=text,
        command=cmd,
        font=("Inter", 16), bd=1, relief="raised"
    ).grid(row=r, column=c, sticky="nsew", padx=6, pady=6
           )

tk.Button(root, text="=", command=on_calc, font=("Inter", 16)).grid(
    row=4, column=2, sticky="nsew", padx=6, pady=6
)


for (text, r, c) in buttons:
    tk.Button(
        root, text=text,
        command=(lambda ch=text: on_click(ch)),
        font=("Inter", 16), bd=1, relief="raised"
    ).grid(row=r, column=c, sticky="nsew", padx=6, pady=6)


root.mainloop()
