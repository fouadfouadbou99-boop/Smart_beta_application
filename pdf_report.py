from reportlab.platypus import SimpleDocTemplate,Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(path='report.pdf'):
    doc=SimpleDocTemplate(path)
    doc.build([Paragraph('Smart Beta Maroc',getSampleStyleSheet()['Title'])])
    return path
