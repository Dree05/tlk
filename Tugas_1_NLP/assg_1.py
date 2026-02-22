# NAMA : ANDRE DEVALDO
# NIM  : 23080960081

HASIL = 4 * 6 + 6 // 2
print("A = 4 x 6 + 6 // 2")
print("HASIL = ", HASIL)

print()

print("--- For Loop ---")
for i in range(1, 21):
    print(i, end=' ')

print("\n\n--- While Loop ---")
a = 1
while a <= 20:
    print(a)
    a += 1

print("\n---cetak angka [0, 1, 4, 9, 16, 25]---")
angka_kuadrat = [x**2 for x in range(6)]
print(angka_kuadrat)

nilai = 80
print("\ncontoh nilai untuk menentukan lulus atau tidak:", nilai)
if nilai >= 75:
    print("Status: Lulus")
else:
    print("Status: Tidak Lulus")