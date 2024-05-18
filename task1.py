import requests
import timeit

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        key_hash = self.hash_function(key)
        key_value = [key, value]

        if not self.table[key_hash]:
            self.table[key_hash].append(key_value)
        else:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    break
            else:
                self.table[key_hash].append(key_value)

    def get(self, key):
        key_hash = self.hash_function(key)
        for pair in self.table[key_hash]:
            if pair[0] == key:
                return pair[1]
        return None

    def delete(self, key):
        key_hash = self.hash_function(key)
        for i, pair in enumerate(self.table[key_hash]):
            if pair[0] == key:
                self.table[key_hash].pop(i)
                return True
        return False

# Приклад використання HashTable
H = HashTable(5)
H.insert("apple", 10)
H.insert("orange", 20)
H.insert("banana", 30)

print(H.get("apple"))   # Виведе: 10
H.delete("apple")
print(H.get("apple"))   # Виведе: None

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

# Приклад використання двійкового пошуку
arr = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7]
x = 5
result = binary_search(arr, x)
print(f"Ітерації: {result[0]}, Верхня межа: {result[1]}")  # Виведе: (2, 5.5)

def KMPSearch(pat, txt):
    M = len(pat)
    N = len(txt)
    lps = [0] * M
    j = 0  # індекс для pat[]
    computeLPSArray(pat, M, lps)
    i = 0  # індекс для txt[]
    while i < N:
        if pat[j] == txt[i]:
            i += 1
            j += 1
        if j == M:
            return i - j
        elif i < N and pat[j] != txt[i]:
            if j != 0:
                j = lps[j-1]
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
                length = lps[length-1]
            else:
                lps[i] = 0
                i += 1

def BMSearch(pat, txt):
    m = len(pat)
    n = len(txt)
    badChar = [-1]*256
    badCharHeuristic(pat, m, badChar)
    s = 0
    while(s <= n-m):
        j = m-1
        while j >= 0 and pat[j] == txt[s+j]:
            j -= 1
        if j < 0:
            return s
        else:
            s += max(1, j - badChar[ord(txt[s+j])])
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
    for i in range(m-1):
        h = (h*d) % q
    for i in range(m):
        p = (d*p + ord(pat[i])) % q
        t = (d*t + ord(txt[i])) % q
    for i in range(n-m+1):
        if p == t:
            for j in range(m):
                if txt[i+j] != pat[j]:
                    break
            j += 1
            if j == m:
                return i
        if i < n-m:
            t = (d*(t-ord(txt[i])*h) + ord(txt[i+m])) % q
            if t < 0:
                t = t+q
    return -1

def download_file_from_google_drive(file_id):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Не вдалося завантажити файл з Google Drive. Статус: {response.status_code}")

# Зчитування файлів з Google Drive
text1 = download_file_from_google_drive('18_R5vEQ3eDuy2VdV3K5Lu-R-B-adxXZh')
text2 = download_file_from_google_drive('13hSt4JkJc11nckZZz2yoFHYL89a4XkMZ')

# Підрядки для пошуку
existing_substring = "алгоритм"
non_existing_substring = "невідомий"

# Функція для вимірювання часу виконання алгоритмів пошуку
def measure_time(text, substring):
    times = {
        'KMP': timeit.timeit(lambda: KMPSearch(substring, text), number=1000),
        'BM': timeit.timeit(lambda: BMSearch(substring, text), number=1000),
        'RK': timeit.timeit(lambda: RKSearch(substring, text), number=1000)
    }
    return times

# Вимірювання часу для text1
times_text1_existing = measure_time(text1, existing_substring)
times_text1_non_existing = measure_time(text1, non_existing_substring)

# Вимірювання часу для text2
times_text2_existing = measure_time(text2, existing_substring)
times_text2_non_existing = measure_time(text2, non_existing_substring)

# Виведення результатів
print("Текст 1, існуючий підрядок:", times_text1_existing)
print("Текст 1, неіснуючий підрядок:", times_text1_non_existing)
print("Текст 2, існуючий підрядок:", times_text2_existing)
print("Текст 2, неіснуючий підрядок:", times_text2_non_existing)

# Визначення найшвидшого алгоритму для кожного тексту окремо та в цілому
def find_fastest(times):
    return min(times, key=times.get)

fastest_text1_existing = find_fastest(times_text1_existing)
fastest_text1_non_existing = find_fastest(times_text1_non_existing)
fastest_text2_existing = find_fastest(times_text2_existing)
fastest_text2_non_existing = find_fastest(times_text2_non_existing)

print(f"Найшвидший алгоритм для тексту 1 (існуючий підрядок): {fastest_text1_existing}")
print(f"Найшвидший алгоритм для тексту 1 (неіснуючий підрядок): {fastest_text1_non_existing}")
print(f"Найшвидший алгоритм для тексту 2 (існуючий підрядок): {fastest_text2_existing}")
print(f"Найшвидший алгоритм для тексту 2 (неіснуючий підрядок): {fastest_text2_non_existing}")

# Визначення найшвидшого алгоритму в цілому
overall_times = {
    'KMP': times_text1_existing['KMP'] + times_text1_non_existing['KMP'] + times_text2_existing['KMP'] + times_text2_non_existing['KMP'],
    'BM': times_text1_existing['BM'] + times_text1_non_existing['BM'] + times_text2_existing['BM'] + times_text2_non_existing['BM'],
    'RK': times_text1_existing['RK'] + times_text1_non_existing['RK'] + times_text2_existing['RK'] + times_text2_non_existing['RK']
}

fastest_overall = find_fastest(overall_times)
print(f"Найшвидший алгоритм в цілому: {fastest_overall}")
