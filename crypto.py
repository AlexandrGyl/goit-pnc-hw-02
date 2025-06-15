import math 

# --- Vigenere code ---
def extend_key(text, key):
    key = key.upper()
    new_key = []
    key_index = 0
    for char in text:
        if char.isalpha():
            new_key.append(key[key_index % len(key)])
            key_index += 1
        else:
            new_key.append(char)
    return ''.join(new_key)

def vigenere_encrypt(text, key):
    text = text.upper()
    key = extend_key(text, key)
    cipher_text = []
    for i in range(len(text)):
        if text[i].isalpha():
            x = (ord(text[i]) - ord('A') + ord(key[i]) - ord('A')) % 26
            cipher_text.append(chr(x + ord('A')))
        else:
            cipher_text.append(text[i])
    return ''.join(cipher_text)

def vigenere_decrypt(text, key):
    text = text.upper()
    key = extend_key(text, key)
    decrypted_text = []
    for i in range(len(text)):
        if text[i].isalpha():
            x = (ord(text[i]) - ord(key[i]) + 26) % 26
            decrypted_text.append(chr(x + ord('A')))
        else:
            decrypted_text.append(text[i])
    return ''.join(decrypted_text)

# --- permutation cipher using keywords ---
def get_column_order(keyword):
    seen = set()
    filtered_key = ''.join([c for c in keyword if not (c in seen or seen.add(c))])
    sorted_key = sorted(filtered_key)
    return [sorted_key.index(c) for c in filtered_key]

def transposition_encrypt(text, keyword):
    key_order = get_column_order(keyword.upper())
    num_cols = len(key_order)
    num_rows = math.ceil(len(text) / num_cols)
    matrix = [''] * num_cols
    for i, char in enumerate(text):
        col = i % num_cols
        matrix[col] += char
    encrypted = ''
    for index in sorted(range(num_cols), key=lambda k: key_order[k]):
        encrypted += matrix[index]
    return encrypted

def transposition_decrypt(cipher_text, keyword):
    key_order = get_column_order(keyword.upper())
    num_cols = len(key_order)
    num_rows = math.ceil(len(cipher_text) / num_cols)
    num_full_cols = len(cipher_text) % num_cols
    if num_full_cols == 0:
        num_full_cols = num_cols
    col_lengths = [num_rows if i < num_full_cols else num_rows - 1 for i in range(num_cols)]
    cols = [''] * num_cols
    pos = 0
    for index in sorted(range(num_cols), key=lambda k: key_order[k]):
        length = col_lengths[index]
        cols[index] = cipher_text[pos:pos + length]
        pos += length
    decrypted = ''
    for i in range(num_rows):
        for col in cols:
            if i < len(col):
                decrypted += col[i]
    return decrypted

# --- matrix cipher ---
def matrix_encrypt(text, key):
    key = key.upper()
    key_order = get_column_order(key)
    num_cols = len(key_order)
    num_rows = math.ceil(len(text) / num_cols)
    text += 'X' * ((num_cols * num_rows) - len(text))  
    matrix = [''] * num_cols
    for i in range(len(text)):
        col = i % num_cols
        matrix[col] += text[i]
    encrypted = ''
    for index in sorted(range(num_cols), key=lambda k: key_order[k]):
        encrypted += matrix[index]
    return encrypted

def matrix_decrypt(cipher_text, key):
    key = key.upper()
    key_order = get_column_order(key)
    num_cols = len(key_order)
    num_rows = math.ceil(len(cipher_text) / num_cols)
    num_full_cols = len(cipher_text) % num_cols
    if num_full_cols == 0:
        num_full_cols = num_cols
    col_lengths = [num_rows if i < num_full_cols else num_rows - 1 for i in range(num_cols)]
    cols = [''] * num_cols
    pos = 0
    for index in sorted(range(num_cols), key=lambda k: key_order[k]):
        length = col_lengths[index]
        cols[index] = cipher_text[pos:pos + length]
        pos += length
    decrypted = ''
    for i in range(num_rows):
        for col in cols:
            if i < len(col):
                decrypted += col[i]
    return decrypted

