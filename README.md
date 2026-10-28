# Proyek Analisis Data: Bike Sharing Dataset ✨

Proyek akhir analisis data ini disusun untuk memenuhi kriteria kelulusan kelas Belajar Analisis Data dengan Python pada Dicoding Academy.

---

## Identitas Pengembang
- **Nama**: Rama Dwi Nugraha
- **Email**: iooloittrr@gmail.com
- **ID Dicoding**: rama_dwi_nugrahaoh17

---

## Deskripsi Proyek
Proyek ini melakukan analisis data eksploratif dan eksplanatori terhadap Bike Sharing Dataset (Capital Bikeshare) periode 2011-2012. Analisis difokuskan pada pengaruh musim dan cuaca terhadap volume rental, pola jam komuter hari kerja versus akhir pekan, dinamika proporsi pengguna kasual versus terdaftar, serta segmentasi lingkungan berbasis suhu dan kelembapan menggunakan teknik manual grouping dan binning.

Tahapan analisis data meliputi:
1. Menentukan pertanyaan bisnis (metode SMART).
2. Data Wrangling (Gathering, Assessing, dan Cleaning data).
3. Exploratory Data Analysis (EDA) dan Analisis Lanjutan (Clustering/Binning tanpa machine learning).
4. Visualisasi data dan Explanatory Analysis dengan prinsip desain dan integritas.
5. Menarik kesimpulan dan rekomendasi aksi bisnis.
6. Pembuatan dashboard interaktif berbasis Streamlit.

---

## Pertanyaan Bisnis (SMART)
1. **Pertanyaan 1**: Bagaimana pengaruh kondisi musim (*Season*) dan kondisi cuaca (*Weather Situation*) terhadap rata-rata dan total volume penyewaan sepeda harian sepanjang periode 2011-2012?
2. **Pertanyaan 2**: Pada jam berapa saja terjadi lonjakan puncak (*peak rush hours*) penyewaan sepeda, dan bagaimana perbedaan pola perilakunya antara hari kerja (*Working Day*) dibandingkan hari libur/akhir pekan (*Weekend / Holiday*) sepanjang tahun 2011-2012?
3. **Pertanyaan 3**: Bagaimana tren pertumbuhan bulanan dan proporsi kontribusi antara pengguna kasual (*Casual Users*) dan pengguna terdaftar (*Registered Members*) dari tahun 2011 hingga 2012?
4. **Pertanyaan 4**: Bagaimana segmentasi volume rental sepeda berdasarkan klaster rentang temperatur suhu (*Temperature Binning*: Cold, Mild, Warm, Hot) dan tingkat kelembapan (*Humidity Binning*: Dry, Ideal, Humid) tanpa algoritma machine learning selama periode 2011-2012?

---

## Struktur Direktori

```text
submission/
├── dashboard/
│   ├── dashboard.py         # Skrip aplikasi dashboard Streamlit
│   ├── main_data.csv        # Dataset bersih yang digunakan untuk dashboard
│   └── requirements.txt     # Daftar dependensi untuk dashboard
├── data/
│   ├── day.csv              # Data mentah harian bike sharing
│   ├── hour.csv             # Data mentah per jam bike sharing
│   └── Readme.txt           # Dokumentasi asli dataset
├── notebook.ipynb           # Berkas Jupyter Notebook (sudah dieksekusi lengkap)
├── README.md                # Dokumentasi petunjuk proyek
├── requirements.txt         # Daftar pustaka yang digunakan
└── url.txt                  # Tautan URL aplikasi dashboard
```

---

## Setup Environment - Anaconda
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

---

## Setup Environment - Shell/Terminal

### Opsi A: Menggunakan Python `venv` (Rekomendasi Virtual Environment Standar)
```bash
# Membuat virtual environment
python -m venv venv

# Mengaktifkan virtual environment
# Pada Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Pada Windows (Command Prompt / CMD):
.\venv\Scripts\activate.bat
# Pada Linux / macOS:
source venv/bin/activate

# Menginstal dependensi
pip install -r requirements.txt
```

### Opsi B: Menggunakan `pipenv` (Sesuai Template Dicoding)
```bash
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

---

## Run steamlit app
Setelah virtual environment aktif dan seluruh dependensi terpasang, jalankan perintah berikut dari direktori utama proyek:

```bash
streamlit run dashboard/dashboard.py
```

Atau jika masuk ke dalam folder `dashboard`:
```bash
cd dashboard
streamlit run dashboard.py
```

Aplikasi dashboard interaktif akan otomatis terbuka pada peramban web di alamat `http://localhost:8501`.

---

## Menjalankan Jupyter Notebook
Untuk melihat seluruh alur Data Wrangling, EDA, hingga Visualisasi Data:
```bash
jupyter notebook notebook.ipynb
```
Seluruh sel kode pada berkas `notebook.ipynb` sudah dieksekusi lengkap beserta output teks, tabel, dan grafik visualisasi.

---

## Panduan Deploy ke Streamlit Community Cloud
1. Pastikan seluruh berkas (`dashboard/`, `data/`, `notebook.ipynb`, `requirements.txt`, `README.md`, `url.txt`) sudah di-*commit* dan di-*push* ke repositori GitHub pribadi yang bersifat **PUBLIC**.
2. Masuk ke [Streamlit Community Cloud](https://share.streamlit.io/) menggunakan akun GitHub.
3. Klik tombol **New app**.
4. Pilih repositori, cabang (*branch* `main` atau `master`), dan tentukan *Main file path*:
   ```text
   dashboard/dashboard.py
   ```
5. Klik **Deploy!**.
6. Setelah aplikasi berhasil aktif dan berjalan, salin tautan publik yang dihasilkan ke dalam berkas `url.txt`.

---

## Ringkasan Kesimpulan
1. **Musim & Cuaca**: Musim Gugur (*Fall*) dan Musim Panas (*Summer*) mencatat rata-rata penyewaan tertinggi (>5.000 unit/hari). Cuaca cerah mendominasi volume rental, sedangkan cuaca hujan/salju menurunkan penyewaan hingga lebih dari 60%.
2. **Pola Jam Komuter**: Hari kerja memiliki pola bimodal dengan lonjakan jam sibuk pada pukul 08:00 dan 17:00-18:00 (aktivitas komuter pekerja). Hari libur/akhir pekan memiliki pola unimodal dengan aktivitas puncak pada siang hari (12:00-16:00).
3. **Dinamika Pengguna**: Total volume rental meningkat sebesar 64,88% pada tahun 2012 dibanding 2011. Pengguna terdaftar (*Registered*) menyumbang 81,17% total volume dan menjadi kontributor utama stabilitas sewa harian.
4. **Segmentasi Lingkungan**: Analisis *binning* menunjukkan suhu kategori Warm (20-28°C) dan Hot (>28°C) dengan kelembapan Ideal (40-70%) merupakan kondisi paling optimal untuk aktivitas bersepeda.
