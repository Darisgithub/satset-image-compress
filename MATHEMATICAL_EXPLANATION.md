# Penerapan Aljabar Linear dalam SVD Image Compression

Dokumen ini menjelaskan konsep matematika di balik **Singular Value Decomposition (SVD)** dan bagaimana menerapkannya untuk kompresi citra digital.

---

## 📚 Bagian 1: Dasar-Dasar Aljabar Linear

### 1.1 Matriks dalam Konteks Gambar

Sebuah gambar digital dapat direpresentasikan sebagai **matriks numerik**, dimana setiap elemen merepresentasikan intensitas pixel.

#### Contoh: Gambar Grayscale 3×3

```
Gambar:                    Matriks Pixel:
┌─────┐                    ┌────────────┐
│ ▓ ░ │                    │ 230  50  100 │
│ ░ ░ │        →           │  80 150  200 │
│ ▓ ▓ │                    │ 220 240   40 │
└─────┘                    └────────────┘

Notasi: A (height=3, width=3)
```

**Nilai pixel:** 0 (hitam) sampai 255 (putih)

#### Gambar RGB (Berwarna)

Gambar RGB terdiri dari **3 channel terpisah**:
- **Channel R (Red):** matriks intensitas merah
- **Channel G (Green):** matriks intensitas hijau  
- **Channel B (Blue):** matriks intensitas biru

```
Gambar RGB:        Decompose ke 3 matriks:
┌─────────┐        
│ 🔴 🟢 🔵│        R = [255  0   0 ]    G = [0  255  0]    B = [0   0  255]
│ 🟡 ⚪ 🟣│    →  [255 255  0]        [255 255 0]       [255  0 255]
│ 🔵 🟡 ⚪│        [0  255 255]        [0  255 255]       [255 255  0]
└─────────┘
```

Setiap channel adalah matriks 2D yang bisa dikompresi secara terpisah.

---

### 1.2 Norma dan Ortogonalitas

#### Norma Vektor (Vector Norm)

Norma adalah **"panjang"** atau **"magnitude"** dari vektor.

Untuk vektor $\vec{v} = [v_1, v_2, ..., v_n]$:

$$||\vec{v}||_2 = \sqrt{v_1^2 + v_2^2 + ... + v_n^2}$$

**Contoh:**
```
Vektor v = [3, 4]
||v||₂ = √(3² + 4²) = √(9 + 16) = √25 = 5
```

#### Ortogonalitas (Perpendicular)

Dua vektor $\vec{u}$ dan $\vec{v}$ adalah **orthogonal** jika:
$$\vec{u} \cdot \vec{v} = 0$$

Artinya: **Produk dot sama dengan 0** (tidak ada "overlap").

**Contoh:**
```
u = [1, 0]    →  u · v = (1)(0) + (0)(1) = 0 ✓ Orthogonal
v = [0, 1]
```

#### Matriks Ortogonal

Matriks $Q$ adalah **orthogonal** jika kolom-kolomnya adalah orthonormal:
$$Q^T Q = I$$

Atau ekuivalen: $Q^T = Q^{-1}$

**Sifat penting:** Matriks orthogonal **mempertahankan panjang vektor** (isometric).

---

### 1.3 Operasi Matriks Fundamental

#### Matrix Multiplication

$$C = A \times B$$

Dimana $C_{ij} = \sum_{k} A_{ik} \times B_{kj}$

**Dimensi:**
```
A (m × n) × B (n × p) = C (m × p)
```

#### Transpose

$$A^T$$

Matriks yang dihasilkan dari menukar baris dan kolom.

**Contoh:**
```
A = [1 2 3]        A^T = [1 4]
    [4 5 6]              [2 5]
                         [3 6]
```

#### Determinant & Eigenvalue

**Determinant** - Skalar yang merepresentasikan "scaling factor" dari matriks.

**Eigenvalue & Eigenvector** - Pasangan $(\lambda, \vec{v})$ dimana:
$$A \vec{v} = \lambda \vec{v}$$

Eigenvalue menunjukkan **seberapa besar** eigenvector di-scale oleh matriks $A$.

---

## 🔄 Bagian 2: Singular Value Decomposition (SVD)

### 2.1 Definisi SVD

**Singular Value Decomposition** adalah teknik untuk menguraikan **setiap matriks** $A$ (m × n) menjadi tiga komponen:

$$A = U \Sigma V^T$$

Dimana:
- **U** (m × m): Matriks orthogonal - **left singular vectors**
- **Σ** (m × n): Matriks diagonal - **singular values**
- **V^T** (n × n): Matriks orthogonal transpose - **right singular vectors**

#### Representasi Diagonal Σ

