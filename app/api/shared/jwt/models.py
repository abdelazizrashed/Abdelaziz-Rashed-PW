from app.api.shared.db_man.services import db


class TokenBlocklistModel(db.Model):

    __tablename__ = 'TokenBlocklist'

    id = db.Column(
        db.Integer,
        primary_key = True
    )
    jti = db.Column(
        db.String(36),
        nullable = False
    )
    created_at = db.Column(
        db.DateTime,
        nullable = False
    )