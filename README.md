# Analisis Pasar Potensial E-Commerce di Brasil  

## 📌 Deskripsi Proyek  
Proyek ini bertujuan untuk mengidentifikasi pasar potensial bagi e-commerce di Brasil dengan menggunakan **geospatial analysis** dan visualisasi data. Fokus utama adalah menemukan wilayah potential market dengan jumlah transaksi rendah tetapi memiliki rata-rata pengeluaran tinggi.  

## Tujuan Analisis  
- Mengidentifikasi wilayah dengan jumlah transaksi dan total pengeluaran terbesar.  
- Menemukan wilayah dengan jumlah transaksi rendah tetapi rata-rata pengeluaran tinggi sebagai target pasar potensial.  
- Menganalisis karakteristik pembelian pelanggan berdasarkan region.  

## Teknologi yang Digunakan  
- **Python** (pandas, numpy, folium, seaborn, matplotlib)  
- **Jupyter Notebook** untuk eksplorasi dan analisis data  
- **Folium** untuk visualisasi peta  

## 📊 Hasil Analisis  
1. **Wilayah dengan transaksi dan pengeluaran terbesar**:  
   - **São Paulo (SP), Rio de Janeiro (RJ), Minas Gerais (MG), Rio Grande do Sul (RS), Paraná (PR)**  
   - Kota dengan ekosistem e-commerce paling berkembang.  

2. **Pasar Potensial (Transaksi rendah, Pengeluaran tinggi)**:  
   - Kota: **Campina Grande, Macapá, Juazeiro do Norte, Paulo Afonso**  
   - Negara bagian: **Acre (AC), Amapá (AP), Paraíba (PB), Piauí (PI)**  

3. **Karakteristik Pembelian**:  
   - Wilayah **Southeast** mendominasi transaksi bulanan, dengan lonjakan pada Agustus & November.  
   - Pembelian puncak terjadi antara **10:00 - 12:00 dan 20:00 - 21:00**.  

## 🚀 Cara Menjalankan  
1. **Install Dependencies**  
   pip install -r requirements.txt
2. **Pindah ke direktori**
   cd dashboard
3. **Jalankan streamlit**
   streamlit run dashboard.py