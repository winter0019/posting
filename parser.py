import pandas as pd
import os

ZONAL_MAPPING = {
    "Katsina": ["Katsina", "Batagarawa", "Rimi", "Jibia", "Kaita", "Charanchi"],
    "Daura": ["Daura", "Mashi", "Mani", "Dutsi", "Bindawa", "Zango", "Sandamu", "Baure"],
    "Dutsinma": ["Dutsinma", "Safana", "Batsari", "Kankia", "Kusada", "Ingawa"],
    "Funtua": ["Funtua", "Bakori", "Danja", "Faskari", "Kankara", "Sabuwa", "Malumfashi", "Kafur"]
}

def assign_zone_to_lga(lga_name):
    if not lga_name or str(lga_name).lower() == 'nan':
        return "Pending"
    
    cleaned_lga = str(lga_name).strip().title()
    for zone, lgas in ZONAL_MAPPING.items():
        if cleaned_lga in [l.title() for l in lgas]:
            return zone
    return "Pending"

def parse_corps_member_excel(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')

    records = []
    for _, row in df.iterrows():
        state_code = str(row.get('statecode', row.get('state_code', row.get('state', '')))).strip().upper()
        
        # Look for full name or name column; if absent, check if there's any other text column, else default cleanly
        full_name = str(row.get('full_name', row.get('name', ''))).strip().title()
        if not full_name or full_name == 'Nan':
            full_name = "Not Provided in Excel"
        
        gender = str(row.get('sex', row.get('gender', ''))).strip().title()
        if gender == 'Nan':
            gender = ''

        phone_raw = row.get('phone_number', row.get('phone', ''))
        phone_number = str(int(phone_raw)) if pd.notnull(phone_raw) and str(phone_raw).replace('.', '', 1).isdigit() else str(phone_raw)
        
        spouse_location = str(row.get('permanent_address', row.get('spouse_location', row.get('address', '')))).strip().title()
        assigned_lga = str(row.get('assigned_lga', '')).strip().title()

        origin = str(row.get('origin', '')).strip().title()
        course = str(row.get('course', '')).strip()
        grade = str(row.get('grade', '')).strip()

        if state_code and state_code != 'NAN':
            records.append({
                'state_code': state_code,
                'full_name': full_name if full_name != 'Not Provided In Excel' else f"Member ({state_code})",
                'gender': gender if gender != 'Nan' else '',
                'phone_number': phone_number if phone_number != 'nan' else '',
                'spouse_location': spouse_location if spouse_location != 'Nan' else '',
                'assigned_lga': assigned_lga if assigned_lga != 'Nan' else '',
                'origin': origin if origin != 'Nan' else '',
                'course': course if course != 'nan' else '',
                'grade': grade if grade != 'nan' else ''
            })

    return records
