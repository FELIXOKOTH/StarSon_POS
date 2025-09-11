from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

c = canvas.Canvas("test_report.pdf", pagesize=letter)
c.drawString(100, 750, "Welcome to ReportLab!")
c.save()

print("Successfully generated test_report.pdf")
