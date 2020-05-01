import numpy as np


def caesar(plain, key):
    plain = plain.upper()
    cipher = str()
    for p in plain:
        cipher += chr(((ord(p) - ord('A') + key) % 26) + ord('A'))
    return cipher


def vigenere(plain, key, auto):
    plain = plain.upper()
    key = key.upper()
    if auto:
        key += plain
    else:
        key = key * (len(plain) // len(key) + 1)
    cipher = ""
    for i in range(0,len(plain)):
        cipher += caesar(plain[i], ord(key[i]) - ord('A'))
    return cipher


def hill(plain, key):
    cipher = ""
    plain = plain.upper()
    dim2 = key.shape[0]
    plain += "X" * ((dim2 - len(plain) % dim2) % dim2)
    dim1 = int(len(plain) / dim2)
    cipher_mat = np.zeros((dim1, dim2))
    for i in range(dim1):
        for j in range(dim2):
            cipher_mat[i][j] = ord(plain[dim2 * i + j]) - ord('A')
    res = np.remainder(np.dot(cipher_mat, key), 26) + ord('A')
    for i in range(dim1):
        for j in range(dim2):
            cipher += chr(int(res[i][j]))
    return cipher


def matrix(x, y, initial):
    return [[initial for i in range(x)] for j in range(y)]


def get_index(p, mat):
    for i in range(5):
        for j in range(5):
            if mat[i][j] == p:
                return i, j


def get_cipher_letters(i1, i2, j1, j2, mat):
    if i1 == i2:
        return mat[i1][(j1+1) % 5], mat[i2][(j2+1) % 5]
    elif j1 == j2:
        return mat[(i1+1) % 5][j1], mat[(i2+1) % 5][j2]
    else:
        diff = abs(j1-j2)
        if j1 > j2:
            return mat[i1][j1 - diff], mat[i2][j2 + diff]
        else:
            return mat[i1][j1 + diff], mat[i2][j2 - diff]


def process_plain(plain):
    res = ""
    i = 0
    while i < len(plain):
        res += plain[i]
        if i+1 < len(plain):
            if plain[i+1] == plain[i]:
                res += 'X'
                i += 1
                continue
            res += plain[i + 1]
        i += 2
    if len(res) % 2 != 0:
        res += 'X'
    res = res.replace("J", "I")
    return res


def play_fair(plain, key):
    key = key.replace(" ", "")
    key = key.upper()
    plain = plain.upper()
    cipher = ""
    result = list()
    for c in key:  # storing key
        if c not in result:
            if c == 'J':
                result.append('I')
            else:
                result.append(c)
    flag = 0
    for i in range(65, 91):  # storing other character
        if chr(i) not in result:
            if i == 73 and chr(74) not in result:
                result.append("I")
                flag = 1
            elif flag == 0 and i == 73 or i == 74:
                pass
            else:
                result.append(chr(i))
    k = 0
    my_matrix = matrix(5, 5, 0)  # initialize matrix
    for i in range(0, 5):  # making matrix
        for j in range(0, 5):
            my_matrix[i][j] = result[k]
            k += 1
    plain = process_plain(plain)
    for i in range(0,len(plain)-1, 2):
        i1, j1 = get_index(plain[i], my_matrix)
        i2, j2 = get_index(plain[i+1], my_matrix)
        c1, c2 = get_cipher_letters(i1,i2,j1,j2,my_matrix)
        cipher += c1
        cipher += c2
    return cipher


def vernam(plain, key):
    xkey = list()
    for i in key:
        xkey.append(ord(i) - ord('A'))
    l = len(xkey)
    ans = ""
    for i in range(0, len(plain)):
        p = (ord(plain[i]) - ord('A')) ^ xkey[i % l]
        ans += chr(p + ord('A'))
    return ans


def read_file(filename):
    file = open(filename, "r")
    ans = []
    for p in file.readlines():
        ans.append(p.replace("\n", ""))
    return ans


def write_file(filename, strlist):
    file = open(filename, "w")
    for st in strlist:
        file.write(st + "\n")


def cipher(keys, plains_file, ciphers_file, algo):
    plains = read_file(plains_file)
    ciphers = []
    if algo == hill:
        for p in plains:
            ciphers.append(algo(p, keys))
        write_file(ciphers_file, ciphers)
        return
    for k in keys:
        ciphers.append("key: " + str(k))
        for p in plains:
            ciphers.append(algo(p, k))
        ciphers.append("\n")
    write_file(ciphers_file, ciphers)


if __name__ == "__main__":
    keys = [3, 6, 12]
    cipher(keys, "caesar_plain.txt", "caesar_cipher.txt", caesar)

    plains = read_file("vigenere_plain.txt") # Vigenere
    keys = [("PIE",False), ("AETHER", True)]
    ciphers = []
    for k in keys:
        ciphers.append("key: " + str(k[0]) + ", mode: " + ("auto mode" if k[1] else "repeating mode"))
        for p in plains:
            ciphers.append(vigenere(p,k[0],k[1]))
        ciphers.append("\n")
    write_file("vigenere_cipher.txt", ciphers)

    keys = ["RATS", "ARCHANGEL"]
    cipher(keys, "playfair_plain.txt", "playfair_cipher.txt", play_fair)
    keys = ["SPARTANS"]
    cipher(keys, "vernam_plain.txt", "vernam_cipher.txt", vernam)

    key = np.array([[5,17],[8,3]])
    cipher(key, "hill_plain_2x2.txt", "hill_cipher_2x2.txt", hill)

    key = np.array([[2, 4, 12], [9, 1, 6], [7, 5, 3]])
    cipher(key, "hill_plain_3x3.txt", "hill_cipher_3x3.txt", hill)