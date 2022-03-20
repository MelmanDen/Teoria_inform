a = "abcде"
summators = []
b = []
# замена на знаки вопрос элементы которые не подхожят под ACSII
a = a.encode(encoding='ascii', errors='replace')
a = a.decode('ascii', 'replace')
print(a, type(a))
for i in a:
    b.append(bin(ord(i))[2:].zfill(8))
print(b)
for i in b:
    print(i, type(i))


kol_summators = int(input("введите колво сумматоров "))
# сдлеать вывод месседжбоксов для ввода сумматоров
for i in range(kol_summators):
    # сделать ошибку ввода для чисел больше количества регистров!!!
    summators.append(input('введите сумматоры '))
print(summators, type(summators))

print(kol_summators)