import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = Document()

# Set standard margins (1 inch / 2.54 cm)
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Helper styles
def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def add_header(title, subtitle=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title)
    run.font.name = 'Calibri'
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 51, 102)
    
    if subtitle:
        p2 = doc.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run2 = p2.add_run(subtitle)
        run2.font.name = 'Calibri'
        run2.font.size = Pt(13)
        run2.font.italic = True
        run2.font.color.rgb = RGBColor(100, 100, 100)

add_header(
    "LAPORAN PRAKTIKUM KEAMANAN SIBER",
    "Implementasi Enkripsi dan Dekripsi Simetris dengan AES-256-GCM"
)

# Identity Table
table_identitas = doc.add_table(rows=4, cols=2)
table_identitas.alignment = WD_TABLE_ALIGNMENT.CENTER
identitas_data = [
    ("Nama Mahasiswa", "Annisa Nur Shadrina"),
    ("NIM", "103072400134"),
    ("Mata Kuliah", "Keamanan Siber"),
    ("Topik Praktikum", "Symmetric Cryptography - AES-256-GCM")
]
for idx, (label, val) in enumerate(identitas_data):
    cell_lbl = table_identitas.cell(idx, 0)
    cell_val = table_identitas.cell(idx, 1)
    cell_lbl.text = label
    cell_lbl.paragraphs[0].runs[0].font.bold = True
    cell_lbl.paragraphs[0].runs[0].font.name = 'Calibri'
    cell_val.text = val
    cell_val.paragraphs[0].runs[0].font.name = 'Calibri'
    set_cell_background(cell_lbl, "EBF1F5")
    set_cell_background(cell_val, "F9FAFB")

doc.add_paragraph()

# 1. Tujuan Praktikum
h1 = doc.add_heading("1. Tujuan Praktikum", level=1)
h1.runs[0].font.color.rgb = RGBColor(0, 51, 102)
p_tujuan = doc.add_paragraph(
    "Tujuan dari praktikum ini adalah untuk:\n"
    "1. Memahami konsep dasar plaintext, ciphertext, dan kunci rahasia simetris.\n"
    "2. Mengimplementasikan fitur enkripsi dan dekripsi teks berbasis CLI menggunakan algoritma AES-256-GCM.\n"
    "3. Memahami dan memverifikasi peran Kunci Simetris, Salt (PBKDF2), dan Nonce/IV dalam menjamin kerahasiaan (*confidentiality*) dan integritas (*integrity*).\n"
    "4. Menguji ketahanan program terhadap penanganan kunci yang salah atau ciphertext yang rusak tanpa menampilkan traceback mentah."
)

# 2. Penjelasan Peran Kunci, Salt, dan Nonce
h2 = doc.add_heading("2. Penjelasan Peran Kunci, Salt, dan Nonce", level=1)
h2.runs[0].font.color.rgb = RGBColor(0, 51, 102)

p_kunci = doc.add_paragraph()
r_k1 = p_kunci.add_run("A. Kunci Rahasia Simetris (AES-256 Key, 32 Byte):\n")
r_k1.bold = True
p_kunci.add_run(
    "Kunci simetris adalah parameter rahasia bersama yang digunakan oleh algoritma AES-256 untuk melakukan proses "
    "transformasi matematis (substitusi S-Box, pergeseran baris, pencampuran kolom, dan penambahan subkunci ronde). "
    "Pada kriptografi simetris, kunci yang sama wajib digunakan baik saat mengenkripsi plaintext maupun saat memulihkan "
    "(mendekripsi) ciphertext. Pada implementasi ini, kunci 256-bit (32 byte) tidak diinputkan mentah oleh pengguna, "
    "melainkan diturunkan secara aman dari kata sandi (*passphrase*) pengguna menggunakan fungsi derivasi kunci PBKDF2-HMAC-SHA256."
)

