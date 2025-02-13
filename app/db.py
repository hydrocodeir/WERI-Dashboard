from app.extensions import db


class BaseModel(db.Model):
    
    __abstract__ = True
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        info={'verbose_name': 'شناسه'}
    )
    
    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        info={'verbose_name': 'تاریخ ایجاد'}
    )
    
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
        info={'verbose_name': 'تاریخ بروزرسانی'}
    )
