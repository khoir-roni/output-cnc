# 🛠️ Kiri:Moto CNC Milling Cheatsheet & Parameter Reference

Dokumen ini berisi rangkuman fungsi, parameter default, dan penjelasan logis untuk konfigurasi **CNC Milling** pada *slicer* browser Kiri:Moto.

---

## 1. Tabs (Pengikat Benda Kerja)
*Tabs* adalah jembatan kecil material yang sengaja ditinggalkan agar benda kerja tidak terlepas, bergeser, atau terlempar saat pemotongan tembus (*cutout*) selesai.

*   **Width (5):** Lebar horizontal struktur tab (5 mm).
*   **Height (5):** Ketinggian/ketebalan vertikal struktur tab (5 mm).
*   **Depth (5):** Kedalaman penetrasi tab masuk ke dalam model (5 mm).
*   **Midline:** Posisi tab otomatis diletakkan tepat di tengah-tengah ketebalan model.
*   **+ (Add Button):** Tombol interaktif untuk menempatkan titik tab baru secara manual pada model 3D.

---

## 2. Stock (Bahan Baku / Blok Material)
Konfigurasi dimensi fisik material mentah sebelum dipotong oleh pahat.

*   **Width (5):** Ukuran total material pada Sumbu X (5 mm).
*   **Depth (5):** Ukuran total material pada Sumbu Y (5 mm).
*   **Height (1):** Ketebalan total material pada Sumbu Z (1 mm).
*   **Offset:** Jarak tambahan (margin) di sekeliling luar model untuk memastikan pembersihan material optimal.
*   **Indexed:** Mode pengerjaan multi-sisi berputar (*4-axis rotary* atau *flip-milling*).

---

## 3. Limits & Z-Axis (Batas Aman Sumbu Z)
Pengaturan koordinat vertikal untuk menjaga keamanan mesin, pahat, dan *clamp* penahan.

*   **Z Anchor (middle v):** Titik acuan sumbu Z, diatur di tengah (*middle*) secara vertikal pada material.
*   **Z Offset (0):** Nilai pergeseran sumbu Z dari titik jangkar (0 mm = tanpa pergeseran).
*   **Z Top (0):** Posisi koordinat permukaan paling atas dari material mentah.
*   **Z Bottom (0):** Batas kedalaman maksimum yang diizinkan untuk dipotong oleh pahat.
*   **Z Clearance (5):** Ketinggian aman (5 mm) di atas benda kerja. Pahat akan naik ke titik ini saat melakukan pergerakan cepat (*rapid travel*) melintasi area kosong agar tidak menabrak material/klem.

---

## 4. Feed & Speed (Kecepatan Gerak Pahat)
Parameter kontrol waktu pengerjaan dan kualitas potong mesin.

*   **Feed Rate (6000):** Kecepatan potong horizontal (Sumbu X/Y) saat memotong material (6000 mm/menit).
*   **Plunge Rate (300):** Kecepatan tusuk vertikal (Sumbu Z) saat pahat pertama kali masuk ke dalam material (300 mm/menit).

---

## 5. Output & Strategi Pemotongan
Menentukan urutan prioritas gerakan pemotongan dan generasi perintah G-code.

*   **Ease Down (10):** Jalur masuk miring (*ramping*) sepanjang 10 mm untuk memotong secara bertahap, meminimalkan stres beban langsung pada ujung pahat.
*   **Depth First:** Pahat akan menyelesaikan satu profil lubang/kantong hingga kedalaman penuh sebelum berpindah ke profil berikutnya. (Jika mati, pemotongan dilakukan lapis demi lapis merata ke seluruh model).
*   **Inner First:** Memotong fitur bagian dalam (seperti lubang/slot) terlebih dahulu sebelum memotong profil luar benda kerja untuk mencegah hilangnya rigiditas bahan.
*   **Tool Init:** Blok kode perintah perintah awal (*setup macro*) untuk inisialisasi pahat atau sistem spindel.

---

