from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import enum
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    otp = db.Column(db.String(6), nullable=True)
    otp_created_at = db.Column(db.DateTime, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_employer = db.Column(db.Boolean, default=False)
    # Role-based access: 'admin', 'manager', 'viewer', etc.
    role = db.Column(db.String(20), default='viewer', nullable=False)
    
    # New fields for profile completion
    full_name = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    resume_path = db.Column(db.String(255), nullable=True)
    
    # Foreign key for company association (for employers)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    
    # Relationships
    applications = db.relationship('JobApplication', back_populates='user', lazy='dynamic')
    jobs = db.relationship('Job', back_populates='creator', lazy=True)
    # Fixed relationship - user can be associated with a company
    company = db.relationship('Company', foreign_keys=[company_id], back_populates='employees')
    # Companies owned by this user (for company owners)
    owned_companies = db.relationship('Company', foreign_keys='Company.owner_id', back_populates='owner')
    skills = db.relationship('Skill', secondary='user_skills', lazy='subquery',
                           backref=db.backref('users', lazy=True))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role_name):
        return self.role == role_name
    
    # Backward compatibility property
    @property
    def companies(self):
        return self.owned_companies
    
    def __repr__(self):
        return f'<User {self.username}>'


class JobType(enum.Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    FREELANCE = "Freelance"
    INTERNSHIP = "Internship"


class ExperienceLevel(enum.Enum):
    ENTRY = "Entry Level"
    JUNIOR = "Junior"
    MID = "Mid-Level"
    SENIOR = "Senior"
    LEAD = "Lead"
    EXECUTIVE = "Executive"


class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    website = db.Column(db.String(200), nullable=True)
    logo_url = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    jobs = db.relationship('Job', back_populates='company', lazy='dynamic')
    # Company owner (the user who created/owns the company)
    owner = db.relationship('User', foreign_keys=[owner_id], back_populates='owned_companies')
    # Employees associated with this company
    employees = db.relationship('User', foreign_keys='User.company_id', back_populates='company')
    
    def __repr__(self):
        return f'<Company {self.name}>'


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)
    icon_class = db.Column(db.String(100), nullable=True)  # e.g., 'fa-code', 'fa-bullhorn'
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    jobs = db.relationship('Job', back_populates='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=True)
    salary_min = db.Column(db.Integer, nullable=True)
    salary_max = db.Column(db.Integer, nullable=True)
    job_type = db.Column(db.Enum(JobType), nullable=False)
    experience_level = db.Column(db.Enum(ExperienceLevel), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_deleted = db.Column(db.Boolean, default=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    company = db.relationship('Company', back_populates='jobs')
    category = db.relationship('Category', back_populates='jobs')
    creator = db.relationship('User', back_populates='jobs')
    applications = db.relationship('JobApplication', back_populates='job', lazy='dynamic')
    skills = db.relationship('Skill', secondary='job_skills')
    
    def __repr__(self):
        return f'<Job {self.title} at {self.company.name}>'


class ApplicationStatus(enum.Enum):
    APPLIED = "Applied"
    REVIEWING = "Reviewing"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"


class JobApplication(db.Model):
    __tablename__ = 'job_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    resume_url = db.Column(db.String(255), nullable=True)
    cover_letter = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(ApplicationStatus), default=ApplicationStatus.APPLIED)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_withdraw = db.Column(db.Boolean, default=False)
    
    # Relationships
    user = db.relationship('User', back_populates='applications')
    job = db.relationship('Job', back_populates='applications')
    
    def __repr__(self):
        return f'<Application {self.id} - {self.user.username} for {self.job.title}>'


class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    # Many-to-many relationship with jobs
    job_skills = db.relationship('JobSkill', back_populates='skill')
    
    def __repr__(self):
        return f'<Skill {self.name}>'


class JobSkill(db.Model):
    __tablename__ = 'job_skills'
    
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), primary_key=True)
    is_required = db.Column(db.Boolean, default=True)
    
    # Relationships
    job = db.relationship('Job')
    skill = db.relationship('Skill', back_populates='job_skills')
    
    def __repr__(self):
        return f'<JobSkill {self.job.title} - {self.skill.name}>'


# User-Skill association table
user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id'), primary_key=True)
)