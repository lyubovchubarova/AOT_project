from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Information(db.Model):
    __tablename__ = "post_data"

    full_sent = db.Column('full_sent', db.Text)
    tokenize_sent = db.Column('tokenize_sent', db.Text)
    pos_tokens = db.Column('pos_tokens', db.Text)
    bloggers = db.Column('bloggers', db.Text)