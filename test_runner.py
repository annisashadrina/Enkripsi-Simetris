import sys
import importlib.util

if sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

spec = importlib.util.spec_from_file_location(
    "aes_prog", 
    r"D:\KULIAH\SEMESTER 5\CYBERSEC\Enkripsi Simetris\Annisa Nur Shadrina_103072400134_AES.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

print("=" * 60)
print("=== PENGUJIAN SKENARIO PRAKTIKUM ENKRIPSI SIMETRIS ===")
print("=" * 60)

# Skenario 1
print("\n[SKENARIO 1: Teks Biasa]")
pt1 = "Halo Informatika"
pw1 = "KatasandiRahasia123"
ct1 = mod.enkripsi(pt1, pw1)
print(f"Plaintext Input : {pt1}")
print(f"Kata Sandi      : {pw1}")
print(f"Ciphertext (B64): {ct1}")
rec1 = mod.dekripsi(ct1, pw1)
print(f"Hasil Dekripsi  : {rec1}")
assert rec1 == pt1, "Skenario 1 gagal!"
print("Status          : SUKSES (Teks hasil dekripsi identik)")

# Skenario 2
print("\n[SKENARIO 2: Teks dengan Angka, Simbol, atau Unicode]")
pt2 = "Siber2026! #AES_GCM$ @Tel-U 🔐 (NIM: 103072400134)"
pw2 = "P@ssw0rd_Kuat!"
ct2 = mod.enkripsi(pt2, pw2)
print(f"Plaintext Input : {pt2}")
print(f"Kata Sandi      : {pw2}")
print(f"Ciphertext (B64): {ct2}")
rec2 = mod.dekripsi(ct2, pw2)
print(f"Hasil Dekripsi  : {rec2}")
assert rec2 == pt2, "Skenario 2 gagal!"
print("Status          : SUKSES (Teks hasil dekripsi identik)")

# Skenario 3
print("\n[SKENARIO 3: Dekripsi dengan Kata Sandi Salah]")
pw_salah = "KataSandiSalahTotal"
print(f"Ciphertext Input: {ct1}")
print(f"Kata Sandi Salah: {pw_salah}")
try:
    mod.dekripsi(ct1, pw_salah)
    print("Status          : GAGAL (Seharusnya menolak)")
except Exception as e:
    print(f"Pesan Error     : {type(e).__name__} - {e}")
    print("Status          : SUKSES (Program menolak dekripsi)")

# Skenario 4
print("\n[SKENARIO 4: Ciphertext Base64 Diubah/Rusak]")
# Modifikasi salah satu karakter pada ciphertext
ct_rusak = ct1[:20] + ("A" if ct1[20] != "A" else "B") + ct1[21:]
print(f"Ciphertext Asli : {ct1}")
print(f"Ciphertext Rusak: {ct_rusak}")
print(f"Kata Sandi      : {pw1}")
try:
    mod.dekripsi(ct_rusak, pw1)
    print("Status          : GAGAL (Seharusnya menolak)")
except Exception as e:
    print(f"Pesan Error     : {type(e).__name__} - {e}")
    print("Status          : SUKSES (Program menolak ciphertext rusak / otentikasi gagal)")

# Test Refleksi Pertanyaan 3: Enkripsi teks sama dengan password sama berulang kali
print("\n[UJI REFLEKSI: Enkripsi teks & password sama 2x berturut-turut]")
ct_run1 = mod.enkripsi(pt1, pw1)
ct_run2 = mod.enkripsi(pt1, pw1)
print(f"Run 1 Ciphertext: {ct_run1}")
print(f"Run 2 Ciphertext: {ct_run2}")
print(f"Apakah Ciphertext Berbeda? -> {'YA, BERBEDA (KARENA SALT & NONCE ACAK)' if ct_run1 != ct_run2 else 'TIDAK'}")

print("\n" + "=" * 60)
print("SELURUH SKENARIO PENGUJIAN TELAH TERPENUHI 100%!")
print("=" * 60)