p_salt = doc.add_paragraph()
r_s1 = p_salt.add_run("B. Salt (16 Byte Acak):\n")
r_s1.bold = True
p_salt.add_run(
    "Salt adalah untaian byte acak yang dibangkitkan secara kriptografis (os.urandom(16)) dan dicampurkan bersama kata sandi "
    "pada saat proses derivasi kunci dengan PBKDF2-HMAC-SHA256 (sebanyak 200.000 iterasi). Salt berperan penting dalam:\n"
    "• Mencegah serangan kamus terkomputasi sebelumnya (*Precomputed Dictionary Attack*) dan tabel pelangi (*Rainbow Table*).\n"
    "• Memastikan bahwa kata sandi yang sama yang digunakan oleh dua pengguna (atau pada dua sesi berbeda) akan menghasilkan "
    "kunci enkripsi biner 32-byte yang sama sekali berbeda.\n"
    "• Salt bukan rahasia sehingga aman digabungkan secara terbuka bersama ciphertext."
)

p_nonce = doc.add_paragraph()
r_n1 = p_nonce.add_run("C. Nonce / Initialization Vector (12 Byte Acak):\n")
r_n1.bold = True
p_nonce.add_run(
    "Nonce (*Number used ONCE*) adalah nilai acak 12 byte (standar rekomendasi NIST SP 800-38D untuk AES-GCM) yang wajib unik "
    "untuk setiap kali operasi enkripsi dijalankan. Nonce berfungsi sebagai inisialisasi counter pada Galois/Counter Mode. "
    "Peran utama Nonce adalah:\n"
    "• Memastikan sifat *semantic security* (probabilistic encryption): teks plaintext yang sama dan kata sandi yang sama tidak "
    "akan pernah menghasilkan ciphertext yang sama.\n"
    "• Mencegah penyerang mendeteksi kesamaan isi pesan atau melakukan serangan pengulangan (*Replay Attack*).\n"
    "• Nonce bukan rahasia dan disertakan di bagian depan payload untuk digunakan kembali saat proses dekripsi."
)

p_payload = doc.add_paragraph()
r_p1 = p_payload.add_run("D. Struktur Payload Output Base64:\n")
r_p1.bold = True
p_payload.add_run(
    "Agar data biner mentah dapat disalin dan ditampilkan di terminal tanpa risiko korupsi karakter, seluruh komponen biner "
    "digabungkan menjadi satu kesatuan sebelum di-encode dengan Base64:\n"
    "Payload = Salt (16 B) + Nonce (12 B) + Ciphertext + Authentication Tag (16 B)\n"
    "Panjang minimum biner sebelum di-decode adalah 44 byte."
)

# 3. Fitur dan Alur Program
h3 = doc.add_heading("3. Fitur dan Alur Program", level=1)
h3.runs[0].font.color.rgb = RGBColor(0, 51, 102)
p_fitur = doc.add_paragraph(
    "Aplikasi diimplementasikan dalam berkas 'Annisa Nur Shadrina_103072400134_AES.py' berbasis CLI terminal interaktif dengan 2 menu utama:\n"
    "1. Menu 1 (Enkripsi): Menerima input string plaintext dan kata sandi, kemudian menghasilkan string ciphertext Base64.\n"
    "2. Menu 2 (Dekripsi): Menerima input ciphertext Base64 dan kata sandi, kemudian memvalidasi integritas data dan mengembalikan plaintext asli.\n"
    "3. Menu 0 (Keluar): Menutup program terminal secara aman.\n\n"
    "Penanganan Error: Program secara eksplisit menangani eksepsi InvalidTag, ValueError, dan UnicodeDecodeError tanpa mencetak traceback error ke pengguna."
)

# 4. Hasil Pengujian (4 Skenario Wajib)
h4 = doc.add_heading("4. Hasil Pengujian 4 Skenario Wajib", level=1)
h4.runs[0].font.color.rgb = RGBColor(0, 51, 102)

p_intro_uji = doc.add_paragraph(
    "Berikut adalah dokumentasi hasil pengujian langsung program terhadap keempat skenario wajib yang ditentukan dalam modul tugas:"
)

