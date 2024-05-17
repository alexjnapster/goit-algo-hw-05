class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        key_hash = self.hash_function(key)
        key_value = [key, value]

        if self.table[key_hash] is None:
            self.table[key_hash] = list([key_value])
            return True
        else:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        key_hash = self.hash_function(key)
        if self.table[key_hash] is not None:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    def delete(self, key):
        key_hash = self.hash_function(key)
        if self.table[key_hash] is not None:
            for i in range(len(self.table[key_hash])):
                if self.table[key_hash][i][0] == key:
                    self.table[key_hash].pop(i)
                    return True
        return False

    def binary_search(arr, x):
        low = 0
        high = len(arr) - 1
        iterations = 0

        while low <= high:
            iterations += 1
            mid = (high + low) // 2

            if arr[mid] < x:
                low = mid + 1
            elif arr[mid] > x:
                high = mid - 1
            else:
                return (iterations, arr[mid])

        if low < len(arr):
            return (iterations, arr[low])
        else:
            return (iterations, None)

    def KMPSearch(pat, txt):
        M = len(pat)
        N = len(txt)
        lps = [0] * M
        j = 0  # index for pat[]
        computeLPSArray(pat, M, lps)
        i = 0  # index for txt[]
        while i < N:
            if pat[j] == txt[i]:
                i += 1
                j += 1
            if j == M:
                return i - j
            elif i < N and pat[j] != txt[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        return -1

    def computeLPSArray(pat, M, lps):
        length = 0
        lps[0] = 0
        i = 1
        while i < M:
            if pat[i] == pat[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

    def BMSearch(pat, txt):
        m = len(pat)
        n = len(txt)
        badChar = [-1] * 256
        badCharHeuristic(pat, m, badChar)
        s = 0
        while (s <= n - m):
            j = m - 1
            while j >= 0 and pat[j] == txt[s + j]:
                j -= 1
            if j < 0:
                return s
            else:
                s += max(1, j - badChar[ord(txt[s + j])])
        return -1

    def badCharHeuristic(string, size, badChar):
        for i in range(size):
            badChar[ord(string[i])] = i

    def RKSearch(pat, txt, q=101):
        d = 256
        m = len(pat)
        n = len(txt)
        p = 0
        t = 0
        h = 1
        for i in range(m - 1):
            h = (h * d) % q
        for i in range(m):
            p = (d * p + ord(pat[i])) % q
            t = (d * t + ord(txt[i])) % q
        for i in range(n - m + 1):
            if p == t:
                for j in range(m):
                    if txt[i + j] != pat[j]:
                        break
                j += 1
                if j == m:
                    return i
            if i < n - m:
                t = (d * (t - ord(txt[i]) * h) + ord(txt[i + m])) % q
                if t < 0:
                    t = t + q
        return -1

import timeit

# Зчитування файлів
with open('1.txt', 'r', encoding='utf-8') as file:
    text1 = file.read()

with open('2.txt', 'r', encoding='utf-8') as file:
    text2 = file.read()

# Підрядки для пошуку
existing_substring = "алгоритм"
non_existing_substring = "невідомий"

# Вимірювання для text1
print("Text 1, existing substring:")
print(timeit.timeit(lambda: KMPSearch(existing_substring, text1), number=1000))
print(timeit.timeit(lambda: BMSearch(existing_substring, text1), number=1000))
print(timeit.timeit(lambda: RKSearch(existing_substring, text1), number=1000))

print("Text 1, non-existing substring:")
print(timeit.timeit(lambda: KMPSearch(non_existing_substring, text1), number=1000))
print(timeit.timeit(lambda: BMSearch(non_existing_substring, text1), number=1000))
print(timeit.timeit(lambda: RKSearch(non_existing_substring, text1), number=1000))

# Вимірювання для text2
print("Text 2, existing substring:")
print(timeit.timeit(lambda: KMPSearch(existing_substring, text2), number=1000))
print(timeit.timeit(lambda: BMSearch(existing_substring, text2), number=1000))
print(timeit.timeit(lambda: RKSearch(existing_substring, text2), number=1000))

print("Text 2, non-existing substring:")
print(timeit.timeit(lambda: KMPSearch(non_existing_substring, text2), number=1000))
print(timeit.timeit(lambda: BMSearch(non_existing_substring, text2), number=1000))
print(timeit.timeit(lambda: RKSearch(non_existing_substring, text2), number=1000))