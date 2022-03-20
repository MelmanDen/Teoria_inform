import tkinter as tk
import tkinter.messagebox as mb
import re
from sympy.ntheory import isprime

def main():
    # прописываем переменные необходимые в программе
    primer = text1.get()
    primer_list = list()
    mod = text2.get()
    count_open = 0
    count_close = 0

    # Избегаем возможных ошибок
    if len(primer) == 0:
        mb.showwarning("Warning", "Заполните все строки")
    elif len(mod) == 0:
        mb.showwarning("Warning", "Заполните все строки")

    proverka = re.findall("[(0-9+*/\-^)]", primer)
    for i in primer:
        primer_list.append(i)
    if not primer_list == proverka:
        mb.showwarning("Warning", "Используйте только цифры и знаки операций")

    if not mod.isdigit():
        mb.showwarning("Warning", "Используйте только цифры")

    if not isprime(int(mod)):
        mb.showwarning("Warning", "mod должен быть простым числом")

    for i in range(len(primer)):
        if primer[i] == "(":
            count_open += 1
        elif primer[i] == ")":
            count_close += 1
        if primer[i] == "^":
            mb.showwarning("Warning", "Для возведения в степень не используйте ^")
        if primer[i] == "*" and primer[i + 1] == "*":
            mb.showwarning("Warning", "Для возведения в степень не используйте **")
        if primer[i] == "/" and primer[i + 1] == "0":
            mb.showwarning("Warning", "Делить на 0 нельзя")
    if count_open != count_close:
        mb.showwarning("Warning", "Скобки раставленны не правильно")

    # сплитим пример по знакам арифметики
    splited_primer = re.split("([(*\-+/)])", primer)
    print(splited_primer)

    # Расширенный алгоритм евклида
    def Extended_algoritm(divided, mod):
        if divided == 0:
            return mod, 0, 1
        else:
            nod, x, y = Extended_algoritm(mod % divided, divided)
        return nod, y - (mod // divided) * x, x

    # Если встречается деление заносим делитель в алгоритм евклида и изменяем / на *
    for i in range(len(splited_primer)):

        if splited_primer[i] == "/":
            divided = splited_primer[i + 1]
            print(divided)
            results = Extended_algoritm(int(divided), int(mod))

            print(f'Делитель равен {results[0]}, x = {results[1]}, y = {results[2]}')
            reversed_element = results[1]
            splited_primer[i] = '*'
            splited_primer[i + 1] = str(reversed_element)
            primer = "".join(splited_primer)
    # Решение конечного примера и вывод в граф интерфейс
    answer = eval(primer)
    answer = answer % int(mod)
    print(answer)

    lbl = tk.Label(text=answer, font=('Roboto', 10, 'bold'), bg='orange', fg='white')
    lbl.pack()
    lbl.place(x=250, y=200)

# создание приложения, полей ввода, кнопок и текста
window = tk.Tk()
window.title('calc')
window.geometry('500x300+700+400')
window.resizable(False, False)
window.configure(bg='black')

lbl1 = tk.Label(text="Калькулятор выражений в поле", font=('Roboto', 10, 'bold'), bg='orange', fg='white')
lbl1.place(x=130, y=20)

lbl1 = tk.Label(text="Выражение", font=('Roboto', 10, 'bold'), bg='orange', fg='white')
lbl1.place(x=20, y=50)
text1 = tk.Entry(width=20, font=('Roboto', 13, 'bold'), bg='red', fg='white')
text1.pack()
text1.place(x=110, y=50)

lbl2 = tk.Label(text="mod", font=('Roboto', 10, 'bold'), bg='orange', fg='white')
lbl2.place(x=310, y=50)
text2 = tk.Entry(width=10, font=('Roboto', 13, 'bold'), bg='red', fg='white')
text2.pack()
text2.place(x=350, y=50)

btn = tk.Button(text="Расчитать", font=('Roboto', 10, 'bold'), bg='green', fg='white', command=main)
btn.pack()
btn.place(x=200, y=120)

lbl3 = tk.Label(text="Ответ:", font=('Roboto', 10, 'bold'), bg='orange', fg='white')
lbl3.pack()
lbl3.place(x=205, y=200)

window.mainloop()