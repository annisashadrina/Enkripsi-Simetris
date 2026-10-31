"""Tugas Praktikum Keamanan Siber: Enkripsi dan Dekripsi Teks menggunakan AES-256-GCM
Nama : Annisa Nur Shadrina
NIM  : 103072400134
Topik: Symmetric Cryptography - AES-GCM
"""
import base64
import hashlib
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag


def turunkan_kunci(kata_sandi: str, salt: bytes) -> bytes:
    """Kunci 32 byte untuk AES-256 dari kata sandi dan salt menggunakan PBKDF2-HMAC-SHA256."""
    return hashlib.pbkdf2_hmac(
        "sha256", kata_sandi.encode("utf-8"), salt, 200_000, dklen=32
    )


def enkripsi(teks: str, kata_sandi: str) -> str:
    """Input: dua teks (plaintext dan kata sandi).
    Output: satu teks ciphertext yang dikodekan dengan Base64.
    
    Format payload biner: salt (16 byte) + nonce (12 byte) + ciphertext & auth tag.
    """
    # 1. Buat salt acak 16 byte dan nonce acak 12 byte
    salt = os.urandom(16)
    nonce = os.urandom(12)
    
    # 2. Buat kunci AES-256 (32 byte) dengan turunkan_kunci()
    kunci = turunkan_kunci(kata_sandi, salt)
    
    # 3. Enkripsi teks UTF-8 menggunakan AESGCM (otomatis menyertakan authentication tag 16 byte)
    aesgcm = AESGCM(kunci)
    ciphertext_with_tag = aesgcm.encrypt(nonce, teks.encode("utf-8"), None)
    
    # 4. Gabungkan salt + nonce + ciphertext (termasuk tag)
    payload = salt + nonce + ciphertext_with_tag
    
    # 5. Encode gabungan payload dengan Base64, lalu kembalikan sebagai string
    return base64.b64encode(payload).decode("ascii")


def dekripsi(ciphertext_b64: str, kata_sandi: str) -> str:
    """Input: dua teks (ciphertext Base64 dan kata sandi).
    Output: plaintext asli atau membangkitkan exception yang ditangani oleh pemanggil.
    """
    # 1. Decode ciphertext_b64 dari Base64 menjadi bytes
    try:
        data = base64.b64decode(ciphertext_b64, validate=True)
    except Exception as exc:
        raise ValueError("Format Base64 tidak valid.") from exc
    
    # Validasi panjang minimum: salt(16) + nonce(12) + tag(16) = 44 bytes
    if len(data) < 44:
        raise ValueError("Data ciphertext terlalu pendek atau rusak.")
    
    # 2. Pisahkan salt (16 byte), nonce (12 byte), dan sisa ciphertext beserta tag
    salt = data[:16]
    nonce = data[16:28]
    ciphertext_with_tag = data[28:]
    
    # 3. Buat kembali kunci dengan turunkan_kunci()
    kunci = turunkan_kunci(kata_sandi, salt)
    
    # 4. Dekripsi AESGCM, lalu decode UTF-8 menjadi teks
    aesgcm = AESGCM(kunci)
    plaintext_bytes = aesgcm.decrypt(nonce, ciphertext_with_tag, None)
    return plaintext_bytes.decode("utf-8")


def main() -> None:
    while True:
        print("\n=== ENKRIPSI SIMETRIS (AES-GCM) ===")
        print("1. Enkripsi teks")
        print("2. Dekripsi teks")
        print("0. Keluar")
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "0":
            print("Program selesai.")
            break
        if pilihan not in {"1", "2"}:
            print("Pilihan menu tidak valid.")
            continue
        
        pesan = input("Masukkan plaintext: " if pilihan == "1" else "Masukkan ciphertext Base64: ")
        kata_sandi = input("Masukkan kata sandi: ")
        if not kata_sandi:
            print("Kata sandi tidak boleh kosong.")
            continue
        
        try:
            if pilihan == "1":
                hasil_b64 = enkripsi(pesan, kata_sandi)
                print("Ciphertext (Base64):", hasil_b64)
            else:
                hasil_plain = dekripsi(pesan, kata_sandi)
                print("Plaintext:", hasil_plain)
        except (InvalidTag, ValueError, UnicodeDecodeError):
            print("Dekripsi gagal: kata sandi atau ciphertext tidak sesuai.")
        except NotImplementedError as exc:
            print(exc)


if __name__ == "__main__":
    main()
