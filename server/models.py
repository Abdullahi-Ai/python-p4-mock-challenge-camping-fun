# models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Camper(db.Model):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    signups = db.relationship('Signup', back_populates='camper', cascade='all, delete-orphan')

    @validates('age')
    def validate_age(self, key, value):
        if not (8 <= value <= 18):
            raise ValueError("Age must be between 8 and 18")
        return value

    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Name is required")
        return value.strip()

    def to_dict(self, only=None, include=None):
        result = {col.name: getattr(self, col.name) for col in self.__table__.columns if not only or col.name in only}
        if include:
            for rel, opts in include.items():
                related_obj = getattr(self, rel)
                if isinstance(related_obj, list):
                    result[rel] = [r.to_dict(**opts) for r in related_obj]
                elif related_obj:
                    result[rel] = related_obj.to_dict(**opts)
        return result


class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)

    signups = db.relationship('Signup', back_populates='activity', cascade='all, delete-orphan')

    def to_dict(self, only=None, include=None):
        result = {col.name: getattr(self, col.name) for col in self.__table__.columns if not only or col.name in only}
        if include:
            for rel, opts in include.items():
                related_obj = getattr(self, rel)
                if isinstance(related_obj, list):
                    result[rel] = [r.to_dict(**opts) for r in related_obj]
                elif related_obj:
                    result[rel] = related_obj.to_dict(**opts)
        return result


class Signup(db.Model):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)

    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)

    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='signups')

    @validates('time')
    def validate_time(self, key, value):
        if not (0 <= value <= 23):
            raise ValueError("Time must be between 0 and 23")
        return value

    def to_dict(self, only=None, include=None):
        result = {col.name: getattr(self, col.name) for col in self.__table__.columns if not only or col.name in only}
        if include:
            for rel, opts in include.items():
                related_obj = getattr(self, rel)
                if isinstance(related_obj, list):
                    result[rel] = [r.to_dict(**opts) for r in related_obj]
                elif related_obj:
                    result[rel] = related_obj.to_dict(**opts)
        return result
