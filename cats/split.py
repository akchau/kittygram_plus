list = "Привет как сам братишка !".split()
print(list)
d = 0
for word in list:
    len_word = len(word)
    d += len_word
print(d)