# Table 4 scenarios
table_uji = doc.add_table(rows=5, cols=4)
table_uji.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["No.", "Skenario Pengujian", "Hasil yang Diharapkan", "Status Pengujian"]
for col_idx, h_text in enumerate(headers):
    cell = table_uji.cell(0, col_idx)
    cell.text = h_text
    cell.paragraphs[0].runs[0].font.bold = True
    cell.paragraphs[0].runs[0].font.name = 'Calibri'
    set_cell_background(cell, "003366")
    cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

scenarios = [
    ("1", "Teks biasa:\n\"Halo Informatika\"", "Teks hasil dekripsi identik dengan input asli.", "SUKSES / PASSED\n(Identik 100%)"),
    ("2", "Teks dengan angka, simbol, dan Unicode:\n\"Siber2026! #AES_GCM$ @Tel-U 🔐 (NIM: 103072400134)\"", "Teks hasil dekripsi tetap identik secara utuh.", "SUKSES / PASSED\n(Identik 100%)"),
    ("3", "Dekripsi dengan kata sandi salah:\nKata sandi keliru diinputkan", "Program menolak dekripsi dan menampilkan pesan kesalahan ramah.", "SUKSES / PASSED\n(Ditolak oleh InvalidTag)"),
    ("4", "Ciphertext Base64 diubah/rusak:\nKarakter ciphertext dimodifikasi", "Program menolak dekripsi dan tidak menghasilkan data sampah.", "SUKSES / PASSED\n(Otentikasi tag gagal)")
]

for row_idx, (no, sken, eksp, stat) in enumerate(scenarios, start=1):
    table_uji.cell(row_idx, 0).text = no
    table_uji.cell(row_idx, 1).text = sken
    table_uji.cell(row_idx, 2).text = eksp
    table_uji.cell(row_idx, 3).text = stat
    for c_i in range(4):
        table_uji.cell(row_idx, c_i).paragraphs[0].runs[0].font.name = 'Calibri'
        table_uji.cell(row_idx, c_i).paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(table_uji.cell(row_idx, c_i), "F7F9FA" if row_idx % 2 == 1 else "FFFFFF")

doc.add_paragraph()

# Rincian Terminal Output Log
h4_1 = doc.add_heading("Log Output Eksekusi Terminal", level=2)
h4_1.runs[0].font.color.rgb = RGBColor(0, 51, 102)

log_text = (
    "=== LOG PENGUJIAN OTOMATIS (test_runner.py) ===\n\n"
    "[SKENARIO 1: Teks Biasa]\n"
    "Plaintext Input : Halo Informatika\n"
    "Kata Sandi      : KatasandiRahasia123\n"
    "Ciphertext (B64): gxqrYfPBjEwW4qtabtY49i6JjztLx7Yeps3jpVy6HOkYIXBOwGzY/K97ZFX5EKGjA71dIH72Ho4SC8bj\n"
    "Hasil Dekripsi  : Halo Informatika\n"
    "Status          : SUKSES (Teks hasil dekripsi identik)\n\n"
    "[SKENARIO 2: Teks Angka, Simbol, Unicode]\n"
    "Plaintext Input : Siber2026! #AES_GCM$ @Tel-U 🔐 (NIM: 103072400134)\n"
    "Kata Sandi      : P@ssw0rd_Kuat!\n"
    "Ciphertext (B64): 60zjdqKyqnCMZSWCIYfQhxkSvcUgyafl7M3Z0YCxVML3GHrMhBeh89Z7YdgODGkrkfu6shaJepdPURwTMOHlssjUdL5xpQud6v890IuwJqFvn+MFXoCqZYloeJH9rL2P\n"
    "Hasil Dekripsi  : Siber2026! #AES_GCM$ @Tel-U 🔐 (NIM: 103072400134)\n"
    "Status          : SUKSES (Teks hasil dekripsi identik)\n\n"
    "[SKENARIO 3: Kata Sandi Salah]\n"
    "Ciphertext Input: gxqrYfPBjEwW4qtabtY49i6JjztLx7Yeps3jpVy6HOkYIXBOwGzY/K97ZFX5EKGjA71dIH72Ho4SC8bj\n"
    "Kata Sandi Salah: KataSandiSalahTotal\n"
    "Hasil Tangkapan : InvalidTag (Dekripsi gagal: kata sandi atau ciphertext tidak sesuai.)\n"
    "Status          : SUKSES (Program menolak dekripsi secara aman)\n\n"
    "[SKENARIO 4: Ciphertext Rusak]\n"
    "Ciphertext Rusak: gxqrYfPBjEwW4qtabtY4Ai6JjztLx7Yeps3jpVy6HOkYIXBOwGzY/K97ZFX5EKGjA71dIH72Ho4SC8bj\n"
    "Kata Sandi      : KatasandiRahasia123\n"
    "Hasil Tangkapan : InvalidTag (Dekripsi gagal: kata sandi atau ciphertext tidak sesuai.)\n"
    "Status          : SUKSES (Program menolak ciphertext yang dimanipulasi)"
)
p_box = doc.add_paragraph()
r_box = p_box.add_run(log_text)
r_box.font.name = 'Consolas'
r_box.font.size = Pt(8.5)
r_box.font.color.rgb = RGBColor(30, 30, 30)

