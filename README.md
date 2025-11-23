# ⬇ Kaizo Image Downloader
Image Downloader for imagebam.com imgbox.com postimg.cc ibb.co.com

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

**[English]** | [Bahasa Indonesia](#bahasa-indonesia)

A powerful, modern, and fast bulk image downloader built with Python and Tkinter. Designed to scrape and download high-quality images from popular image hosting sites, bypassing interstitial pages and ads automatically.

![App Screenshot](screenshot.png)

## 🚀 Key Features

* **Site Support:** Works seamlessly with:
    * `postimg.cc`
    * `imgbox.com`
    * `ibb.co` / `ibb.co.com`
    * `imagebam.com` (Auto-bypass "Continue" buttons & Cookie Injection)
* **Modern GUI & Themes:** 5 Professional themes included (Dark Soft, Light Pro, Ocean Breeze, Matrix, Midnight Blue).
* **Turbo Mode:** Supports up to **50 simultaneous connections** for maximum speed usage.
* **Smart Dashboard:** Real-time monitoring of Speed, Total Size, Duration, and Success/Error rates.
* **Connection Monitor:** Live status indicators for your internet and target servers.
* **Resume Capability:** Skips files that have already been downloaded to save bandwidth.
* **Optimized Core:** Uses large chunk sizes (128KB) and thread pooling for efficient CPU and Disk usage.

## 🛠️ Installation

1.  **Install Python:**
    Make sure you have Python installed. You can download it from [python.org](https://www.python.org/).

2.  **Clone or Download:**
    Download this repository as a ZIP file or clone it using Git.

3.  **Install Dependencies:**
    Open your terminal/command prompt in the project folder and run:
    ```bash
    pip install requests beautifulsoup4
    ```

## 📖 How to Use

1.  Run the script:
    ```bash
    python Kaizo_Image_Downloader.pyw
    ```
2.  **Input Links:** Paste your list of image links into the text area (one link per line) or use the **"📂 Load .txt File"** button.
3.  **Settings:**
    * Select your destination folder.
    * Adjust the **Connections (Turbo)** slider (Recommended: 8-16 for normal use, 32+ for high-speed internet).
    * Choose your preferred **Theme**.
4.  **Start:** Click **"START DOWNLOAD"**.
5.  Sit back and watch the dashboard!

---

<a name="bahasa-indonesia"></a>
# ⬇ Kaizo Image Downloader - Bahasa Indonesia
Download gambar untuk imagebam.com imgbox.com postimg.cc ibb.co.com

Aplikasi download gambar massal yang canggih, modern, dan cepat yang dibuat menggunakan Python dan Tkinter. Dirancang untuk mengunduh gambar resolusi tinggi dari berbagai situs hosting gambar populer, mampu melewati halaman iklan dan tombol "Continue" secara otomatis.

## 🚀 Fitur Utama

* **Mendukung Situs:** Bekerja lancar dengan:
    * `postimg.cc`
    * `imgbox.com`
    * `ibb.co` / `ibb.co.com`
    * `imagebam.com` (Otomatis bypass tombol "Continue" & Injeksi Cookie)
* **Tampilan Modern (GUI):** Tersedia 5 Tema Profesional (Dark Soft, Light Pro, Ocean Breeze, Matrix, Midnight Blue).
* **Mode Turbo:** Mendukung hingga **50 koneksi bersamaan** untuk memaksimalkan kecepatan internet.
* **Dashboard Pintar:** Memantau Kecepatan, Total Ukuran File, Durasi, dan Status Sukses/Gagal secara *real-time*.
* **Monitor Koneksi:** Indikator status langsung untuk internet dan server tujuan.
* **Fitur Resume:** Otomatis melewati file yang sudah pernah didownload untuk menghemat kuota.
* **Optimasi Core:** Menggunakan ukuran paket data besar (128KB) dan manajemen thread yang efisien agar tidak memberatkan komputer.

## 🛠️ Cara Instalasi

1.  **Install Python:**
    Pastikan kamu sudah menginstall Python. Jika belum, download di [python.org](https://www.python.org/).

2.  **Download Script:**
    Download repository ini sebagai ZIP atau clone menggunakan Git.

3.  **Install Library Pendukung:**
    Buka terminal/CMD di folder project ini, lalu ketik perintah:
    ```bash
    pip install requests beautifulsoup4
    ```

## 📖 Cara Penggunaan

1.  Jalankan script:
    ```bash
    python Kaizo_Image_Downloader.pyw
    ```
2.  **Masukkan Link:** Copy-paste daftar link gambar kamu ke kolom input (satu link per baris) atau gunakan tombol **"📂 Load File .txt"**.
3.  **Pengaturan:**
    * Pilih folder penyimpanan.
    * Atur **Jumlah Koneksi (Turbo)** (Saran: 8-16 untuk penggunaan normal, 32+ jika internet sangat cepat).
    * Pilih **Tema Tampilan** sesuai selera.
4.  **Mulai:** Klik tombol **"MULAI DOWNLOAD"**.
5.  Tunggu hingga proses selesai!

---

## ⚠️ Disclaimer

This tool is for educational purposes only. Please respect the Terms of Service of the websites you are downloading from. Do not use this tool to download copyrighted content without permission.

Alat ini dibuat untuk tujuan edukasi. Harap patuhi Syarat dan Ketentuan (ToS) dari situs web tempat Anda mengunduh. Jangan gunakan alat ini untuk mengunduh konten berhak cipta tanpa izin.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
