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
        rightMargin=30,
        leftMargin=30,
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

    # Table Data Structure
    table_data = [
        ["S/N", "State Code", "Full Name", "Spouse Location", "Assigned LGA", "Current PPA", "Phone"]
    ]

    for idx, r in enumerate(records, start=1):
        table_data.append([
            str(idx),
            str(r.get('state_code', '')),
            str(r.get('full_name', '')),
            str(r.get('spouse_location', '')),
            str(r.get('assigned_lga', '')),
            str(r.get('current_ppa', '')),
            str(r.get('phone_number', ''))
        ])

    # Table Styling for A4 Page Fitting
    col_widths = [25, 65, 110, 100, 75, 80, 75]
    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#006633')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
    ]))

    elements.append(t)
    doc.build(elements)
    return file_path
