from fpdf import FPDF
import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Laporan Hasil Pemeriksaan Laboratorium', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=True)
        self.ln(5)

    def lab_result_table(self, data):
        self.set_font('Arial', '', 12)
        for item in data:
            self.cell(70, 10, item[0], border=1)
            self.cell(40, 10, str(item[1]), border=1)
            self.cell(50, 10, item[2], border=1)
            self.ln()

lab_data = [
    ("Nama Pasien", "Jane Doe", ""),
    ("Tanggal Lahir", "1985-04-23", ""),
    ("Tanggal Pemeriksaan", str(datetime.date.today()), ""),
    ("Jumlah Kehamilan", 3, "Normal: 0 - 15"),
    ("Glukosa (mg/dL)", 138, "Normal: < 140"),
    ("Tekanan Darah (mm Hg)", "82", "Normal: < 80"),
    ("Ketebalan Lipatan Kulit (mm)", 35, "Normal: 10 - 50"),
    ("Insulin (mu U/ml)", 130, "Normal: 16 - 166"),
    ("BMI", 28.5, "Normal: 18.5 - 24.9"),
    ("Diabetes Pedigree Function", 0.245, ""),
    ("Usia", 40, "Tahun"),
    ("Hasil", "-", "Akan diprediksi oleh sistem")
]

pdf = PDF()
pdf.add_page()
pdf.chapter_title("Informasi Pasien & Hasil Lab Terkait Diabetes")
pdf.lab_result_table(lab_data)

pdf.output("Laporan_Lab.pdf")
print("PDF dummy berhasil dibuat: Laporan_Lab.pdf")