$$\Sigma = \begin{bmatrix}
\sigma_1 & 0 & 0 & \cdots & 0 \\
0 & \sigma_2 & 0 & \cdots & 0 \\
0 & 0 & \sigma_3 & \cdots & 0 \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
0 & 0 & 0 & \cdots & \sigma_r \\
\end{bmatrix}$$

**Singular values:** $\sigma_1 \geq \sigma_2 \geq \sigma_3 \geq ... \geq \sigma_r \geq 0$ (selalu non-negative, terurut descending)

---

### 2.2 Interpretasi Geometris SVD

Setiap matriks $A$ merepresentasikan **transformasi linear** dari input space ke output space.

SVD mendekomposisi transformasi ini menjadi **3 operasi sederhana**:

```
Input Vector
    ↓
[V^T]: Rotasi dalam input space
    ↓
[Σ]: Scaling (stretch/shrink) dalam setiap dimensi
    ↓
[U]: Rotasi dalam output space
    ↓
Output Vector
```

#### Visualisasi

```
Original Space                  Transformed Space
(input)                        (output)

     v₂  (eigenvector)              u₂ (eigenvector)
     ↑                              ↑
     |    Unit Circle               |    Ellipse
     |     ⭕                        |      ⭕
     |                              |   σ₂ · u₂
     └──────→ v₁                    └──────→ u₁
            σ₁ · u₁

Proses: Rotasi V^T → Scaling Σ → Rotasi U
```

---

### 2.3 Hubungan SVD dengan Eigenvalue Decomposition

SVD dan **Eigenvalue Decomposition (EVD)** saling berhubungan:

#### EVD dari A^T A (Covariance Matrix)

$$A^T A = (U \Sigma V^T)^T (U \Sigma V^T)$$
$$A^T A = V \Sigma^T U^T U \Sigma V^T$$
$$A^T A = V \Sigma^T \Sigma V^T = V \Lambda V^T$$

Dimana:
- **Eigenvectors** dari $A^T A$ adalah **kolom V** (right singular vectors)
- **Eigenvalues** dari $A^T A$ adalah **$\sigma_i^2$** (kuadrat dari singular values)

**Interpretasi:** 
- Singular values menunjukkan "variance" dalam setiap komponen principal
- Semakin besar $\sigma_i$, semakin besar kontribusi komponen ke-i dalam merepresentasikan data original

---

## 🖼️ Bagian 3: Aplikasi SVD untuk Image Compression

### 3.1 Konsep Dasar Kompresi

#### Full Rank Reconstruction

Menggunakan semua singular values:

$$A = U \Sigma V^T = U_{m \times m} \Sigma_{m \times n} V^T_{n \times n}$$

**Ukuran penyimpanan:**
- U: $m \times m$ floats
- Σ: $m \times n$ floats (hanya diagonal)
- V^T: $n \times n$ floats

**Total: $m^2 + n(m+n)$ floats** (boros!)

#### Low Rank Approximation

**Ide:** Hanya gunakan **k singular values terbesar** (k << m, n)

$$A_k = U_{m \times k} \Sigma_{k \times k} V^T_{k \times n}$$

**Ukuran penyimpanan:**
- U_k: $m \times k$ floats
- Σ_k: $k \times k$ floats (hanya diagonal)
- V^T_k: $k \times n$ floats

**Total: $k(m + n + 1)$ floats** (jauh lebih kecil!)

### 3.2 Compression Ratio Calculation

Untuk gambar dengan dimensi **height × width** dan **channels** channel:

#### Original Size
$$\text{Original} = \text{height} \times \text{width} \times \text{channels} \text{ bytes}$$

#### Compressed Size
$$\text{Compressed} = k \times (\text{height} + \text{width} + 1) \times \text{channels} \text{ bytes}$$

#### Compression Ratio
$$\text{Ratio} = \frac{\text{Compressed}}{\text{Original}} \times 100\%$$

#### Contoh Konkret

```
Image: 600 × 400 pixels, RGB (3 channels)
Rank k: 50

Original size = 600 × 400 × 3 = 720,000 bytes = 703.1 KB

Compressed size = 50 × (600 + 400 + 1) × 3 
                = 50 × 1001 × 3
                = 150,150 bytes = 146.6 KB

Compression Ratio = 150,150 / 720,000 × 100% = 20.85%
```

**Interpretasi:** Ukuran file berkurang hingga hanya 20.85% dari original! 🎉

---

### 3.3 Loss of Information (Trade-off)

Saat menggunakan **low rank approximation**, kita kehilangan informasi detail tinggi.

#### Frobenius Norm - Ukuran Error

Error dari rekonstruksi rank-k:

