# Proyek Identifikasi Spesies dengan BLAST

Aplikasi web sederhana yang dibuat dengan Python (Flask) dan Biopython untuk mengidentifikasi spesies berdasarkan sekuens DNA atau protein menggunakan layanan NCBI BLAST.

## 📜 Deskripsi

Aplikasi ini memungkinkan pengguna untuk mengunggah file sekuens dalam format FASTA. Sekuens tersebut kemudian dikirim ke server NCBI untuk dianalisis menggunakan BLAST (Basic Local Alignment Search Tool). Hasilnya akan menampilkan spesies yang paling cocok berdasarkan kemiripan sekuens, beserta informasi relevan seperti tingkat identitas dan E-value.

Proyek ini merupakan eksplorasi dasar di bidang bioinformatika yang menggabungkan pengembangan web dengan analisis data biologis.

## ✨ Fitur

-   Antarmuka web yang responsif untuk mengunggah file.
-   Mendukung format file FASTA (.fasta, .fa, .fna, .faa).
-   Deteksi otomatis tipe sekuens (DNA atau Protein) untuk memilih program BLAST yang sesuai (`blastn` atau `blastp`).
-   Menampilkan hasil identifikasi teratas beserta metriknya (Accession, Score, E-value, Identity).
-   Animasi memuat saat menunggu hasil dari NCBI.

## 🚀 Teknologi yang Digunakan

-   **Backend:** Python, Flask
-   **Bioinformatika:** Biopython
-   **Frontend:** HTML, Tailwind CSS, JavaScript
-   **Platform:** GitHub

## ⚙️ Cara Menjalankan Secara Lokal

Untuk menjalankan proyek ini di komputer Anda, ikuti langkah-langkah berikut:

1.  **Clone repository ini:**
    ```bash
    git clone [https://github.com/NAMA_USER_ANDA/NAMA_REPO_ANDA.git](https://github.com/NAMA_USER_ANDA/NAMA_REPO_ANDA.git)
    cd NAMA_REPO_ANDA
    ```

2.  **Buat dan aktifkan virtual environment (opsional tapi disarankan):**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Instal semua pustaka yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Catatan: Anda perlu membuat file `requirements.txt` terlebih dahulu dengan menjalankan `pip freeze > requirements.txt` di terminal Anda).*

4.  **Jalankan aplikasi Flask:**
    ```bash
    python app.py
    ```

5.  Buka browser dan kunjungi `http://127.0.0.1:5000`.

---
