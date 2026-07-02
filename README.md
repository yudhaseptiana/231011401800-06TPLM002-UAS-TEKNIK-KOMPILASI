# 231011401800-06TPLM002-UAS-TEKNIK-KOMPILASI

# Simulator Mini-Compiler (While Loop)

Repositori ini berisi implementasi program `WhileCompiler` berbasis Python yang dirancang sebagai simulator sederhana untuk menunjukkan alur kerja dari fase-fase utama sebuah **Kompilator (Compiler)** pada mata kuliah **Teknik Kompilasi**.

Program ini secara khusus memproses satu struktur kontrol spesifik, yaitu perulangan `while` (contoh: `while ( x < 10 ) { x = x + 1 }`), melalui 4 tahapan utama kompilasi.

---

## 🚀 Fitur & Tahapan Kompilasi

Program ini mensimulasikan proses kompilasi melalui empat fase standar:

1. **Analisis Leksikal (Lexical Analysis / Scanner):** Memecah kode sumber mentah menjadi potongan kata bermakna (*tokens*).
2. **Analisis Sintaksis (Syntax Analysis / Parser):** Memvalidasi struktur hirarki kode dan merepresentasikannya ke dalam bentuk *Abstract Syntax Tree* (AST) sederhana.
3. **Analisis Semantik (Semantic Analysis):** Memeriksa validitas kontekstual, seperti memastikan semua variabel yang digunakan di dalam kondisi perulangan telah dideklarasikan pada *Symbol Table*.
4. **Generasi Kode Antara (Intermediate Code Generation / TAC):** Mentransformasikan AST menjadi *Three-Address Code* (TAC) yang merepresentasikan instruksi tingkat rendah menggunakan kontrol alur lompatan (`goto`).

---

## 📦 Struktur Kelas dan Komponen

Kelas utama `WhileCompiler` memiliki komponen internal sebagai berikut:

* `self.source_code`: Menyimpan *string* kode sumber input yang akan dikompilasi.
* `self.label_counter`: Menghitung dan menghasilkan label unik (`L1`, `L2`, dst.) untuk kebutuhan instruksi melompat pada TAC.
* `self.symbol_table`: Sebuah tabel simbol berbasis *dictionary* yang menyimpan variabel valid beserta tipe datanya. Secara default, variabel yang dikenali adalah `x` dan `y` bertipe `int`.

---

## 🛠️ Penjelasan Detail Kode

### 1. Analisis Leksikal (`lexical_analysis`)
Menggunakan modul regular expression (`re`) untuk mendeteksi karakter khusus seperti operator dan tanda kurung, lalu memberikan spasi di sekitar karakter tersebut agar dapat dipecah menjadi *list of tokens* menggunakan fungsi `.split()`.

### 2. Analisis Sintaksis & Semantik (`syntax_and_semantic_analysis`)
* **Sintaksis:** Melakukan pengecekan struktural dasar untuk memastikan token pertama adalah `while`, serta memiliki pasangan tanda kurung `()` dan kurung kurawal `{}`. Jika valid, data diekstrak ke dalam struktur AST:
  ```python
  ast = {
      "node_type": "WhileLoop",
      "condition": condition_str,
      "body": body_str
  }

  Semantik: Memeriksa setiap token alfabet di dalam kondisi while. Jika ada variabel yang tidak terdaftar di dalam self.symbol_table, program akan melempar NameError (simulasi variabel belum dideklarasikan).

  Generasi Kode Antara (generate_tac)
Memanfaatkan metode generator label otomatis untuk menyusun alur eksekusi berbasis kode tiga alamat (TAC) menggunakan sintaks kondisional if ... goto dan lompatan mutlak goto.

Contoh Penggunaan & Output
Secara default, jika file uas_teknik_kompilasi.py dijalankan langsung, program menggunakan input berikut:
while ( x < 10 ) { x = x + 1 }

Hasil Log Terminal:
==================================================
KODE SUMBER INPUT:
  while ( x < 10 ) { x = x + 1 }
==================================================

1. [HASIL ANALISIS LEKSIKAL]
   Tokens: ['while', '(', 'x', '<', '10', ')', '{', 'x', '=', 'x', '+', '1', '}']

2 & 3. [HASIL ANALISIS SINTAKSIS (AST) & SEMANTIK]
   AST Node: {'node_type': 'WhileLoop', 'condition': 'x < 10', 'body': 'x = x + 1'}
   Status Semantik: Valid (Semua variabel terdaftar)

4. [GENERASI THREE-ADDRESS CODE (TAC)]
L1:
if x < 10 goto L2
goto L3
L2:
  x = x + 1
goto L1
L3:
==================================================

Analisis Logika TAC:
L1: Titik awal perulangan untuk mengecek kondisi kembali.

if x < 10 goto L2: Jika kondisi terpenuhi (benar), lompat ke blok L2 untuk mengeksekusi isi body.

goto L3: Jika kondisi salah, lompat ke blok L3 untuk keluar dari perulangan.

goto L1: Di akhir blok L2, program dipaksa melompat kembali ke atas (L1) untuk mengecek ulang kondisi perulangan.

Kesimpulan
Meskipun analisis pada simulator ini masih berbasis manipulasi string dan list sederhana (belum menggunakan algoritma parsing formal seperti LL/LR Parser), program ini secara fundamental berhasil menggambarkan miniatur proses transformasi kode sumber tingkat tinggi menjadi kode antara siap pakai yang independen terhadap mesin target.