## 6. Advanced Z Controls
*   **First Z Max:** Memaksa kedalaman pemotongan lapisan pertama (*first pass*) langsung berada pada batas maksimum demi efisiensi.
*   **Force Z Max:** Memaksa sumbu Z untuk selalu naik ke titik clearance tertinggi setiap kali berganti jalur potong baru.

---

## 7. Entry & Engagement (Sudut Penetrasi)
*   **Ease Angle (0.8):** Sudut kemiringan (0.8 derajat) saat pahat masuk bergerak maju ke dalam material (*ramping angle*).
*   **Engage Factor (0):** Koefisien beban atau penyesuaian kecepatan saat pahat pertama kali menyentuh dinding material.

---

## 8. Origin (Titik Nol Mesin / WCS G54)
Menentukan letak titik koordinat awal (0,0,0) sebagai acuan kerja mesin CNC.

*   **Origin Top:** Titik nol sumbu Z diposisikan rata dengan permukaan atas material mentah.
*   **Origin Center:** Titik nol sumbu X dan Y diletakkan tepat di tengah-tengah material mentah.
*   **Offset X (0) / Y (0) / Z (0):** Pergeseran koordinat manual secara spesifik jika titik nol nyata di meja mesin sengaja digeser dari standar perangkat lunak.

---

## 9. Tombol Sistem
*   **Select:** Digunakan untuk memilih model, area kerja, atau tipe pahat (*endmill*).
*   **Reset:** Mengembalikan seluruh konfigurasi parameter ke setelan bawaan pabrik (*factory default*).
*   **Expert:** Mengaktifkan opsi mode tingkat lanjut untuk membuka fungsi-fungsi optimasi tersembunyi.

---

## 10. Fitur Tambahan (Expert Mode)
*   **Arc Output:** Mengaktifkan konversi kode gerakan melingkar sejati (`G2`/`G3`) alih-alih memecah lingkaran menjadi ribuan garis lurus pendek (`G1`). Menghasilkan gerakan mesin yang jauh lebih halus dan ukuran berkas G-code yang jauh lebih kecil.
*   **Skip Shadow:** Mengabaikan kalkulasi pemotongan pada area kosong yang tidak memiliki model kerja untuk menghemat waktu pengerjaan.
*   **Rounded Corners:** Membulatkan sedikit radius sudut tajam pada jalur lintasan agar kecepatan makan mesin (*feed*) konstan dan mengurangi getaran berlebih (*chatter*).

---

## 📑 Panduan Pengaturan Parameter CNC: Tabs, Stock, & Advanced

Untuk membuka seluruh parameter di bawah ini, pastikan Anda telah mengaktifkan tombol **Expert** di panel kanan bawah Kiri:Moto terlebih dahulu.

```mermaid
flowchart TD
    Start([Mulai Setup Kiri:Moto]) --> Expert[Aktifkan Mode Expert]
    
    subgraph S1 [1. Pengaturan Tabs]
        Tabs1[Centang Opsi Tabs] --> Tabs2[Set Dimensi Width/Height/Depth: 5]
        Tabs2 --> Tabs3[Aktifkan Midline & Tambahkan Titik Tabs +]
    end
    
    subgraph S2 [2. Pengaturan Stock]
        Stock1[Masukkan Dimensi Bahan Mentah X, Y, Z] --> Stock2[Atur Offset Luar & Nonaktifkan Indexed]
    end
    
    subgraph S3 [3. Limits & Batas Sumbu Z]
        Limit1[Set Z Anchor: middle v] --> Limit2[Set Z Offset, Top, & Bottom: 0]
        Limit2 --> Limit3[Set Z Clearance: 5 mm]
    end
    
    subgraph S4 [4. Kecepatan & Feedrate]
        Speed1[Set Feed Rate: 6000 mm/min] --> Speed2[Set Plunge Rate: 300 mm/min]
    end
    
    subgraph S5 [5. Alur Potong & G-Code]
        Alur1[Set Ease Down: 10 mm & Ease Angle: 0.8°] --> Alur2[Centang Depth First & Inner First]
        Alur2 --> GCode[Centang Arc Output, Skip Shadow, Rounded Corners]
    end
    
    Expert --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> Save[Tekan Shift + U untuk Save ke Cloud]
    Save --> End([Selesai / Siap Generate G-code])
    
    style Start fill:#4F46E5,stroke:#312E81,stroke-width:2px,color:#fff
    style End fill:#10B981,stroke:#065F46,stroke-width:2px,color:#fff
    style Save fill:#F59E0B,stroke:#78350F,stroke-width:2px,color:#fff
```

