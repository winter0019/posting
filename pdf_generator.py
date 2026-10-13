from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_zonal_pdf(zone_name, records, output_path="zonal_posting_report.pdf"):
    doc = SimpleDocTemplate(output_path, pagesize=landscape(letter),
                            rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading1'], fontSize=16, leading=20, alignment=1, textColor=colors.HexColor('#1E3A8A')
    )
    subtitle_style = ParagraphStyle(
        'SubTitleStyle', parent=styles['Normal'], fontSize=11, leading=14, alignment=1, textColor=colors.HexColor('#4B5563')
    )

    story.append(Paragraph("NATIONAL YOUTH SERVICE CORPS - KATSINA STATE", title_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph(f"<b>ZONAL POSTING REPORT: MARRIED CORPS MEMBERS ({zone_name.upper()} ZONE)</b>", subtitle_style))
    story.append(Spacer(1, 15))

    table_data = [["S/N", "State Code", "Full Name", "Spouse Location", "Assigned LGA", "Current PPA", "Phone"]]
    
    for idx, record in enumerate(records, start=1):
        table_data.append([
            str(idx),
            record.get('state_code', ''),
            record.get('full_name', ''),
            record.get('spouse_location', ''),
            record.get('assigned_lga', ''),
            record.get('current_ppa', ''),
            record.get('phone_number', '')
        ])

    col_widths = [30, 95, 130, 130, 100, 150, 85]
    t = Table(table_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
    ]))

    story.append(t)
    doc.build(story)
    return output_path
