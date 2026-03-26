from pathlib import Path

from fpdf import FPDF

fixtures_dir = Path("app/tests/fixtures")
fixtures_dir.mkdir(parents=True, exist_ok=True)

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, "This is a sample PDF for testing.\nIt contains readable text.")
pdf.output(str(fixtures_dir / "sample.pdf"))

print("sample.pdf created successfully")