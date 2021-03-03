from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)



class Disc(db.Model):
    """Disc Model"""

    __tablename__ = "discs"

    id = db.Column(db.Integer, 
                    primary_key=True, 
                    autoincrement=True)

    name = db.Column(db.Text, 
                    nullable=False)

    plastic = db.Column(db.Text, 
                    default="N/A")

    difficulty = db.Column(db.Float)

    speed = db.Column(db.Float)

    glide = db.Column(db.Float)

    high_stability = db.Column(db.Float)

    low_stability = db.Column(db.Float)

    image_url = db.Column(db.Text)

    company_name = db.Column(db.Text, 
                    db.ForeignKey('companies.name'))
                    

    company = db.relationship('Company', backref='discs')

    def __repr__(self):
        return f"<Disc: {self.name} Company: {self.company_name}>"

    def serialize(self):
        serialized = {"name": self.name,
                    "plastic": self.plastic,
                    "difficulty": self.difficulty,
                    "speed": self.speed,
                    "glide": self.glide,
                    "high_stability": self.high_stability,
                    "low_stability": self.low_stability,
                    "image_url": self.image_url,
                    "compaby_name": self.company_name}
        return serialized


class Company(db.Model):
    """Company Model"""

    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    

    def __repr__(self):
        return f"<Company {self.name}>"

    def serialize(self):
        serialized = {"name": self.name}
        return serialized