# --- MAIN MENU ---
while True:
    print ("\n"
    "Для початку роботи із програмою  створіть файл input.txt в кталозі із прорамою." "\n"
    "Вставте текст який хочете зашифрувати у створений файл")
    print("\n Оберiть дію:")
    print("1 - Зашифрувати (Віженера)")
    print("2 - Розшифрувати (Віженера)")
    print("3 - Зашифрувати (Перестановка з текстовим ключем)")
    print("4 - Розшифрувати (Перестановка з текстовим ключем)")
    print("5 - Зашифрувати (Табличний шифр)")
    print("6 - Розшифрувати (Табличний шифр)")
    print("0 - Вийти")
    choice = input("Ваш вибір: ")

    if choice == "1":
        vigenere_key = input("Введіть англійською ключ для шифрування шифром Віжінера: ")
        try:
            with open("input.txt", "r", encoding="utf-8") as f:
                text = f.read()
            encrypted = vigenere_encrypt(text, vigenere_key)
            with open("vig_encrypted.txt", "w", encoding="utf-8") as f:
                f.write(encrypted)
            print("Зашифровано шифром Віженера → vig_encrypted.txt")
        except FileNotFoundError:
            print("Файл input.txt не знайдено!")

    elif choice == "2":
        vigenere_key = input("Введіть ключ, який використовувався для шифрування: ")
        try:
            with open("vig_encrypted.txt", "r", encoding="utf-8") as f:
                text = f.read()
            decrypted = vigenere_decrypt(text, vigenere_key)
            with open("vig_decrypted.txt", "w", encoding="utf-8") as f:
                f.write(decrypted)
            print("Розшифровано шифром Віженера → vig_decrypted.txt")
        except FileNotFoundError:
            print("Файл vig_encrypted.txt не знайдено!")

    elif choice == "3":
        keyword_key = input("Введіть фразу-ключ для простої перестановки (великі англійські літери): ")
        try:
            with open("input.txt", "r", encoding="utf-8") as f:
                text = f.read()
            encrypted = transposition_encrypt(text, keyword_key)
            with open("trans_encrypted.txt", "w", encoding="utf-8") as f:
                f.write(encrypted)
            print("Зашифровано простою перестановкою → trans_encrypted.txt")
        except FileNotFoundError:
            print("Файл input.txt не знайдено!")

    elif choice == "4":
        keyword_key = input("Введіть фразу-ключ, яка використовувалась для шифрування: ")
        try:
            with open("trans_encrypted.txt", "r", encoding="utf-8") as f:
                text = f.read()
            decrypted = transposition_decrypt(text, keyword_key)
            with open("trans_decrypted.txt", "w", encoding="utf-8") as f:
                f.write(decrypted)
            print("Розшифровано простою перестановкою → trans_decrypted.txt")
        except FileNotFoundError:
            print("Файл trans_encrypted.txt не знайдено!")

    elif choice == "5":
        matrix_key = input("Введіть фразу-ключ для табличного шифрування: ")
        try:
            with open("input.txt", "r", encoding="utf-8") as f:
                text = f.read()
            encrypted = matrix_encrypt(text, matrix_key)
            with open("matrix_encrypted.txt", "w", encoding="utf-8") as f:
                f.write(encrypted)
            print("Зашифровано табличним шифром → matrix_encrypted.txt")
        except FileNotFoundError:
            print("Файл input.txt не знайдено!")

    elif choice == "6":
        matrix_key = input("Введіть фразу-ключ для дешифрування: ")
        try:
            with open("matrix_encrypted.txt", "r", encoding="utf-8") as f:
                text = f.read()
            decrypted = matrix_decrypt(text, matrix_key)
            with open("matrix_decrypted.txt", "w", encoding="utf-8") as f:
                f.write(decrypted)
            print("Розшифровано табличним шифром → matrix_decrypted.txt")
        except FileNotFoundError:
            print("Файл matrix_encrypted.txt не знайдено!")

    elif choice == "0":
        print("Вихід з програми.")
        break
    else:
        print("Невірна команда. Спробуйте ще раз.")
