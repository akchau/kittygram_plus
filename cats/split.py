"""Скрипт для подсчета знаков в строке"""
list = "Привет как ты !".split()
print(list)
d = 0
for word in list:
    len_word = len(word)
    d += len_word
print(d)
