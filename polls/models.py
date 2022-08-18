from application.extensions import db


class Poll(db.Base):
    __tablename__ = "polls"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