# Section for Screenshots
h4_2 = doc.add_heading("Tangkapan Layar Pengujian (Screenshots)", level=2)
h4_2.runs[0].font.color.rgb = RGBColor(0, 51, 102)

p_sc1 = doc.add_paragraph()
r_sc1_lbl = p_sc1.add_run("[Gambar 1: Screenshot Fitur 1 - Enkripsi Teks]\n")
r_sc1_lbl.bold = True
r_sc1_desc = p_sc1.add_run("(Silakan lampirkan tangkapan layar terminal saat menjalankan menu 1 - Enkripsi teks)")
r_sc1_desc.italic = True

p_sc2 = doc.add_paragraph()
r_sc2_lbl = p_sc2.add_run("[Gambar 2: Screenshot Fitur 2 - Dekripsi Teks Sukses & Gagal]\n")
r_sc2_lbl.bold = True
r_sc2_desc = p_sc2.add_run("(Silakan lampirkan tangkapan layar terminal saat menjalankan menu 2 - Dekripsi dengan password benar vs salah)")
r_sc2_desc.italic = True

# 5. Jawaban Pertanyaan Refleksi
h5 = doc.add_heading("5. Jawaban Pertanyaan Refleksi", level=1)
h5.runs[0].font.color.rgb = RGBColor(0, 51, 102)

# Refleksi 1
p_q1 = doc.add_paragraph()
r_q1_t = p_q1.add_run("Pertanyaan 1: Mengapa kata sandi yang sama diperlukan ketika melakukan dekripsi?\n")
r_q1_t.bold = True
p_q1.add_run(
    "Jawaban:\n"
    "Kriptografi simetris (seperti AES) beroperasi menggunakan prinsip kunci bersama (shared secret key). "
    "Operasi matematis pada proses enkripsi dan dekripsi bersifat berbalikan (invers) dan hanya dapat ditutup serta dibuka "
    "oleh kunci biner yang sama persis. Pada implementasi ini, kunci 256-bit diturunkan melalui fungsi PBKDF2 dari kata sandi "
    "dan salt. Karena sifat fungsi hash kriptografis yang memiliki efek longsoran (avalanche effect), perbedaan sekecil satu "
    "karakter saja pada kata sandi akan menghasilkan kunci biner 32-byte yang berbeda secara drastis. Kunci yang keliru tidak "
    "akan mampu membalikkan permutasi AES dan akan langsung gagal saat validasi Authentication Tag pada mode GCM. Oleh karena itu, "
    "kata sandi yang sama persis adalah syarat mutlak untuk meregenerasi kunci simetris yang valid."
)

