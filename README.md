#  SIRITA: Perencanaan Anggaran (v1.1.2)
> **"Planning with Honor, Executing with Excellence. Jaga Siri'ta melalui SIRITA Perencanaan."**

[![Odoo Version](https://img.shields.io/badge/Odoo-18.0-ae4988.svg?logo=odoo)](https://www.odoo.com/)
[![License](https://img.shields.io/badge/License-LGPL--3-blue.svg)](LICENSE)
[![SIRITA Ecosystem](https://img.shields.io/badge/Ecosystem-SIRITA-orange.svg)](https://github.com/sirita-integrated)

**SIRITA Perencanaan** adalah modul  dalam ekosistem SIRITA (Sistem Universitas Terintegrasi) yang dirancang untuk mengelola perencanaan anggaran strategis institusi dengan menjunjung tinggi filosofi **Siri'ta** (Menjaga Kehormatan & Martabat Institusi). Modul ini memastikan akuntabilitas dan integritas tinggi dalam setiap tahapan pengusulan anggaran universitas.

---

##  Fitur Utama

- **Integrity-Driven Workflow**: Validasi berjenjang yang ketat dari tingkat **Operator → SPI → LPM** untuk memastikan setiap usulan memenuhi standar integritas institusi.
- **Dual-Period Management**: Kontrol yang sangat presisi antara **Periode Usulan Awal** dan **Periode Usulan Revisi (V1 hingga VN)**.
- **Organic Master Data Growth**: Item SBI kustom yang divalidasi oleh SPI secara otomatis dikonversi menjadi *Master Database SBI* Institusi yang terus bertumbuh secara organik.
- **Seamless Integration**: Terintegrasi penuh dengan addon default dan custom odoo lainnya.
- **Smart Budgeting Ready**: Dapat di integrasikan dengan AI (Plugin 'sirita_perencanaan_ai') untuk pemetaan kategori Anggaran (On Progress...... )

---

## Instalasi

1. Pastikan Anda telah menginstal modul dasar Odoo 18.
2. Clone repository ini ke folder `extra-addons` Anda:
   ```bash
   git clone https://github.com/sufyaldy/sirita_perencanaan.git
   ```
3. Update daftar modul di Odoo (Activate Developer Mode).
4. Klik **Update App List**.
5. Cari **SIRITA: Perencanaan Anggaran** dan klik **Activate/Upgrade**.

---

##  Struktur Alur Kerja (Workflow)

Berikut adalah alur akuntabilitas yang diterapkan dalam modul ini:
1. **Operator**: Melakukan input usulan rencana kegiatan dan anggaran.
2. **SPI (Satuan Penjamin Mutu Internal)**: Melakukan validasi standar biaya dan kelayakan anggaran.
3. **LPM (Lembaga Penjamin Mutu)**: Melakukan persetujuan akhir berdasarkan kesesuaian dengan Rencana Strategis (RENSTRA) Universitas.

---

##  Laporan & Output
Modul ini menghasilkan dokumen TOR (Terms of Reference) yang siap cetak serta dokumen Rencana Kerja Tahunan yang terstruktur rapi untuk kebutuhan audit dan manajerial.

---

##  Kontributor & Lisensi

- **Author**: Sufyaldy | [sufyaldys@gmail.com](mailto:sufyaldys@gmail.com)
- **Organization**: SIRITA Ecosystem 
- **License**: LGPL-3 (Lesser General Public License)
