from app import db

class Store(db.Model):
    __tablename__ = 'store'
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, nullable=False)
    timezone = db.Column(db.String(255), nullable=False)

class PollData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.store_id'), nullable=False)
    timestamp_utc = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(10), nullable=False)

class BusinessHours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.store_id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    start_time_local = db.Column(db.String(10), nullable=False)
    end_time_local = db.Column(db.String(10), nullable=False)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.String(50), unique=True, nullable=False)
    store_id = db.Column(db.Integer, nullable=False)
    uptime_last_hour = db.Column(db.Integer)
    uptime_last_day = db.Column(db.Integer)
    uptime_last_week = db.Column(db.Integer)
    downtime_last_hour = db.Column(db.Integer)
    downtime_last_day = db.Column(db.Integer)
    downtime_last_week = db.Column(db.Integer)

