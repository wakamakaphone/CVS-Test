from reportlab.lib.pagesizes import A4
from PIL import Image
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import pdfplumber
from datetime import date
#####################################################

def generate_certificate(output_path, candidate_name, grad_number, place_of_birth, diploma_mark, diploma_mark_num, institute_logo_path, institute_signatures_path):
    # Create a PDF document:
    doc = SimpleDocTemplate(output_path, pagesize=A4)

    # Create a list to hold the elements of the PDF:
    elements = []

################################ PDF Design start ########################################

    # Add graduate number on corner of degree (aligment=0):
    gradnum_style = ParagraphStyle(
        "Aligmentstyle",
        parent=getSampleStyleSheet()["Title"],
        fontName="Helvetica",
        fontSize=8,
        leading = 10,
        alignment=0
    )
    grad_num_text = f"ΑΡΙΘΜΟΣ ΜΗΤΡΩΟΥ<br/>ΔΙΠΛΩΜΑΤΟΥΧΩΝ - {grad_number}"
    faculty = Paragraph(grad_num_text, gradnum_style)
    elements.extend([faculty, Spacer(1, 0)])
    
    # Add Greek Democracy text:
    grdim_style = ParagraphStyle(
        "GrDimStyle",
        parent=getSampleStyleSheet()["Title"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading = 15,
        alignment=1
    )
    grdim_text = Paragraph("ΕΛΛΗΝΙΚΗ ΔΗΜΟΚΡΑΤΙΑ", grdim_style)
    elements.extend([grdim_text, Spacer(1, 0)])

    # Add institute logo:
    if institute_logo_path:
        logo = Image(institute_logo_path, width=110, height=110)
        elements.append(logo)

    # Add institute name - Patras University - define institute style:
    institute_style = ParagraphStyle(
        "InstituteStyle",
        parent=getSampleStyleSheet()["Title"],
        fontName="Helvetica-Bold",
        fontSize=25,
        alignment=1
    )
    institute = Paragraph("ΠΑΝΕΠΙΣΤΗΜΙΟ ΠΑΤΡΩΝ", institute_style)
    elements.extend([institute, Spacer(1, 1)])

    # Add Polytechnic School text - define body text style:
    body_text_style = ParagraphStyle(
    "DegreeTextstyle",
    parent=getSampleStyleSheet()["Title"],
    fontName="Helvetica",
    fontSize=13,
    leading = 15,
    alignment=1
    )
    polytechnic = Paragraph("ΠΟΛΥΤΕΧΝΙΚΗ ΣΧΟΛΗ", body_text_style)
    elements.extend([polytechnic, Spacer(1, 0)])

    # Add faculty name - ECE Faculty:
    faculty_style = ParagraphStyle(
        "Facultystyle",
        parent=getSampleStyleSheet()["Title"],
        fontName="Helvetica-Bold",
        fontSize=19,
        leading = 20,
        alignment=1
    )
    faculty = Paragraph("ΤΜΗΜΑ ΗΛΕΚΤΡΟΛΟΓΩΝ ΜΗΧΑΝΙΚΩΝ ΚΑΙ<br/>ΤΕΧΝΟΛΟΓΙΑΣ ΥΠΟΛΟΓΙΣΤΩΝ", faculty_style)
    elements.extend([faculty, Spacer(1, 0)])

    # Add diploma title - using institute style:
    diptitle = Paragraph("ΔΙΠΛΩΜΑ", institute_style)
    elements.extend([diptitle, Spacer(1, 8)])

    # Add candidate name:
    name_style = ParagraphStyle(
        "NameStyle",
        parent=getSampleStyleSheet()["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        alignment=1
    )
    name = Paragraph(candidate_name, name_style)
    elements.extend([name, Spacer(1, 3)])

    # Add body text of the degree - using body text style:
    degree_text = f"ΑΠΟ: {place_of_birth}<br/>ΣΠΟΥΔΑΣΕ<br/>\
        ΤΟ ΓΝΩΣΤΙΚΟ ΑΝΤΙΚΕΙΜΕΝΟ ΤΟΥ ΗΛΕΚΤΡΟΛΟΓΟΥ ΜΗΧΑΝΙΚΟΥ<br/>\
        ΚΑΙ ΜΗΧΑΝΙΚΟΥ ΥΠΟΛΟΓΙΣΤΩΝ<br/>ΣΤΟ ΠΑΝΕΠΙΣΤΗΜΙΟ ΠΑΤΡΩΝ<br/>\
        ΚΑΙ ΜΕΤΑ ΑΠΟ ΤΗΝ ΕΠΙΤΥΧΗ ΟΛΟΚΛΗΡΩΣΗ ΤΩΝ<br/>ΠΡΟΒΛΕΠΟΜΕΝΩΝ ΥΠΟΧΡΕΩΣΕΩΝ<br/>\
        ΑΝΑΚΗΡΥΧΘΗΚΕ ΔΙΠΛΩΜΑΤΟΥΧΟΣ<br/>ΜΕ ΒΑΘΜΟ"
    faculty = Paragraph(degree_text, body_text_style)
    elements.extend([faculty, Spacer(1, 10)])

    # Add Good-Better-Best dividing stucture - using name style:
    if diploma_mark_num >= 8.50: gbb_text = "ΑΡΙΣΤΑ"
    elif (6.50 <= diploma_mark_num <= 8.49): gbb_text = "ΛΙΑΝ ΚΑΛΩΣ"
    else : gbb_text = "ΚΑΛΩΣ"
    #elif (5.00 >= diploma_mark_num <= 6.49): gbb_text = "ΚΑΛΩΣ"
    gbb = Paragraph(gbb_text, name_style)
    elements.extend([gbb, Spacer(1, 1)])
    
    # Add diploma mark(words & Num) - using body text style:
    mark_text = f"{diploma_mark} ({diploma_mark_num})"
    mark = Paragraph(mark_text, body_text_style)
    elements.extend([mark, Spacer(1, 25)])

    # Add location and date of Cert creation:
    today = date.today()
    date01 = today.strftime("%d/%m/%Y")
    date_text = f"ΠΑΤΡΑ, {date01}"
    LocDate = Paragraph(date_text, body_text_style)
    elements.extend([LocDate, Spacer(1, 12)])

     # Add institute signatures:
    if institute_signatures_path:
        signatures = Image(institute_signatures_path, width=450, height=100)
        elements.append(signatures)

################################ PDF Design over ########################################

    # Build PDF document
    doc.build(elements)
    print(f"Certificate generated and saved at: {output_path}")

# Build funcion to extract text from certificates
def extract_certificate(pdf_path_int):
    with pdfplumber.open(pdf_path_int) as pdf:
        # Initialize variables:
        candidate_name = ""
        grad_number = ""
        place_of_birth = ""
        diploma_mark = ""
        # Extract text from each page
        for page in pdf.pages:
            # Extract Candidate Name using its position in the pdf (line count)
            candidate_name = page.extract_text().splitlines()[8]

            for line in page.extract_text().splitlines():
                # Extract Grad Number using - to locate it: (text on pdf: ΑΡΙΘΜΟΣ ΜΗΤΡΩΟΥ ΔΙΠΛΩΜΑΤΟΥΧΩΝ - _GRAD_NUM)
                if '-' in line.lower():
                    grad_number = line.split()[-1]
                # Extract Birth Location using : to locate it: (text on pdf: ΑΠΟ: _BIRTH_LOCATTION)
                if ':' in line.lower():
                    place_of_birth = line.split(maxsplit=1)[-1]
                # Extract Diploma Mark using ( to locate it: (text on pdf: _DIPLOMA_MARK (_DIPLOMA_MARK_NUM))
                elif '(' in line.lower():
                    diploma_mark =line.rsplit(maxsplit=1)[0]

        return (candidate_name, grad_number, place_of_birth, diploma_mark)