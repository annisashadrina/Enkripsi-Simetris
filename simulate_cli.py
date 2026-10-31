import subprocess
import re

p1 = subprocess.Popen(
    ["python", r"D:\KULIAH\SEMESTER 5\CYBERSEC\Enkripsi Simetris\Annisa Nur Shadrina_103072400134_AES.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    encoding="utf-8"
)

# Simulasi 1: Enkripsi teks
inputs_1 = "1\nHalo, Informatika!\nRahasia123\n0\n"
out1, _ = p1.communicate(input=inputs_1)
print("=== SESI TERMINAL 1 (ENKRIPSI) ===")
print(out1)

# Ekstrak ciphertext dari output
match = re.search(r"Ciphertext \(Base64\):\s*(\S+)", out1)
assert match is not None
ciphertext = match.group(1)

# Simulasi 2: Dekripsi Sukses & Dekripsi Gagal
p2 = subprocess.Popen(
    ["python", r"D:\KULIAH\SEMESTER 5\CYBERSEC\Enkripsi Simetris\Annisa Nur Shadrina_103072400134_AES.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    encoding="utf-8"
)

inputs_2 = f"2\n{ciphertext}\nRahasia123\n2\n{ciphertext}\nPasswordSalah\n0\n"
out2, _ = p2.communicate(input=inputs_2)
print("=== SESI TERMINAL 2 (DEKRIPSI SUKSES & GAGAL) ===")
print(out2)