---

### 🛑 1. Pengaturan Tabs (Jembatan Pengikat)
*Tabs* wajib diatur jika Anda memotong material hingga tembus (*cutout*). Tanpa tabs, benda kerja akan lepas di akhir pemotongan, tersangkut pada pahat yang berputar, dan berisiko merusak model atau mematahkan pahat.

*   **Cara Memasang Tabs:**
    1. Centang atau aktifkan opsi **Tabs**.
    2. Masukkan dimensi standar: **Width: 5**, **Height: 5**, dan **Depth: 5**.
    3. Pilih **Midline** agar posisi jembatan ini berada tepat di tengah-tengah ketebalan material Anda.
    4. Klik tombol **+ (Select/Add)**, lalu klik pada garis luar model di layar 3D untuk menempatkan titik tabs. Berikan minimal 2–4 titik untuk menjaga stabilitas objek.

---

### 📦 2. Pengaturan Stock (Ukuran Bahan Mentah)
Kiri:Moto memerlukan data ukuran balok material mentah asli yang Anda jepit di meja CNC.

*   **Konfigurasi Dimensi:**
    *   **Width (X):** Masukkan lebar total bahan mentah Anda (Contoh: `5` mm atau sesuai ukuran asli kayu/akrilik Anda).
    *   **Depth (Y):** Masukkan kedalaman/panjang bahan mentah (Contoh: `5` mm).
    *   **Height (Z):** Masukkan tebal material mentah Anda (Contoh: `1` mm).
*   **Offset:** Jika bahan mentah Anda sedikit lebih besar dari model digital, berikan nilai offset (misal `2` mm) agar pahat mulai memotong dari luar material dengan aman.
*   **Indexed:** Biarkan tidak dicentang kecuali Anda menggunakan sumbu rotasi ke-4 (*4th axis / rotary table*).

---

### 📐 3. Pengaturan Koordinat & Batas Sumbu Z (Limits)
Bagian terpenting untuk mencegah pahat menabrak meja kerja mesin (*spoilboard*).

*   **Z Anchor:** Pilih **middle v** (*Middle Vertical*) untuk memposisikan titik jangkar di tengah material, atau sesuaikan dengan kebutuhan taktik pengerjaan Anda.
*   **Z Offset:** Atur ke `0` sebagai standar awal.
*   **Z Top & Z Bottom:** Atur ke `0`. Ini adalah titik aman di mana **Z Top** adalah permukaan atas material mentah Anda, dan **Z Bottom** adalah batas bawah terdalam pergerakan pahat.
*   **Z Clearance:** Atur ke `5` mm. Setiap kali pahat selesai memotong satu jalur dan ingin pindah ke jalur lain, pahat akan naik setinggi 5 mm di atas material untuk menghindari klem penahan.

---

### ⚡ 4. Pengaturan Kecepatan (Feed & Plunge)
*   **Feed Rate:** Atur ke `6000` mm/menit. Ini adalah kecepatan gerak potong horizontal (X dan Y). *Catatan: Sesuaikan nilai ini dengan kemampuan mesin Anda. Untuk mesin hobi kecil, Anda mungkin perlu menurunkannya ke 1000–2000 mm/menit.*
*   **Plunge Rate:** Atur ke `300` mm/menit. Ini adalah kecepatan pahat bergerak turun tegak lurus (Sumbu Z) menusuk material. Selalu buat nilai ini jauh lebih kecil dari Feed Rate.