$$\text{Error} = ||A - A_k||_F = \sqrt{\sum_{i=k+1}^{r} \sigma_i^2}$$

Dimana $r$ = min(m, n) = rank maksimal

**Interpretasi:**
- Error diukur dari **singular values yang diabaikan** ($\sigma_{k+1}$ ke $\sigma_r$)
- Semakin besar $\sigma_i$ yang diabaikan, semakin besar error
- Karena $\sigma_i$ terurut descending, error minimal ketika mengambil $k$ terbesar

#### Visual Quality vs Compression

```
Rank k=10      Rank k=50       Rank k=100      Original
┌──────────┐   ┌──────────┐    ┌──────────┐    ┌──────────┐
│  ▓▓▓    │   │  ▓▓▓░░░  │    │  ▓▓▓░░░░ │    │  ▓▓▓░░░░ │
│ (Blur)   │   │ (Better) │    │ (Good)   │    │ (Perfect)│
│ Size: 10%│   │ Size: 21%│    │ Size: 42%│    │ Size:100%│
└──────────┘   └──────────┘    └──────────┘    └──────────┘

Trade-off: Semakin tinggi k → kualitas lebih baik tapi size lebih besar
```

---

## 💾 Bagian 4: Implementasi di Project

### 4.1 Flow Matematika

```
User Upload Image
    ↓
Image to Matrix (Convert pixel values to float32)
    A (H × W) ← Image data
    
    ↓
[IF RGB] Split ke 3 Channel
    A_R, A_G, A_B (H × W masing-masing)
    
    ↓
SVD Decomposition
    U, Σ, V^T = SVD(A_i)
    
    ↓
Low Rank Approximation (user pilih k via slider)
    A_k = U[:k] @ Σ[:k] @ V^T[:k:]
    
    ↓
Normalization (Min-Max Scaling ke 0-255)
    A_normalized = (A_k - min) / (max - min) × 255
    
    ↓
[IF RGB] Recombine Channels
    Result = [A_R_k, A_G_k, A_B_k]
    
    ↓
Convert to uint8 (standard image format)
    
    ↓
Display & Save
```

### 4.2 Kode Matematika

#### SVD Decomposition (Python dengan NumPy)

```python
import numpy as np

# Citra grayscale: H × W
image = np.array(image, dtype=np.float32)

# SVD Decomposition
U, S, VT = np.linalg.svd(image, full_matrices=False)

# U: H × H atau H × min(H,W) (tergantung full_matrices)
# S: min(H, W) singular values (vector 1D)
# VT: min(H,W) × W atau W × W
```

#### Low Rank Reconstruction

```python
k = 50  # Rank yang dipilih user

# Rekonstruksi dengan rank k
# U[:, :k] → ambil k kolom pertama (H × k)
# np.diag(S[:k]) → buat diagonal matrix (k × k)
# VT[:k, :] → ambil k baris pertama (k × W)
A_compressed = U[:, :k] @ np.diag(S[:k]) @ VT[:k, :]

# Hasil: H × W (dimensi sama seperti original)
```

#### Normalization

```python
# SVD bisa menghasilkan nilai negatif atau > 255
min_val = A_compressed.min()
max_val = A_compressed.max()

# Min-Max scaling
if max_val > min_val:
    A_normalized = (A_compressed - min_val) / (max_val - min_val) * 255

# Convert ke uint8 (0-255 integer)
result = np.clip(A_normalized, 0, 255).astype(np.uint8)
```

---

## 📊 Bagian 5: Analisis & Trade-offs

### 5.1 Kompleksitas Komputasi

| Operasi | Kompleksitas | Waktu |
|---------|------------|-------|
| SVD Decomposition | O(mn²) atau O(m²n) | Lambat untuk gambar besar |
| Low Rank Reconstruction | O(k(m+n)) | Cepat |
| Normalization | O(mn) | Cepat |

**Note:** SVD adalah operasi paling expensive. Untuk production, bisa pakai approximate SVD.

### 5.2 Kualitas vs Kompresi

#### Parameter Penting

```
Rank k:
  k = 1-20   → Extreme compression, very blurry
  k = 50-100 → Good trade-off (20-40% original size)
  k = 200+   → High quality, less compression
  k = min(H,W) → Lossless (100% original size)
```

#### Optimal k Selection

Heuristic:
```python
# Ambil singular values yang cukup untuk ~90% energy
total_energy = np.sum(S ** 2)
cumsum_energy = np.cumsum(S ** 2)
threshold_idx = np.where(cumsum_energy >= 0.9 * total_energy)[0][0]
optimal_k = threshold_idx + 1
```

### 5.3 Keuntungan dan Keterbatasan SVD

