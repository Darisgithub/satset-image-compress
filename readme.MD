# Implementasi Image Compression Menggunakan Metode Singular Value Decomposition (SVD) Berbasis Python

> Linear Algebra Final Project — Image Compression using Singular Value Decomposition (SVD) with Python ecosystem and interactive visualization.

Project ini merupakan implementasi konsep Aljabar Linear pada kompresi citra digital menggunakan metode Singular Value Decomposition (SVD). Aplikasi dibuat menggunakan Python dengan library NumPy, Matplotlib, Pillow, dan Streamlit.

## Contributors

| No | Contributor           | NIM         |
| -- | --------------------- | ----------- |
| 1  | Muhamad Rifki Firdaus | 24552010142 |
| 2  | Bagoes Wahyu Untoro   | 24552010157 |
| 3  | Muhammad Daris        | 24552010133 |
| 4  | Ramzi Sajid           | 24552010183 |
| 5  | Galih Raka Danoarta   | 24552010134 |

---

## Academic Information

* Course: Linear Algebra
* Study Program: Informatics Engineering
* Faculty: Faculty of Engineering
* University: Universitas Muhammadiyah Tangerang
* Year: 2026

---

## Project Goals

* Memahami penerapan Aljabar Linear dalam dunia IT
* Mengimplementasikan metode SVD pada kompresi gambar
* Menampilkan perbandingan gambar sebelum dan sesudah kompresi
* Membuat aplikasi interaktif berbasis Python

---

## Tech Stack

| Kebutuhan          | Technology |
| ------------------ | ---------- |
| Core Programming   | Python     |
| Matrix Computation | NumPy      |
| Visualization      | Matplotlib |
| Image Processing   | Pillow     |
| Interactive UI     | Streamlit  |

---

## System Architecture

```text
User Upload Image
        ↓
Pillow Read Image
        ↓
NumPy Convert Matrix
        ↓
SVD Compression
        ↓
Matplotlib Visualization
        ↓
Streamlit Display UI
```

---

## Features

* Upload gambar
* Kompresi gambar menggunakan metode SVD
* Perbandingan gambar asli dan hasil kompresi
* Visualisasi hasil menggunakan Matplotlib
* Tampilan interaktif menggunakan Streamlit

---

## Installation

### Install Dependencies

```bash
pip install numpy matplotlib pillow streamlit
```

---

## Run Project

```bash
streamlit run src/app.py
```

---

## Project Structure

```text
svd-image-compression/
│
├── src/
│   ├── app.py              # Streamlit UI
│   └── compression.py      # SVD compression logic
│
├── images/
├── requirements.txt
└── README.md
```

---

## SVD Concept

Singular Value Decomposition (SVD) adalah metode dekomposisi matriks:

```math
A = UΣV^T
```

Metode ini digunakan untuk mengurangi ukuran data gambar dengan tetap mempertahankan informasi penting pada citra.

---

## Conclusion

Project ini menunjukkan bahwa konsep Aljabar Linear dapat diterapkan dalam bidang teknologi informasi, khususnya pada kompresi citra digital menggunakan metode Singular Value Decomposition (SVD).

Dengan bantuan Python dan library scientific computing, proses kompresi gambar dapat divisualisasikan secara interaktif dan mudah dipahami.