---

### 🔄 5. Alur Pemotongan & Output (Expert Mode)
*   **Ease Down:** Atur ke `10` mm. Fitur ini membuat pahat masuk ke material secara miring (*ramping*) sepanjang 10 mm, bukan langsung menancap tegak lurus, sehingga memperpanjang umur pakai pahat.
*   **Ease Angle:** Masukkan `0.8` derajat untuk sudut kemiringan saat pahat mulai menusuk masuk secara perlahan (*ramping angle*).
*   **Depth First (Rekomendasi - Dicentang):** Pahat akan menyelesaikan satu lubang hingga jebol ke bawah terlebih dahulu, baru pindah ke lubang berikutnya.
*   **Inner First (Rekomendasi - Dicentang):** Pahat akan memotong bagian dalam/lubang-lubang kecil terlebih dahulu. Profil luar model baru akan dipotong di akhir proses agar sisa bahan tetap kokoh terjepit.

---

### 🛠️ 6. Fitur Optimasi G-Code (Expert)
*   **Arc Output (Wajib Dicentang):** Mengaktifkan kode G2/G3 untuk gerakan melingkar sejati. Hasil potongan bulat akan menjadi sangat halus dan ukuran file G-code menjadi sangat kecil.
*   **Skip Shadow (Dicentang):** Mengabaikan kalkulasi pada area kosong yang tidak memiliki model untuk menghemat waktu pengerjaan mesin.
*   **Rounded Corners (Dicentang):** Membulatkan sedikit sudut tajam pada jalur pahat agar mesin tidak mengerem mendadak di sudut siku, yang dapat menyebabkan getaran (*chatter*) pada hasil potongan.

---

### 🪵 & 💎 Rekomendasi Feed/Plunge Rate Berdasarkan Material

Berikut adalah panduan perkiraan kecepatan pemotongan (*Feed Rate* & *Plunge Rate*) untuk beberapa jenis material menggunakan mata pahat standar (misal: *2-flute flat endmill* diameter 3.175 mm atau 1/8" pada mesin CNC hobi/semipro):

| Material | Feed Rate (X/Y) | Plunge Rate (Z) | Depth of Cut (Stepdown) per Pass | Keterangan |
| :--- | :--- | :--- | :--- | :--- |
| **Kayu Lunak (Softwood / MDF / Plywood)** | 1500 - 2500 mm/menit | 300 - 500 mm/menit | 1.0 - 2.0 mm | Mudah dipotong, bersihkan serpihan kayu secara berkala agar tidak macet. |
| **Kayu Keras (Hardwood - Jati/Mahoni)** | 1000 - 1500 mm/menit | 200 - 300 mm/menit | 0.5 - 1.0 mm | Butuh kecepatan lebih lambat dan stepdown lebih tipis agar pahat tidak patah dan serat tidak pecah (*tearout*). |
| **Akrilik (Acrylic / PMMA)** | 800 - 1200 mm/menit | 150 - 250 mm/menit | 0.3 - 0.6 mm | Gunakan mata pahat *single-flute* (O-flute) agar akrilik tidak meleleh dan menggulung pada pahat. |
| **Aluminium (Soft Metal - Seri 6061)** | 400 - 600 mm/menit | 80 - 120 mm/menit | 0.1 - 0.2 mm | Wajib pelumasan (*mist/air blast*) agar aluminium tidak menempel pada mata pahat (*chip welding*). |

*Catatan: Nilai di atas adalah panduan awal. Selalu lakukan tes potong (*test cut*) pada material sisa sebelum memulai proyek utama.*

---

> [!TIP]
> **Penyimpanan Profil (Cloud Save)**
> Jika Anda sudah selesai memasukkan angka-angka ini, jangan lupa tekan **Shift + U** untuk mengamankan dan menyimpan seluruh profil pengaturan ini ke cloud Kiri:Moto!

