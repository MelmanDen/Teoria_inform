# import tkinter as tk
# import tkinter.messagebox as mb

primal_text = "abcде"
summators = []
spisok_text_to_bit = []
register = [0, 0, 0]
# замена на знаки вопрос элементы которые не подхожят под ACSII
primal_text = primal_text.encode(encoding='ascii', errors='replace')
primal_text = primal_text.decode('ascii', 'replace')
print(primal_text, type(primal_text))
for i in primal_text:
    spisok_text_to_bit.append(bin(ord(i))[2:].zfill(8))
print(spisok_text_to_bit)

kol_summators = int(input("введите колво сумматоров "))
# сдлеать вывод месседжбоксов для ввода сумматоров
for i in range(kol_summators):
    # сделать ошибку ввода для чисел больше количества регистров!!!
    summators.append(list(input('введите сумматоры ')))

for i in range(len(summators)):
    for j in range(len(summators[i])):
        summators[i][j] = int(summators[i][j])

print(summators, type(summators[0][0]))

def encoding():
    # вводим элементы которые потребуются
    spisok_text_to_bit = ['01100001', '01100010', '01100011', '00111111', '00111111']
    summators = [[0, 1], [1, 2], [0,1,2]]
    spisok_polinomov = []
    k = []
    spisok_indeksov_edinic = []

    # Из списка битов вытаскиваем индексы единиц для кодирования полиномами
    for i in range(len(spisok_text_to_bit)):
        indeks_edinic = []
        for j in range(len(spisok_text_to_bit[i])):
            if spisok_text_to_bit[i][j] == '1':
                indeks_edinic.append(j)
        spisok_indeksov_edinic.append(indeks_edinic)

    print(spisok_indeksov_edinic)

    # делам "умножение полиномов"
    for i in range(len(summators)):
        for j in range(len(summators[i])):
            for m in range(len(spisok_indeksov_edinic)):
                for c in range(len(spisok_indeksov_edinic[m])):
                    spisok_polinomov.append(spisok_indeksov_edinic[m][c] + summators[i][j])
        k.append(spisok_polinomov)
        spisok_polinomov = []

    for i in range(len(k)):
        f = []
        for j in k[i]:
            if (k[i].count(j) % 2) != 0:
                f.append(j)
        f = list(set(f))
        spisok_polinomov.append(f)
    print(spisok_polinomov)


    encoded_string = []
    max_el = 0
    for i in spisok_polinomov:
        if max_el < max(i):
            max_el = max(i)
    i = 0
    while i <= max_el:
        encoded_list = []
        for j in range(len(spisok_polinomov)):
            if i in spisok_polinomov[j]:
                encoded_list += ''.join('1')
            elif i not in spisok_polinomov[j]:
                encoded_list += ''.join('0')
        i += 1

        encoded_string.append(encoded_list)
    asd = ''
    print(encoded_string)
    for j in range(len(encoded_string)-1):
       asd += ''.join(encoded_string[j])+'.' + ''.join(encoded_string[j+1]) + '.'
    print(asd)
encoding()

