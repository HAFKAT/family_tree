from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class FamilyMember(db.Model):
    __tablename__ = 'family_members'

    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    birth_year = db.Column(db.String(10), default='')
    death_year = db.Column(db.String(10), default='')
    role = db.Column(db.String(80), default='')
    generation = db.Column(db.Integer, default=1)
    bio = db.Column(db.Text, default='')
    photo = db.Column(db.String(120), default='')   # filename only
    birth_place = db.Column(db.String(120), default='')
    occupation = db.Column(db.String(120), default='')

    # Relationships stored as comma separated ids for simplicity
    parent_ids = db.Column(db.String(200), default='')  # e.g. "1,2"
    spouse_id = db.Column(db.String(20), default='')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_parent_ids(self):
        return [p for p in self.parent_ids.split(',') if p] if self.parent_ids else []

    def set_parent_ids(self, ids_list):
        self.parent_ids = ','.join(ids_list) if ids_list else ''

    def get_spouse_id(self):
        return self.spouse_id if self.spouse_id else None

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'birth_year': self.birth_year,
            'death_year': self.death_year,
            'role': self.role,
            'generation': self.generation,
            'bio': self.bio,
            'photo': self.photo,
            'birth_place': self.birth_place,
            'occupation': self.occupation,
            'parent_ids': self.get_parent_ids(),
            'spouse_id': self.spouse_id or ''
        }
