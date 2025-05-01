from app.extensions import db
from sqlalchemy.orm import relationship
from app.models.user import User

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    is_done = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='tasks')
