# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PerencanaanAnggaran(models.Model):
    _name = 'sirita.perencanaan.anggaran'
    _description = 'Pagu Perencanaan Anggaran SIRITA Clean'
    _order = 'year desc, type asc'

    def _get_default_department(self):
        return self.env.user.employee_id.department_id.id

    name = fields.Char(string='Judul Perencanaan', required=True)
    year = fields.Selection([(str(y), str(y)) for y in range(2023, 2031)], 
                            string='Tahun Anggaran', default=lambda self: str(fields.Date.today().year), required=True)
    
    type = fields.Selection([
        ('1', 'Pagu Indikatif'),
        ('2', 'Pagu Definitif'),
        ('3', 'Revisi Anggaran')
    ], string='Jenis Pagu', default='1', required=True)

    revision_number = fields.Integer(string='Revisi Ke-', default=0)
    parent_id = fields.Many2one('sirita.perencanaan.anggaran', string='Induk Anggaran', ondelete='cascade')
    revision_ids = fields.One2many('sirita.perencanaan.anggaran', 'parent_id', string='Riwayat Revisi')
    iku_id = fields.Many2one('sirita.perencanaan.iku', string='Target IKU', required=False)
    department_id = fields.Many2one('hr.department', string='Unit Kerja', default=_get_default_department, required=True)
    user_id = fields.Many2one('res.users', string='Penanggung Jawab', default=lambda self: self.env.user)

    state = fields.Selection([
        ('draft', 'Usulan / Draft'),
        ('spi', 'Reviu SPI'),
        ('lpm', 'Reviu LPM'),
        ('done', 'Selesai'),
    ], string='Status', default='draft')

    review_notes = fields.Text(string='Catatan Reviewer')
    item_ids = fields.One2many('sirita.perencanaan.item', 'parent_id', string='Detail Usulan')
    total_amount = fields.Monetary(string='Total Anggaran', compute='_compute_total', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    # --- TOR (KAK) COMPREHENSIVE FIELDS ---
    # Header Info
    tor_kementerian = fields.Char(string='Kementerian', default='KEMENTERIAN AGAMA R.I.')
    tor_organisasi = fields.Char(string='Unit Organisasi', default='DITJEN PENDIDIKAN ISLAM')
    tor_program = fields.Char(string='Program', default='PENDIDIKAN ISLAM')
    tor_satker = fields.Char(string='Satuan Kerja', default='IAIN PAREPARE')
    
    # Summary sections
    tor_output_expected = fields.Html(string='Hasil yang Diharapkan (Output)')
    tor_performance_indicator = fields.Html(string='Indikator Kinerja Kegiatan')
    tor_output_type = fields.Html(string='Satuan Ukur dan Jenis Keluaran')
    
    # 1. Latar Belakang
    tor_legal_basis = fields.Html(string='1.a Dasar Hukum')
    tor_general_overview = fields.Html(string='1.b Gambaran Umum')
    tor_rationale = fields.Html(string='1.c Alasan Kegiatan')
    
    # 2. Kegiatan
    tor_activity_description = fields.Html(string='2.a Uraian Kegiatan')
    tor_activity_target = fields.Html(string='2.b Sasaran Kegiatan')
    
    # 3. Maksud & Tujuan
    tor_maksud = fields.Html(string='3.a Maksud Kegiatan')
    tor_tujuan = fields.Html(string='3.b Tujuan Kegiatan')
    
    # 4. Indikator & Keluaran
    tor_indicator_qualitative = fields.Html(string='4.a Indikator Keluaran (Kualitatif)')
    tor_output_quantitative = fields.Html(string='4.b Keluaran (Kuantitatif)')
    
    # 5. Cara Pelaksanaan
    tor_method = fields.Html(string='5.a Metode Pelaksanaan')
    tor_stages = fields.Html(string='5.b Tahapan Kegiatan')
    
    # 6. Tempat & 7. Pelaksana
    tor_location = fields.Char(string='6. Tempat Pelaksanaan', default='IAIN Parepare')
    tor_coordinator_id = fields.Many2one('hr.employee', string='Koordinator Pelaksana')
    tor_member_ids = fields.Many2many('hr.employee', 'perencanaan_tor_member_rel', 'perencanaan_id', 'employee_id', string='Anggota Pelaksana')
    
    # 8. Jadwal
    tor_schedule_desc = fields.Char(string='Rentang Waktu (When)', default='Januari s/d Desember')
    # Dynamic schedule booleans for matrix (Jan-Des)
    tor_m1 = fields.Boolean('Jan'); tor_m2 = fields.Boolean('Feb'); tor_m3 = fields.Boolean('Mar')
    tor_m4 = fields.Boolean('Apr'); tor_m5 = fields.Boolean('Mei'); tor_m6 = fields.Boolean('Jun')
    tor_m7 = fields.Boolean('Jul'); tor_m8 = fields.Boolean('Agu'); tor_m9 = fields.Boolean('Sep')
    tor_m10 = fields.Boolean('Okt'); tor_m11 = fields.Boolean('Nov'); tor_m12 = fields.Boolean('Des')

    @api.depends('item_ids.total')
    def _compute_total(self):
        for rec in self:
            rec.total_amount = sum(rec.item_ids.mapped('total'))

    def _check_period(self, period_type):
        """ Helper untuk validasi jendela waktu (initial vs revision) """
        today = fields.Date.today()
        period = self.env['sirita.perencanaan.period'].search([
            ('year', '=', self.year),
            ('type', '=', period_type),
            ('date_start', '<=', today),
            ('date_stop', '>=', today),
            ('is_active', '=', True)
        ], limit=1)
        if not period:
            label = "Usulan Anggaran Baru" if period_type == 'initial' else "Revisi Anggaran"
            raise UserError(_(f"Maaf, saat ini Jendela Waktu {label} sedang TERTUTUP! \n\n"
                             f"Admin LPM belum membuka periode ini untuk Tahun Anggaran {self.year}."))
        return True

    def action_submit_spi(self): 
        self._check_period('initial')
        self.write({'state': 'spi'})

    def action_submit_lpm(self): self.write({'state': 'lpm'})
    def action_approve(self): self.write({'state': 'done'})
    def action_refuse(self): self.write({'state': 'draft'})

    def action_create_revision(self):
        """ Fungsi untuk menduplikasi dokumen yang sudah DONE menjadi Dokumen REVISI baru """
        import logging
        _logger = logging.getLogger(__name__)
        
        # Validasi Jendela Waktu REVISI
        self._check_period('revision')

        # Pastikan dipanggil dari 1 record saja di form
        self.ensure_one()
        
        target_revision = self.revision_number + 1
        _logger.info(f"SIRITA: Mencoba membuat revisi ke-{target_revision} untuk {self.name}")

        # 1. Buat Header Baru secara manual dari data lama
        new_val = {
            'name': f"{self.name} (Revisi {target_revision})",
            'year': self.year,
            'type': '3', # Revisi
            'state': 'draft',
            'parent_id': self.id,
            'revision_number': target_revision,
            'iku_id': self.iku_id.id,
            'department_id': self.department_id.id,
            'user_id': self.env.user.id,
            'tor_kementerian': self.tor_kementerian,
            'tor_organisasi': self.tor_organisasi,
            'tor_program': self.tor_program,
            'tor_satker': self.tor_satker,
            'tor_output_expected': self.tor_output_expected,
            'tor_performance_indicator': self.tor_performance_indicator,
            'tor_output_type': self.tor_output_type,
            'tor_legal_basis': self.tor_legal_basis,
            'tor_general_overview': self.tor_general_overview,
            'tor_rationale': self.tor_rationale,
            'tor_activity_description': self.tor_activity_description,
            'tor_activity_target': self.tor_activity_target,
            'tor_maksud': self.tor_maksud,
            'tor_tujuan': self.tor_tujuan,
            'tor_indicator_qualitative': self.tor_indicator_qualitative,
            'tor_output_quantitative': self.tor_output_quantitative,
            'tor_method': self.tor_method,
            'tor_stages': self.tor_stages,
            'tor_location': self.tor_location,
            'tor_coordinator_id': self.tor_coordinator_id.id,
            'tor_member_ids': [(6, 0, self.tor_member_ids.ids)],
            'tor_schedule_desc': self.tor_schedule_desc,
            'tor_m1': self.tor_m1, 'tor_m2': self.tor_m2, 'tor_m3': self.tor_m3,
            'tor_m4': self.tor_m4, 'tor_m5': self.tor_m5, 'tor_m6': self.tor_m6,
            'tor_m7': self.tor_m7, 'tor_m8': self.tor_m8, 'tor_m9': self.tor_m9,
            'tor_m10': self.tor_m10, 'tor_m11': self.tor_m11, 'tor_m12': self.tor_m12,
        }
        
        # Gunakan context agar tidak diganggu oleh tracking mail atau trigger lain
        new_rev = self.env['sirita.perencanaan.anggaran'].with_context(tracking_disable=True).create(new_val)
        _logger.info(f"SIRITA: Berhasil membuat record baru ID {new_rev.id} dengan revisi {new_rev.revision_number}")
        
        # 2. Buat Item Baru secara manual
        for item in self.item_ids:
            self.env['sirita.perencanaan.item'].create({
                'parent_id': new_rev.id,
                'sbi_id': item.sbi_id.id,
                'name': item.name,
                'akun_id': item.akun_id.id,
                'volume': item.volume,
                'satuan_id': item.satuan_id.id,
                'unit_price': item.unit_price,
            })
        
        # 3. Lempar user ke halaman revisi yang baru dibuat
        return {
            'name': f"Draft Revisi Ke-{target_revision}",
            'type': 'ir.actions.act_window',
            'res_model': 'sirita.perencanaan.anggaran',
            'view_mode': 'form',
            'res_id': new_rev.id,
            'target': 'current',
            'context': {'form_view_initial_mode': 'edit'}
        }

    def action_submit_lpm(self):
        """ Lulus Reviu SPI: Konversi item Kustom ke Master SBI """
        import logging
        _logger = logging.getLogger(__name__)
        self._check_period('initial')
        
        # PROSES VALIDASI SBI: Jika ada item kustom yang diisi operator dan disetujui SPI
        sbi_obj = self.env['perencanaan.sbi']
        for item in self.item_ids:
            if item.is_custom and not item.sbi_id:
                # Cek apakah item serupa sudah ada di SBI
                existing_sbi = sbi_obj.search([('name', '=', item.name)], limit=1)
                if not existing_sbi:
                    # Daftarkan ke Master SBI Otomatis
                    new_sbi = sbi_obj.create({
                        'name': item.name,
                        'price': item.unit_price,
                        'satuan_id': item.satuan_id.id,
                        'akun_id': item.akun_id.id,
                    })
                    item.write({'sbi_id': new_sbi.id, 'is_custom': False})
                    _logger.info(f"SIRITA: Mempromosikan '{item.name}' menjadi Master SBI.")

        self.write({'state': 'lpm'})

    def action_print_tor(self):
        """ Mencetak laporan PDF TOR/KAK """
        return self.env.ref('sirita_perencanaan.action_report_tor').report_action(self)

    @api.model
    def get_perencanaan_stats(self):
        """ Mengambil data statistik untuk dashboard OWL """
        self.env.cr.execute("""
            SELECT state, sum(total_amount) as total 
            FROM sirita_perencanaan_anggaran 
            GROUP BY state
        """)
        state_data = {r[0]: r[1] for r in self.env.cr.fetchall()}
        
        # Budget per IKU
        self.env.cr.execute("""
            SELECT iku.code, sum(pagu.total_amount) 
            FROM sirita_perencanaan_anggaran pagu
            JOIN sirita_perencanaan_iku iku ON pagu.iku_id = iku.id
            GROUP BY iku.code
        """)
        iku_stats = self.env.cr.fetchall()

        # Top 5 Departments
        self.env.cr.execute("""
            SELECT COALESCE(dept.name->>'id_ID', dept.name->>'en_US', dept.name->>current_setting('res.lang')::text, 'Non-Dept') as name, 
                   sum(pagu.total_amount)
            FROM sirita_perencanaan_anggaran pagu
            LEFT JOIN hr_department dept ON pagu.department_id = dept.id
            GROUP BY dept.id, dept.name
            ORDER BY 2 DESC LIMIT 5
        """)
        top_depts = self.env.cr.fetchall()

        return {
            'states': {
                'draft': state_data.get('draft', 0),
                'review': state_data.get('spi', 0) + state_data.get('lpm', 0),
                'done': state_data.get('done', 0),
            },
            'iku_data': [{'code': r[0], 'amount': r[1]} for r in iku_stats],
            'top_depts': [{'name': str(r[0]), 'amount': r[1]} for r in top_depts],
        }

class PerencanaanItem(models.Model):
    _name = 'sirita.perencanaan.item'
    _description = 'Item Usulan Anggaran SIRITA'
    
    parent_id = fields.Many2one('sirita.perencanaan.anggaran', string='Induk Perencanaan', ondelete='cascade')
    sbi_id = fields.Many2one('perencanaan.sbi', string='Standar Biaya (SBI)')
    name = fields.Char(string='Nama Kegiatan', required=True)
    akun_id = fields.Many2one('perencanaan.akun', string='Akun')
    volume = fields.Float(string='Volume', default=1.0)
    satuan_id = fields.Many2one('perencanaan.satuan', string='Satuan')
    unit_price = fields.Float(string='Harga Satuan')
    total = fields.Monetary(string='Jumlah', compute='_compute_subtotal', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='parent_id.currency_id')
    is_custom = fields.Boolean(string='Kustom?', default=False, help='Tandai jika item ini belum ada di master SBI')

    @api.onchange('sbi_id')
    def _onchange_sbi_id(self):
        if self.sbi_id:
            self.name = self.sbi_id.name
            self.unit_price = self.sbi_id.price
            self.satuan_id = self.sbi_id.satuan_id.id

    @api.depends('volume', 'unit_price')
    def _compute_subtotal(self):
        for rec in self:
            rec.total = rec.volume * rec.unit_price

class PerencanaanPeriod(models.Model):
    _name = 'sirita.perencanaan.period'
    _description = 'Jendela Waktu Perencanaan'

    name = fields.Char(string='Nama Periode', required=True)
    type = fields.Selection([
        ('initial', 'Usulan Anggaran Awal'),
        ('revision', 'Usulan Revisi Anggaran')
    ], string='Jenis Periode', default='initial', required=True)
    
    year = fields.Selection([(str(y), str(y)) for y in range(2023, 2031)], 
                             string='Untuk Tahun Anggaran', required=True)
    date_start = fields.Date(string='Tanggal Buka', required=True)
    date_stop = fields.Date(string='Tanggal Tutup', required=True)
    is_active = fields.Boolean(string='Aktif?', default=True)
