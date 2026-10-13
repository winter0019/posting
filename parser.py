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
    # Clean column headers: lowercase, strip spaces, replace spaces/hyphens with underscores
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')

    records = []
    for _, row in df.iterrows():
        # Flexible mapping supporting both your standard headers and user alternative headers
        state_code = str(row.get('state_code', row.get('state', ''))).strip().upper()
        full_name = str(row.get('full_name', row.get('name', ''))).strip().title()
        
        # Phone number handling
        phone_raw = row.get('phone_number', row.get('phone_number', row.get('phone', '')))
        phone_number = str(int(phone_raw)) if pd.notnull(phone_raw) and str(phone_raw).replace('.', '', 1).isdigit() else str(phone_raw)
        
        spouse_location = str(row.get('spouse_location', row.get('address', ''))).strip().title()
        assigned_lga = str(row.get('assigned_lga', '')).strip().title()

        if state_code and state_code != 'NAN' and full_name and full_name != 'Nan':
            records.append({
                'state_code': state_code,
                'full_name': full_name,
                'phone_number': phone_number if phone_number != 'nan' else '',
                'spouse_location': spouse_location if spouse_location != 'Nan' else '',
                'assigned_lga': assigned_lga if assigned_lga != 'Nan' else ''
            })

    return records
