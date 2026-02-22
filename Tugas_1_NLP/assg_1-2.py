# Meminta input nilai
nilai = float(input("Masukkan nilai Anda: "))

# Logika penentuan nilai huruf
if nilai >= 81:
    nilai_huruf = 'A'
elif nilai >= 76:
    nilai_huruf = 'B'
elif nilai >= 66:
    nilai_huruf = 'C'
elif nilai >= 55:
    nilai_huruf = 'D'
else: # Kondisi untuk di bawah 55
    nilai_huruf = 'E'

print(f"Nilai angka: {nilai}")
print(f"Nilai huruf: {nilai_huruf}")