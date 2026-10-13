from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MarriedCorpsMember(db.Model):
    __tablename__ = 'married_corps_members'
    id = db.Column(db.Integer, primary_key=True)
    state_code = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    spouse_location = db.Column(db.String(150), nullable=True)
    current_ppa = db.Column(db.String(150), nullable=True)
    assigned_lga = db.Column(db.String(100), nullable=False)
    zone = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "state_code": self.state_code,
            "full_name": self.full_name,
            "gender": self.gender,
            "phone_number": self.phone_number,
            "spouse_location": self.spouse_location,
            "current_ppa": self.current_ppa,
            "assigned_lga": self.assigned_lga,
            "zone": self.zone
        }
