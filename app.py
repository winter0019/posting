import os
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
from models import db, MarriedCorpsMember
from parser import parse_corps_member_excel, assign_zone_to_lga
from pdf_generator import generate_zonal_pdf

app = Flask(__name__)

# Database Configuration (PostgreSQL / SQLite fallback)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///katsina_nysc.db')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    # Renders the mobile and desktop friendly web interface
    return render_template('index.html')

@app.route('/api/upload-married-corpers', methods=['POST'])
def upload_excel():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file and file.filename.endswith(('.xlsx', '.xls')):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            records = parse_corps_member_excel(file_path)
            processed_count = 0

            for rec in records:
                zone = assign_zone_to_lga(rec['assigned_lga'])
                
                # Upsert based on state_code
                existing = MarriedCorpsMember.query.filter_by(state_code=rec['state_code']).first()
                if existing:
                    existing.full_name = rec['full_name']
                    existing.phone_number = rec.get('phone_number')
                    existing.spouse_location = rec.get('spouse_location')
                    existing.current_ppa = rec.get('current_ppa')
                    existing.assigned_lga = rec['assigned_lga']
                    existing.zone = zone
                else:
                    new_member = MarriedCorpsMember(
                        state_code=rec['state_code'],
                        full_name=rec['full_name'],
                        phone_number=rec.get('phone_number'),
                        spouse_location=rec.get('spouse_location'),
                        current_ppa=rec.get('current_ppa'),
                        assigned_lga=rec['assigned_lga'],
                        zone=zone
                    )
                    db.session.add(new_member)
                processed_count += 1

            db.session.commit()
            os.remove(file_path)

            return jsonify({
                "message": f"Successfully processed and synced {processed_count} records.",
                "total_records": processed_count
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Invalid file format. Please upload an Excel (.xlsx or .xls) file."}), 400

@app.route('/api/married-corpers', methods=['GET'])
def get_married_corpers():
    zone = request.args.get('zone')
    lga = request.args.get('lga')
    
    query = MarriedCorpsMember.query
    if zone and zone != "All":
        query = query.filter_by(zone=zone)
    if lga:
        query = query.filter_by(assigned_lga=lga)
        
    results = query.all()
    return jsonify({
        "status": "success",
        "count": len(results),
        "data": [r.to_dict() for r in results]
    }), 200

@app.route('/api/download-report/<zone>', methods=['GET'])
def download_report(zone):
    if zone == "All":
        records = MarriedCorpsMember.query.all()
    else:
        records = MarriedCorpsMember.query.filter_by(zone=zone).all()
        
    records_dict = [r.to_dict() for r in records]
    pdf_path = generate_zonal_pdf(zone, records_dict)
    return send_file(pdf_path, as_attachment=True, download_name=f"{zone}_Zone_Married_Corpers.pdf")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
