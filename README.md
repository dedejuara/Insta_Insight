# Insta_Insight Documentation

Program Insta_Insight adalah sebuah aplikasi yang mengintegrasikan beberapa proses untuk memberikan wawasan mendalam terhadap media di Instagram. Beberapa proses utama yang dijalankan dalam program ini melibatkan:

1. **Scraping Media Instagram:** Mengambil data media dari akun Instagram yang ditentukan.
2. **Face Detection:** Menggunakan model deteksi wajah untuk mengenali wajah dalam media yang diambil.
3. **Image Classification:** Melakukan klasifikasi gambar untuk mengidentifikasi objek atau konten tertentu dalam media.
4. **Image Captioning:** Menambahkan deskripsi teks otomatis untuk setiap media yang diambil.

## Requirements

Untuk menjalankan program ini, pastikan sistem Anda memenuhi persyaratan berikut:

- Python 3.10
- Library yang diperlukan
  - selenium 4.15.2
  - gradio 3.40.1
  - bs4
  - mediapipe
- Chromedriver 190.0.6045.105
- Chrome for Testing (Chromium) 190.0.6045.105

Untuk model deteksi wajah, Anda perlu mengunduh file detector yang dapat diakses melalui [tautan ini](https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite). Simpan file dengan nama `detector.tflite`.

NB: Sangat disarankan untuk menggunakan virtual environment.

## Instalasi

1. Instal semua dependensi dengan menjalankan perintah:

    ```bash
    pip install -r requirements.txt
    ```

2. Download file detector dari mediapipe dengan menjalankan script berikut:

    ```python
    import requests

    url = "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite"
    file_path = "detector.tflite"

    response = requests.get(url)

    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
    ```

## Penggunaan

1. Jalankan aplikasi dengan perintah:

    ```bash
    python app.py
    ```

2. Buka link yang ditampilkan dalam terminal, biasanya pada [http://127.0.0.1:7860/](http://127.0.0.1:7860/).
3. Aplikasi akan menampilkan antarmuka dengan elemen input user, tombol, dan output dataframe.
4. Isi kolom input dengan username Instagram yang akan di-scrap.
5. Klik tombol `Get Insight`, lalu tunggu sampai program selesai, yang biasanya memakan waktu sekitar 20 menit.
6. Jika berhasil, hasil output berupa dataframe dari scraping, face detection, image classification, dan image captioning akan ditampilkan.
7. Seluruh media hasil scraping akan disimpan dalam folder `Scraping_Instagram`.

Dengan menjalankan langkah-langkah di atas, Anda dapat mendapatkan wawasan yang mendalam terhadap konten yang terdapat dalam akun Instagram yang ditentukan.
