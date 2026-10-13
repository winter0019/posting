import pandas as pd
import os

ZONAL_MAPPING = {
    "Katsina": ["Katsina", "Batagarawa", "Rimi", "Charanchi", "Kurfi"],
    "Daura": ["Daura", "Mai'Adua", "Zango", "Sandamu", "Baure", "Mani", "Mashi", "Dutsi"],
    "Dutsinma": ["Dutsinma", "Safana", "Batsari", "Kankia", "Kusada", "Ingawa"],
    "Funtua": ["Funtua", "Bakori", "Danja", "Faskari", "Kankara", "Sabuwa", "Malumfashi"]
}

def assign_zone_to_lga(lga_name):
    for zone, lgas in ZONAL_MAPPING.items():
        if lga_name in lgas:
            return zone
    return "Unassigned"

def parse_corps_member_excel(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    required_columns = ['state_code', 'full_name', 'phone_number', 'spouse_location', 'assigned_lga']
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in Excel sheet: {missing_cols}")

    df['state_code'] = df['state_code'].astype(str).str.strip().str.upper()
    df['full_name'] = df['full_name'].astype(str).str.strip().str.title()
    df['phone_number'] = df['phone_number'].astype(str).str.strip()
    df['spouse_location'] = df['spouse_location'].astype(str).str.strip().str.title()
    df['assigned_lga'] = df['assigned_lga'].astype(str).str.strip().str.title()

    df = df.dropna(subset=['state_code'])
    df = df[df['state_code'] != 'NAN']

    records = df.to_dict(orient='records')
    return records
