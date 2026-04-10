# -*- coding: utf-8 -*-
from odoo import models, fields

class PerencanaanSumber(models.Model):
    _name = 'perencanaan.sumber'
    _description = 'Sumber Anggaran (RM/PNBP/BOPTN)'
    
    name = fields.Char(string='Sumber Anggaran', required=True)
    code = fields.Char(string='Kode Sumber')

class PerencanaanSatuan(models.Model):
    _name = 'perencanaan.satuan'
    _description = 'Satuan Ukuran (Orang/Kali/Paket)'
    
    name = fields.Char(string='Nama Satuan', required=True)

class PerencanaanAkun(models.Model):
    _name = 'perencanaan.akun'
    _description = 'Akun Mata Anggaran (BAS)'
    
    name = fields.Char(string='Nama Akun', required=True)
    code = fields.Char(string='Nomor Akun', required=True)

class PerencanaanSBI(models.Model):
    _name = 'perencanaan.sbi'
    _description = 'Standar Biaya Input (SBI)'
    
    name = fields.Char(string='Nama Komponen/Barang', required=True)
    code = fields.Char(string='Kode SBI')
    price = fields.Float(string='Harga Satuan (SBM)')
    satuan_id = fields.Many2one('perencanaan.satuan', string='Satuan')
    akun_id = fields.Many2one('perencanaan.akun', string='Akun Biaya (Default)')
    active = fields.Boolean(default=True)

class PerencanaanPeriod(models.Model):
    _name = 'sirita.perencanaan.period'
    _description = 'Periode Revisi Anggaran'
    _order = 'date_start desc'

    name = fields.Char(string='Nama Periode', required=True, placeholder='Misal: Revisi Triwulan I')
    year = fields.Selection([(str(y), str(y)) for y in range(2023, 2031)], 
                            string='Tahun Anggaran', required=True)
    date_start = fields.Date(string='Tanggal Buka', required=True)
    date_stop = fields.Date(string='Tanggal Tutup', required=True)
    is_active = fields.Boolean(string='Aktif?', default=True)

    _sql_constraints = [
        ('check_dates', 'CHECK(date_start <= date_stop)', 'Tanggal tutup tidak boleh mendahului tanggal buka!')
    ]

class PerencanaanIKU(models.Model):
    _name = 'sirita.perencanaan.iku'
    _description = 'Indikator Kinerja Utama (IKU)'
    _order = 'code asc'

    code = fields.Char(string='Kode IKU', required=True)
    name = fields.Char(string='Indikator', required=True)
    description = fields.Text(string='Deskripsi / Target')
    active = fields.Boolean(default=True)

    def name_get(self):
        result = []
        for rec in self:
            name = f"[{rec.code}] {rec.name}"
            result.append((rec.id, name))
        return result