#### ✅ Keuntungan
- **Mathematically optimal** - Minimal Frobenius norm error untuk rank k
- **Interpretable** - Singular values menunjukkan "importance"
- **General purpose** - Bekerja untuk setiap matriks
- **Supports all image types** - Grayscale, RGB, RGBA

#### ❌ Keterbatasan
- **Computational cost** - SVD O(m²n) atau O(mn²)
- **Not JPEG-like** - Tidak optimal untuk natural images (JPEG compression ratio lebih baik)
- **No perceptual encoding** - Tidak mempertimbangkan human vision
- **Not suitable for text** - Blurry untuk gambar dengan text

---

## 🎓 Bagian 6: Contoh Kalkulasi Lengkap

### Contoh: Kompresi Gambar 4×4 Sederhana

#### Step 1: Input Image Matrix

```
Gambar grayscale 4×4:
A = [ 100  120  140  160 ]
    [ 110  130  150  170 ]
    [ 120  140  160  180 ]
    [ 130  150  170  190 ]
```

#### Step 2: SVD Decomposition

```
U = [ -0.30  -0.45  -0.82   0.10 ]
    [ -0.31  -0.44   0.53  -0.65 ]
    [ -0.33  -0.42   0.10   0.84 ]
    [ -0.34  -0.41   0.24  -0.07 ]

S = [ 1280.5, 14.2, 3.1, 0.05 ]

V^T = [ -0.26  -0.40  -0.54  -0.68 ]
      [ -0.46   0.88  -0.16   0.02 ]
      [  0.85  -0.26   0.40  -0.01 ]
      [  0.05   0.01  -0.71   0.71 ]
```

#### Step 3: Low Rank Approximation (k=2)

```
A_2 = U[:, :2] @ S[:2] @ V^T[:2, :]

    = [ -0.30  -0.45 ] @ [ 1280.5    0    ] @ [ -0.26  -0.40  -0.54  -0.68 ]
      [ -0.31  -0.44 ]   [   0    14.2    ]   [ -0.46   0.88  -0.16   0.02 ]
      [ -0.33  -0.42 ]
      [ -0.34  -0.41 ]

    = [ 101.2  119.8  139.6  159.8 ]
      [ 111.1  129.9  149.7  170.2 ]
      [ 121.0  139.8  159.5  179.6 ]
      [ 131.1  149.9  169.7  189.4 ]
```

#### Step 4: Evaluate Error

```
Reconstruction error (Frobenius norm):
||A - A_2||_F = √(3.1² + 0.05²) = √(9.61 + 0.0025) ≈ 3.1

Relative error: 3.1 / 1280.5 ≈ 0.24% ✓ Very small!
```

#### Step 5: Size Comparison

```
Original: 4 × 4 = 16 values = 16 floats
Compressed (k=2): 2×(4+4+1) = 18 values = 18 floats

Hmm... lebih besar? Ini karena overhead k kecil untuk matrik kecil.
Untuk gambar besar, kompresi jauh lebih signifikan!

Contoh gambar besar:
Original: 1000 × 1000 = 1,000,000 values
Compressed (k=100): 100×(1000+1000+1) = 200,100 values
Ratio: 200,100 / 1,000,000 = 20% ✓ Much better!
```

---

## 📚 Referensi Aljabar Linear

### Konsep Kunci
1. **Matriks** - Array 2D dari bilangan
2. **Norm** - Ukuran/magnitude dari vektor
3. **Orthogonality** - Perpendicular relationships
4. **Eigenvalues/Eigenvectors** - Karakteristik intrinsik matriks
5. **SVD** - Universal decomposition untuk setiap matriks

### Aplikasi SVD Lainnya
- **Principal Component Analysis (PCA)** - Dimensionality reduction
- **Image processing** - Denoising, super-resolution
- **Recommender systems** - Collaborative filtering
- **Signal processing** - Spectral analysis
- **Machine learning** - Feature extraction

---

## 🎯 Kesimpulan

SVD adalah **aplikasi langsung dari aljabar linear** untuk memecahkan masalah praktis:

✅ **Matematika:** Dekomposisi A = UΣV^T menggunakan konsep orthogonal matrices, singular values, dan linear transformations

✅ **Intuisi:** Memisahkan komponen penting (besar σ) dan tidak penting (kecil σ)

✅ **Aplikasi:** Kompresi citra dengan membuang komponen kecil, drastis mengurangi ukuran file tanpa kehilangan banyak informasi visual

✅ **Result:** Trade-off yang elegant antara **compression ratio** dan **image quality**

Ini menunjukkan kekuatan aljabar linear dalam memecahkan masalah dunia nyata! 🚀
