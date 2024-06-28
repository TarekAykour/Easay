from PyPDF2 import PdfReader, PdfWriter

# Load the original PDF
input_path = "/mnt/data/resume-1.pdf"
output_path = "/mnt/data/resume-1-updated.pdf"
reader = PdfReader(input_path)
writer = PdfWriter()

# Read the original content
original_text = """
Tarek Aykour
tarek_aykour@hotmail.com · https://www.linkedin.com/in/tarekaykour/

Educatie

Inholland Rotterdam, Zuid-holland
HBO Communicatie sep 2022 - Heden

Scheepvaart en Transport College Rotterdam, Zuid-Holland
MBO4 Manager Havenlogistiek sep 2017 - jun 2020

Werkervaring

Jumbo Supermarkt Rotterdam, Zuid-Holland
AGF Medewerker sep 2017 - aug 2018

Thuisbezorgd Rotterdam, Zuid-Holland
Maaltijd Bezorger aug 2018 - aug 2019

Hamburg Süd Rotterdam, Zuid-Holland
Customer Service Import sep 2019 - feb 2020

Vaardigheden

Communicatievaardigheden: Communicatie, Samenwerken, Contentstrategie, SEO

Designvaardigheden: Figma, Photoshop, Blender, Premiere Pro, After Effects

Programmeervaardigheden: Python, Javascript, HTML, CSS, C++, Git, Docker

Talen: Nederlands, Engels, Spaans, Portugees

Certificaten

IBM Data Analyst IBM jun 2024

IBM Front-End Developer IBM jun 2024

IBM AI Developer IBM jun 2024
"""

# Updated content with more space under each section
updated_text = """
Tarek Aykour
tarek_aykour@hotmail.com · https://www.linkedin.com/in/tarekaykour/

### Educatie

**Inholland Rotterdam, Zuid-holland**  
HBO Communicatie  
sep 2022 - Heden  

**Scheepvaart en Transport College Rotterdam, Zuid-Holland**  
MBO4 Manager Havenlogistiek  
sep 2017 - jun 2020  


### Werkervaring

**Jumbo Supermarkt Rotterdam, Zuid-Holland**  
AGF Medewerker  
sep 2017 - aug 2018  

**Thuisbezorgd Rotterdam, Zuid-Holland**  
Maaltijd Bezorger  
aug 2018 - aug 2019  

**Hamburg Süd Rotterdam, Zuid-Holland**  
Customer Service Import  
sep 2019 - feb 2020  


### Vaardigheden

**Communicatievaardigheden:**  
Communicatie, Samenwerken, Contentstrategie, SEO  

**Designvaardigheden:**  
Figma, Photoshop, Blender, Premiere Pro, After Effects  

**Programmeervaardigheden:**  
Python, Javascript, HTML, CSS, C++, Git, Docker  

**Talen:**  
Nederlands, Engels, Spaans, Portugees  


### Certificaten

**IBM Data Analyst IBM**  
jun 2024  

**IBM Front-End Developer IBM**  
jun 2024  

**IBM AI Developer IBM**  
jun 2024  
"""

# Add the updated text to a new PDF page
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Create a PDF in memory with the updated content
from io import BytesIO
packet = BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.drawString(50, 750, "Tarek Aykour")
can.drawString(50, 735, "tarek_aykour@hotmail.com · https://www.linkedin.com/in/tarekaykour/")

# Draw the rest of the text
text = can.beginText(50, 710)
text.setFont("Helvetica", 12)
for line in updated_text.split('\n'):
    text.textLine(line)
can.drawText(text)
can.save()

# Move to the beginning of the StringIO buffer
packet.seek(0)

# Read the PDF created in memory
new_pdf = PdfReader(packet)

# Add the new page with the updated text to the writer
writer.add_page(new_pdf.pages[0])

# Save the updated PDF
with open(output_path, "wb") as output_pdf:
    writer.write(output_pdf)

output_path
