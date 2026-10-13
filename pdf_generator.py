import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_zonal_pdf(zone_name, records):
    pdf_dir = "reports"
    os.makedirs(pdf_dir, exist_ok=True)
    filename = f"{zone_name.lower().replace(' ', '_')}_zone_married_corpers.pdf"
    file_path = os.path.join(pdf_dir, filename)

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=25,
        leftMargin=25,
        topMargin=30,
        bottomMargin=30
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        alignment=1, # Center
        textColor=colors.HexColor('#006633')
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=colors.HexColor('#333333')
    )
    
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=colors.HexColor('#555555')
    )
    
    # Cell text style to ensure wrapping
    cell_style = ParagraphStyle(
        'CellStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#222222')
    )
    
    header_cell_style = ParagraphStyle(
        'HeaderCellStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    # Header details
    elements.append(Paragraph("NATIONAL YOUTH SERVICE CORPS - KATSINA STATE", title_style))
    elements.append(Spacer(1, 4))
    
    report_title = f"ZONAL POSTING REPORT: MARRIED CORPS MEMBERS ({zone_name.upper()} ZONE)"
    if zone_name.lower() == 'all':
        report_title = "ZONAL POSTING REPORT: MARRIED CORPS MEMBERS (ALL ZONES)"
    
    elements.append(Paragraph(report_title, subtitle_style))
    elements.append(Spacer(1, 4))
    
    # Calculate Statistics per Zone
    zone_counts = {"Katsina": 0, "Daura": 0, "Dutsinma": 0, "Funtua": 0, "Pending": 0}
    for r in records:
        z = r.get('zone', 'Pending')
        if z in zone_counts:
            zone_counts[z] += 1
        else:
            zone_counts['Pending'] += 1
            
    total_count = len(records)
    stats_text = f"Total Records: {total_count}  |  Katsina: {zone_counts['Katsina']}  |  Daura: {zone_counts['Daura']}  |  Dutsinma: {zone_counts['Dutsinma']}  |  Funtua: {zone_counts['Funtua']}"
    elements.append(Paragraph(stats_text, meta_style))
    elements.append(Spacer(1, 10))

    # Table Data Structure with Wrapped Paragraphs
    table_data = [
        [
            Paragraph("S/N", header_cell_style),
            Paragraph("State Code", header_cell_style),
            Paragraph("Full Name", header_cell_style),
            Paragraph("Spouse Location", header_cell_style),
            Paragraph("Assigned LGA", header_cell_style),
            Paragraph("Current PPA", header_cell_style),
            Paragraph("Phone", header_cell_style)
        ]
    ]

    for idx, r in enumerate(records, start=1):
        table_data.append([
            Paragraph(str(idx), cell_style),
            Paragraph(str(r.get('state_code', '')), cell_style),
            Paragraph(str(r.get('full_name', '')), cell_style),
            Paragraph(str(r.get('spouse_location', '')), cell_style),
            Paragraph(str(r.get('assigned_lga', '')), cell_style),
            Paragraph(str(r.get('current_ppa', 'None')), cell_style),
            Paragraph(str(r.get('phone_number', '')), cell_style)
        ])

    # Adjusted A4 Table Column Widths (Total width fits page safely)
    col_widths = [22, 60, 95, 130, 75, 70, 65]
    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#006633')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]),
    ]))

    elements.append(t)
    doc.build(elements)
    return file_path