# Refleksi 2
p_q2 = doc.add_paragraph()
r_q2_t = p_q2.add_run("Pertanyaan 2: Mengapa ciphertext perlu dikonversi ke Base64 ketika ditampilkan sebagai teks?\n")
r_q2_t.bold = True
p_q2.add_run(
    "Jawaban:\n"
    "Hasil keluaran enkripsi AES-GCM (yang digabungkan dengan salt dan nonce) berupa rangkaian byte biner mentah (raw bytes) "
    "dengan rentang nilai 0x00 hingga 0xFF. Sebagian besar nilai biner tersebut bukan merupakan karakter teks yang dapat dicetak "
    "(non-printable characters), melainkan kode kontrol terminal (seperti NULL, newline, EOF, bell) dan byte yang tidak sesuai "
    "dengan format standar teks UTF-8 atau ASCII. Jika byte biner ini dipaksa dicetak langsung ke terminal atau disalin-tempel, "
    "data akan terpotong, mengalami korupsi nilai byte, atau menyebabkan kegagalan decoding. "
    "Base64 mengonversi setiap 3 byte biner menjadi 4 karakter ASCII yang aman (A-Z, a-z, 0-9, +, /, =), sehingga payload "
    "dapat ditampilkan di terminal, disalin ke clipboard, dan dikirimkan tanpa risiko kerusakan data."
)

# Refleksi 3
p_q3 = doc.add_paragraph()
r_q3_t = p_q3.add_run("Pertanyaan 3: Mengapa proses enkripsi dengan plaintext dan kata sandi yang sama dapat menghasilkan ciphertext berbeda?\n")
r_q3_t.bold = True
p_q3.add_run(
    "Jawaban:\n"
    "Hal ini disebabkan oleh penerapan Salt acak (16 byte) dan Nonce acak (12 byte) baru yang selalu dibangkitkan secara independen "
    "menggunakan 'os.urandom()' setiap kali fungsi enkripsi dijalankan:\n"
    "1. Peran Salt Acak: Walaupun kata sandi yang diketik sama, salt yang berbeda menyebabkan fungsi PBKDF2 menghasilkan kunci AES 256-bit "
    "yang berbeda secara unik pada setiap eksekusi.\n"
    "2. Peran Nonce Acak: Pada mode AES-GCM, nonce berfungsi sebagai titik awal counter blok. Nilai counter yang unik memastikan aliran kunci "
    "(keystream) yang dihasilkan selalu berbeda, sehingga ciphertext yang dihasilkan dari plaintext yang sama akan selalu berubah secara acak.\n"
    "Sifat ini merupakan standar keamanan modern (Semantic Security / Probabilistic Encryption) untuk mencegah serangan analisis pola/frekuensi, "
    "mencegah penyerang mengetahui apakah dua pesan terenkripsi memiliki isi yang sama, serta mencegah serangan Rainbow Table dan Replay Attack."
)

# 6. Kesimpulan
h6 = doc.add_heading("6. Kesimpulan", level=1)
h6.runs[0].font.color.rgb = RGBColor(0, 51, 102)
p_kesimpulan = doc.add_paragraph(
    "1. Algoritma AES-256-GCM berhasil diimplementasikan secara optimal pada program terminal Python berbasis spesifikasi modul tugas.\n"
    "2. Penggunaan PBKDF2-HMAC-SHA256 (200.000 iterasi) dengan salt 16-byte efektif melindungi kata sandi dari serangan kamus dan brute-force.\n"
    "3. Penerapan nonce acak 12-byte dan tag otentikasi 16-byte pada mode GCM tidak hanya menjamin kerahasiaan (*confidentiality*) tetapi juga "
    "menjamin keaslian dan integritas (*integrity/authenticity*) data, di mana manipulasi sekecil apapun pada ciphertext akan langsung ditolak.\n"
    "4. Program berhasil lulus 100% pada seluruh 4 skenario pengujian wajib dan menangani error secara elegan tanpa traceback mentah."
)

output_path = r"D:\KULIAH\SEMESTER 5\CYBERSEC\Enkripsi Simetris\Laporan_Praktikum_Enkripsi_Simetris_103072400134.docx"
doc.save(output_path)
print(f"Laporan berhasil dibuat di: {output_path}")

