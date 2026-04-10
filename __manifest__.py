# -*- coding: utf-8 -*-
{
    'name': 'SIRITA: Perencanaan Anggaran',
    'version': '1.1.2',
    'summary': 'Manajemen Perencanaan & Anggaran Strategis - Menjaga Siri\'ta Institusi (SIRITA Ecosystem)',
    'description': """
SIRITA: Perencanaan Strategis & Anggaran Terintegrasi (v14)
==========================================================
Bagian Inti dari SIRITA (Sistem Universitas Terintegrasi)

Filosofi Siri'ta:
-----------------
Perencanaan anggaran yang akuntabel dalah bentuk menjaga Siri' (Kehormatan/Martabat) Institusi. 
Modul ini memastikan setiap langkah universitas dilakukan dengan integritas tertinggi dan 
tanggung jawab suci (Accountability First).

Fitur Utama & Keunggulan Ekosistem:
-----------------------------------
- Integrity-Driven Workflow: Validasi berjenjang (Operator -> SPI -> LPM) menjaga akuntabilitas.
- Dual-Period Management: Kontrol ketat Periode Usulan Awal & Periode Usulan Revisi (V1-VN).
- Organic Master Data Growth: Item SBI kustom yang divalidasi SPI otomatis menjadi Master SBI Institusi.
- Seamless Integration: Terhubung dengan SIRITA Akademik, OJS, Sevima, dan SISTER.
- Smart Budgeting: Dukungan AI (Plugin 'sirita_perencanaan_ai') untuk pemetaan kategori Anggaran.

"Planning with Honor, Executing with Excellence. Jaga Siri'ta melalui SIRITA Perencanaan."
    """,
    'category': 'Account/Planning',
    'author': ' Sufyaldy | sufyaldys@gmail.com',
    'depends': ['base', 'hr'],
    'data': [
        'security/perencanaan_security.xml',
        'security/ir.model.access.csv',
        'data/sirita_data.xml',
        'reports/report_actions.xml',
        'reports/report_tor_template.xml',
        'views/perencanaan_views.xml',
        'views/master_views.xml',
        'views/menu_views.xml',
        'data/sirita_data.xml',
        'data/perencanaan_akun_data.xml',
        'data/perencanaan_iku_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'sirita_perencanaan/static/src/js/perencanaan_dashboard.js',
            'sirita_perencanaan/static/src/xml/perencanaan_dashboard.xml',
        ],
    },
}