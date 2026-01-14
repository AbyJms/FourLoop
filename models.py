from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance (initialized in app.py)
db = SQLAlchemy()


# =========================
# USERS
# =========================
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'player' or 'seeker'
    tokens = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<User id={self.id} username={self.username} role={self.role} tokens={self.tokens}>"



# =========================
# JOBS (posted by seekers)
# =========================
class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    seeker_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)

    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    people_required = db.Column(db.Integer, nullable=False)
    duration_hours = db.Column(db.Integer, nullable=False)
    tokens_reward = db.Column(db.Integer, nullable=False)

    status = db.Column(db.String(20), nullable=False, default="published")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Job id={self.id} title={self.title} seeker_id={self.seeker_id} status={self.status}>"



# =========================
# JOB PARTICIPANTS
# =========================
class JobParticipant(db.Model):
    __tablename__ = "job_participants"

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<JobParticipant job_id={self.job_id} user_id={self.user_id} completed={self.completed}>"



# =========================
# REDEMPTIONS
# =========================
class Redemption(db.Model):
    __tablename__ = "redemptions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    reward_type = db.Column(db.Text, nullable=False)
    used = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Redemption id={self.id} user_id={self.user_id} reward_type={self.reward_type} used={self.used}>"
