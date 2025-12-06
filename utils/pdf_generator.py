from fpdf import FPDF
import os

class PDFReport:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.add_page()

        # Correct Unicode font path
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "DejaVuSans.ttf")
        self.pdf.add_font("DejaVu", "", font_path, uni=True)
        self.pdf.set_font("DejaVu", size=12)

    def build(self, inputs, total_cost, breakdown):
        self.pdf.cell(0, 10, "Manufacturing Cost Report", ln=True)

        self.pdf.ln(5)
        self.pdf.set_font("DejaVu", size=11)

        self.pdf.cell(0, 8, f"Total Cost: ₹{total_cost:.2f}", ln=True)

        self.pdf.ln(2)
        self.pdf.cell(0, 8, "Breakdown:", ln=True)

        for k, v in breakdown.items():
            self.pdf.cell(0, 6, f"{k}: ₹{v:.2f}", ln=True)

        return bytes(self.pdf.output(dest="S"))

def generate_pdf_bytes(inputs, total_cost, breakdown):
    report = PDFReport()
    return report.build(inputs, total_cost, breakdown)