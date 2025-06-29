import os
import sys
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, session, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
from models import db, User, Job, Company, Category, JobType, ExperienceLevel, Skill, JobSkill, JobApplication, ApplicationStatus
from datetime import datetime, timedelta
import random
import string
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from hashids import Hashids

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure database with proper Render support
def get_database_url():
    """Get the correct database URL for the environment"""
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        print(f"🔗 Found DATABASE_URL: {database_url[:50]}...")
        # Render provides postgres:// but SQLAlchemy needs postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
            print("🔄 Converted postgres:// to postgresql://")
        return database_url
    
    print("⚠️ No DATABASE_URL found, using SQLite fallback")
    # Fallback for local development
    return 'sqlite:///instance/jobconnect.db'

# Set configuration
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print(f"🗄️ Database URI: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")

# Initialize database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize Hashids for obfuscated IDs
hashids = Hashids(salt=app.secret_key, min_length=8)
app.jinja_env.globals['hashids'] = hashids

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Role-based access control decorator ---
from functools import wraps
from flask import abort

def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(role_name):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
    
# Root route to show the homepage
@app.route('/')
def index():
    # Get featured jobs
    featured_jobs = Job.query.filter_by(is_active=True).filter(Job.is_deleted==False).join(Category).filter(Category.is_active == True).order_by(Job.created_at.desc()).limit(6).all()
    
    # Get all categories with their job counts
    categories = db.session.query(
        Category,
        db.func.count(Job.id).label('job_count')
    ).\
    outerjoin(Job, (Category.id == Job.category_id) & (Job.is_active == True) & (Job.is_deleted == False) & (Category.is_active == True)).\
    group_by(Category.id).\
    all()
    
    # Convert SQLAlchemy Row objects to dictionaries
    categories_with_counts = []
    for category, job_count in categories:
        categories_with_counts.append({
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'icon_class': category.icon_class,
            'is_active': category.is_active,
            'job_count': job_count
        })
    
    return render_template('index.html', 
                         jobs=featured_jobs, 
                         categories=categories_with_counts,
                         current_year=datetime.now().year)

@app.route('/jobs')
def jobs():
    # Get query parameters
    selected_types = request.args.getlist('job_type')
    selected_experience = request.args.getlist('experience')
    query = request.args.get('query', '')
    location = request.args.get('location', '')

    # Base query
    jobs_query = Job.query.filter_by(is_active=True).filter(Job.is_deleted==False).join(Category).filter(Category.is_active == True)

    # Apply filters
    if selected_types:
        jobs_query = jobs_query.filter(Job.job_type.in_([JobType(t) for t in selected_types]))
    
    if selected_experience:
        jobs_query = jobs_query.filter(Job.experience_level.in_([ExperienceLevel(e) for e in selected_experience]))

    if query:
        jobs_query = jobs_query.filter(
            db.or_(
                Job.title.ilike(f'%{query}%'),
                Job.description.ilike(f'%{query}%'),
                Company.name.ilike(f'%{query}%')
            )
        ).join(Job.company)
    
    if location:
        jobs_query = jobs_query.filter(Job.location.ilike(f'%{location}%'))

    # Get all jobs with filters
    all_jobs = jobs_query.order_by(Job.created_at.desc()).all()
    
    # Get all job types and experience levels for filters
    job_types = [member.value for member in JobType]
    experience_levels = [member.value for member in ExperienceLevel]
    
    # Get categories for the navigation
    categories = Category.query.filter_by(is_active=True).all()
    
    return render_template('jobs.html',
                         jobs=all_jobs,
                         job_types=job_types,
                         experience_levels=experience_levels,
                         selected_types=selected_types,
                         selected_experience=selected_experience,
                         query=query,
                         location=location,
                         categories=categories,
                         current_year=datetime.now().year)

@app.route('/jobs/search')
def search_jobs():
    # Get query parameters
    selected_types = request.args.getlist('job_type')
    selected_experience = request.args.getlist('experience')
    query = request.args.get('query', '')
    location = request.args.get('location', '')
    
    # Base query
    jobs_query = Job.query.filter_by(is_active=True).filter(Job.is_deleted==False).join(Category).filter(Category.is_active == True)
    
    # Apply filters
    if selected_types:
        jobs_query = jobs_query.filter(Job.job_type.in_([JobType(t) for t in selected_types]))
    
    if selected_experience:
        jobs_query = jobs_query.filter(Job.experience_level.in_([ExperienceLevel(e) for e in selected_experience]))

    if query:
        jobs_query = jobs_query.filter(
            db.or_(
                Job.title.ilike(f'%{query}%'),
                Job.description.ilike(f'%{query}%'),
                Company.name.ilike(f'%{query}%')
            )
        ).join(Job.company)
    
    if location:
        jobs_query = jobs_query.filter(Job.location.ilike(f'%{location}%'))
    
    # Get results and filter options
    jobs = jobs_query.order_by(Job.created_at.desc()).all()
    job_types = [member.value for member in JobType]
    experience_levels = [member.value for member in ExperienceLevel]
    
    # Get categories for the navigation
    categories = Category.query.filter_by(is_active=True).all()
    
    return render_template('jobs.html',
                         jobs=jobs,
                         job_types=job_types,
                         experience_levels=experience_levels,
                         selected_types=selected_types,
                         selected_experience=selected_experience,
                         query=query,
                         location=location,
                         categories=categories,
                         current_year=datetime.now().year)

@app.route('/categories/<int:category_id>')
def category_jobs(category_id):
    from flask import request
    category = Category.query.get_or_404(category_id)
    jobs_query = Job.query.filter_by(category_id=category_id).filter(Job.is_deleted==False).filter(Job.is_active==True)
    # Job Type filter (multi-select)
    job_types = request.args.getlist('job_type')
    if job_types:
        jobs_query = jobs_query.filter(Job.job_type.in_(job_types))
    # Experience Level filter (multi-select)
    experience_levels = request.args.getlist('experience')
    if experience_levels:
        jobs_query = jobs_query.filter(Job.experience_level.in_(experience_levels))
    # Salary filter (minimum)
    salary_min = request.args.get('salary', type=int)
    if salary_min:
        jobs_query = jobs_query.filter(Job.salary >= salary_min)
    jobs = jobs_query.order_by(Job.created_at.desc()).all()
    return render_template('category_jobs.html', category=category, jobs=jobs)

@app.route('/categories')
@login_required
def categories():
    from models import Category
    categories = Category.query.filter_by(is_active=True).all()
    return render_template('categories.html', categories=categories)

# Job listing routes
@app.route('/jobs/<job_hashid>', methods=['GET', 'POST'])
def job_detail(job_hashid):
    decoded = hashids.decode(job_hashid)
    if not decoded:
        abort(404)
    job_id = decoded[0]
    job = Job.query.get_or_404(job_id)
    
    # Get required and preferred skills
    required_skills = db.session.query(Skill).join(JobSkill).filter(
        JobSkill.job_id == job_id,
        JobSkill.is_required == True
    ).all()
    
    preferred_skills = db.session.query(Skill).join(JobSkill).filter(
        JobSkill.job_id == job_id,
        JobSkill.is_required == False
    ).all()
    
    # Check if the user has already applied for this job
    has_applied = False
    application = None
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        application = JobApplication.query.filter_by(
            user_id=current_user.id,
            job_id=job_id
        ).first()
        has_applied = application is not None

    # Handle job application submission
    if request.method == 'POST' and current_user.is_authenticated and not has_applied:
        resume = request.files.get('resume')
        cover_letter = request.form.get('cover_letter')
        if not resume or resume.filename == '':
            flash('Resume is required.', 'error')
            return redirect(request.url)
        if not allowed_file(resume.filename, {'pdf', 'doc', 'docx'}):
            flash('Invalid file type. Only PDF, DOC, DOCX allowed.', 'error')
            return redirect(request.url)
        filename = secure_filename(f"{current_user.id}_{job_id}_{resume.filename}")
        resume.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Create job application with correct field names
        new_application = JobApplication(
            user_id=current_user.id,
            job_id=job_id,
            resume_url=filename,
            cover_letter=cover_letter,
            status=ApplicationStatus.APPLIED,
            applied_at=datetime.utcnow()
        )
        db.session.add(new_application)
        db.session.commit()
        flash('Your application has been submitted!', 'success')
        return redirect(url_for('applications'))
    
    return render_template('job_detail.html', 
                          job=job, 
                          required_skills=required_skills,
                          preferred_skills=preferred_skills,
                          has_applied=has_applied)

@app.route('/companies/<int:company_id>')
def company_detail(company_id):
    company = Company.query.get_or_404(company_id)
    jobs = Job.query.filter_by(company_id=company_id, is_active=True).filter(Job.is_deleted==False).join(Category).filter(Category.is_active == True).all()
    
    return render_template('company_detail.html', company=company, jobs=jobs)

# API endpoint for job search (for AJAX requests)
@app.route('/api/jobs/search')
def search_jobs_api():
    search_query = request.args.get('query', '')
    location = request.args.get('location', '')
    
    jobs_query = Job.query.filter(Job.is_active == True).filter(Job.is_deleted==False).join(Category).filter(Category.is_active == True)
    
    if search_query:
        jobs_query = jobs_query.filter(Job.title.ilike(f'%{search_query}%') | 
                                      Company.name.ilike(f'%{search_query}%'))
    
    if location:
        jobs_query = jobs_query.filter(Job.location.ilike(f'%{location}%'))
    
    jobs = jobs_query.join(Job.company).order_by(Job.created_at.desc()).limit(10).all()
    
    results = []
    for job in jobs:
        results.append({
            'id': job.id,
            'title': job.title,
            'company': job.company.name,
            'location': job.location,
            'job_type': job.job_type.value,
            'url': url_for('job_detail', job_hashid=hashids.encode(job.id))
        })
    
    return jsonify(results)

# Update the index route to show featured jobs and handle authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please provide both email and password.', 'error')
            return redirect(url_for('login'))
            
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Successfully logged in!', 'success')
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html', current_year=datetime.now().year)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        is_employer = request.form.get('is_employer', 'false') == 'true'

        if not email or not password or not confirm_password:
            flash('All fields are required', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))

        # Create new user
        user = User(
            email=email,
            is_employer=is_employer,
            is_verified=True  # Auto-verify since we're not using OTP
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Log in the user
        login_user(user)
        flash('Registration successful!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', current_year=datetime.now().year)

@app.route('/complete_profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    if request.method == 'POST':
        # Get form data
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        is_employer = request.form.get('is_employer') == 'true'
        
        # Update user information
        current_user.full_name = full_name
        current_user.email = email
        current_user.is_employer = is_employer
        
        # Handle employee-specific data
        if not is_employer:
            bio = request.form.get('bio')
            skills = request.form.get('skills')
            
            current_user.bio = bio
            
            # Handle resume upload if provided
            if 'resume' in request.files and request.files['resume'].filename:
                resume_file = request.files['resume']
                if resume_file and allowed_file(resume_file.filename, {'pdf'}):
                    filename = secure_filename(f"{current_user.id}_{resume_file.filename}")
                    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    
                    # Ensure upload directory exists
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    
                    resume_file.save(resume_path)
                    current_user.resume_path = filename
                else:
                    flash('Invalid resume file. Please upload a PDF file.', 'error')
            
            # Save skills
            if skills:
                # Clear existing skills
                current_user.skills = []
                
                # Add new skills
                skill_list = [s.strip() for s in skills.split(',')]
                for skill_name in skill_list:
                    # Check if skill exists
                    skill = Skill.query.filter_by(name=skill_name).first()
                    if not skill:
                        # Create new skill
                        skill = Skill(name=skill_name)
                        db.session.add(skill)
                
                    # Add skill to user (would need a user_skills table)
                    # This is a placeholder - you'll need to implement the relationship
            
        # Handle employer-specific data
        else:
            company_name = request.form.get('company_name')
            company_website = request.form.get('company_website')
            company_description = request.form.get('company_description')
            
            # Check if company already exists
            company = Company.query.filter_by(name=company_name).first()
            if not company:
                company = Company(
                    name=company_name,
                    website=company_website,
                    description=company_description,
                    owner_id=current_user.id
                )
                db.session.add(company)
                db.session.flush()  # Get the ID without committing
            
            # Associate user with company
            current_user.company_id = company.id
            
            # Handle job posting if provided
            job_title = request.form.get('job_title')
            job_description = request.form.get('job_description')
            job_skills = request.form.get('job_skills')
            job_type = request.form.get('job_type')
            job_location = request.form.get('job_location')
            
            if job_title and job_description:
                # Create new job
                job = Job(
                    title=job_title,
                    description=job_description,
                    location=job_location,
                    job_type=JobType[job_type],
                    company_id=company.id,
                    user_id=current_user.id
                )
                db.session.add(job)
                db.session.flush()  # Get the ID without committing
                
                # Add skills to job
                if job_skills:
                    skill_list = [s.strip() for s in job_skills.split(',')]
                    for skill_name in skill_list:
                        # Check if skill exists
                        skill = Skill.query.filter_by(name=skill_name).first()
                        if not skill:
                            # Create new skill
                            skill = Skill(name=skill_name)
                            db.session.add(skill)
                            db.session.flush()  # Get the ID without committing
                        
                        # Add skill to job
                        job_skill = JobSkill(job_id=job.id, skill_id=skill.id)
                        db.session.add(job_skill)
        
        # Commit all changes
        db.session.commit()
        
        flash('Profile completed successfully!', 'success')
        return redirect(url_for('jobs'))
    
    # GET request - show the form
    categories = Category.query.filter_by(is_active=True).all()
    return render_template('complete_profile.html', categories=categories)

@app.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    # Only employers can post jobs
    if not current_user.is_employer:
        flash('Only employers can post jobs', 'error')
        return redirect(url_for('jobs'))
    
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        job_type = request.form.get('job_type')
        experience_level = request.form.get('experience_level')
        category_id = request.form.get('category_id')
        salary_min = request.form.get('salary_min') or None
        salary_max = request.form.get('salary_max') or None
        skills = request.form.get('skills')
        
        # Validate required fields
        if not title or not description or not job_type or not category_id:
            flash('Please fill in all required fields', 'error')
            categories = Category.query.filter_by(is_active=True).all()
            return render_template('post_job.html', categories=categories)
        
        # Create new job
        job = Job(
            title=title,
            description=description,
            location=location,
            job_type=JobType[job_type],
            experience_level=ExperienceLevel[experience_level],
            category_id=category_id,
            salary_min=salary_min,
            salary_max=salary_max,
            company_id=current_user.company_id,
            user_id=current_user.id
        )
        db.session.add(job)
        db.session.flush()  # Get the ID without committing
        
        # Add skills to job
        if skills:
            skill_list = [s.strip() for s in skills.split(',')]
            for skill_name in skill_list:
                # Check if skill exists
                skill = Skill.query.filter_by(name=skill_name).first()
                if not skill:
                    # Create new skill
                    skill = Skill(name=skill_name)
                    db.session.add(skill)
                    db.session.flush()  # Get the ID without committing
                
                # Add skill to job
                job_skill = JobSkill(job_id=job.id, skill_id=skill.id)
                db.session.add(job_skill)
        
        # Commit all changes
        db.session.commit()
        
        flash('Job posted successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    # GET request - show the form
    categories = Category.query.filter_by(is_active=True).all()
    return render_template('post_job.html', categories=categories)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_employer:
        # Get jobs posted by this employer
        jobs = Job.query.filter_by(user_id=current_user.id).filter(Job.is_deleted==False).join(Category).filter(Category.is_active == True).order_by(Job.created_at.desc()).all()
        return render_template('employer_dashboard.html', jobs=jobs, current_year=datetime.now().year)
    else:
        # Get job applications for this job seeker
        applications = JobApplication.query.filter_by(user_id=current_user.id).order_by(JobApplication.applied_at.desc()).all()
        return render_template('jobseeker_dashboard.html', applications=applications, current_year=datetime.now().year)

@app.route('/logout')
@login_required
def logout():
    # Clear all flash messages before logging out
    session.pop('_flashes', None)
    logout_user()
    flash('You have been logged out successfully', 'logout')
    return redirect(url_for('login'))

@app.route('/success')
@login_required
def success():
    return render_template('success.html', user=current_user)

@app.route('/users')
@login_required
def view_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/edit_user', methods=['POST'])
@login_required
def edit_user():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Not authenticated'}), 401

    # Get form data
    user_id = request.form.get('user_id')
    username = request.form.get('username')
    phone_number = request.form.get('phone_number')
    
    # Validate input
    if not user_id or not username or not phone_number:
        return jsonify({'error': 'Missing required fields'}), 400
        
    # Validate phone number format
    if not phone_number.isdigit() or len(phone_number) != 10:
        return jsonify({'error': 'Please enter a valid 10-digit phone number'}), 400
    
    # Get the user
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if phone number is already in use by another user
    existing_user = User.query.filter(User.phone_number == phone_number, User.id != user.id).first()
    if existing_user:
        return jsonify({'error': 'Phone number is already in use by another user'}), 400
    
    # Update user information
    user.username = username
    user.phone_number = phone_number
    db.session.commit()
    
    return jsonify({'message': 'User updated successfully'}), 200

@app.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    user_id = request.form.get('user_id')
    
    if not user_id:
        flash('User ID is required', 'error')
        return redirect(url_for('view_users'))
    
    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('view_users'))
    
    try:
        # Check if user has owned companies
        if user.owned_companies:
            # Delete the companies first
            for company in user.owned_companies:
                db.session.delete(company)
        
        # Delete job applications associated with the user
        JobApplication.query.filter_by(user_id=user.id).delete()
        
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        
        flash('User deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
    
    return redirect(url_for('view_users'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Get form data
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        bio = request.form.get('bio')
        skills = request.form.get('skills')
        
        # Update user information
        current_user.full_name = full_name
        current_user.email = email
        current_user.bio = bio
        
        # Handle resume upload if provided
        if 'resume' in request.files and request.files['resume'].filename:
            resume_file = request.files['resume']
            if resume_file and allowed_file(resume_file.filename, {'pdf'}):
                filename = secure_filename(f"{current_user.id}_{resume_file.filename}")
                resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Ensure upload directory exists
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                
                resume_file.save(resume_path)
                current_user.resume_path = filename
                flash('Resume updated successfully!', 'success')
            else:
                flash('Invalid resume file. Please upload a PDF file.', 'error')
        
        # Update skills
        if skills:
            # Clear existing skills
            current_user.skills = []
            
            # Add new skills
            skill_list = [s.strip() for s in skills.split(',')]
            for skill_name in skill_list:
                # Check if skill exists
                skill = Skill.query.filter_by(name=skill_name).first()
                if not skill:
                    # Create new skill
                    skill = Skill(name=skill_name)
                    db.session.add(skill)
                
                # Add skill to user
                if skill not in current_user.skills:
                    current_user.skills.append(skill)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    # Get current skills as comma-separated string
    current_skills = ', '.join([skill.name for skill in current_user.skills]) if current_user.skills else ''
    
    return render_template('profile.html',
                         user=current_user,
                         current_skills=current_skills,
                         ApplicationStatus=ApplicationStatus,
                         current_year=datetime.now().year)

@app.route('/applications')
@login_required
def applications():
    user_applications = JobApplication.query.filter_by(user_id=current_user.id).all()
    return render_template('applications.html', applications=user_applications)

@app.route('/withdraw_application/<int:application_id>', methods=['POST'])
@login_required
def withdraw_application(application_id):
    application = JobApplication.query.get_or_404(application_id)
    # Only the user who owns the application can withdraw
    if application.user_id != current_user.id:
        flash('You are not authorized to withdraw this application.', 'danger')
        return redirect(url_for('dashboard'))
    application.is_withdraw = True
    db.session.commit()
    flash('Your application has been withdrawn.', 'info')
    return redirect(url_for('dashboard'))

# --- Admin Job Management Routes ---
@app.route('/admin/jobs')
@login_required
@role_required('admin')
def admin_jobs():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('admin_jobs.html', jobs=jobs)

@app.route('/admin/jobs/create', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def admin_create_job():
    # TODO: Implement job creation logic
    return 'Job creation form here'

@app.route('/admin/jobs/<job_hashid>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def admin_edit_job(job_hashid):
    # Decode hashid to integer ID
    decoded = hashids.decode(job_hashid)
    if not decoded:
        abort(404)
    job_id = decoded[0]
    job = Job.query.get_or_404(job_id)
    if request.method == 'POST':
        job.title = request.form['title']
        job.description = request.form['description']
        job.location = request.form['location']
        job.salary_min = request.form.get('salary_min', type=int)
        job.salary_max = request.form.get('salary_max', type=int)
        job.job_type = JobType[request.form['job_type']]
        job.experience_level = ExperienceLevel[request.form['experience_level']]
        job.category_id = request.form.get('category_id', type=int)
        job.company_id = request.form.get('company_id', type=int)
        job.is_active = 'is_active' in request.form
        db.session.commit()
        flash('Job updated successfully', 'success')
        return redirect(url_for('admin_jobs'))
    companies = Company.query.all()
    categories = Category.query.filter_by(is_active=True).all()
    job_types = list(JobType)
    experience_levels = list(ExperienceLevel)
    return render_template('admin_job_form.html',
                           job=job,
                           companies=companies,
                           categories=categories,
                           job_types=job_types,
                           experience_levels=experience_levels)

@app.route('/admin/jobs/<job_hashid>/delete', methods=['POST'])
@login_required
@role_required('admin')
def admin_delete_job(job_hashid):
    decoded = hashids.decode(job_hashid)
    if not decoded:
        abort(404)
    job_id = decoded[0]
    job = Job.query.get_or_404(job_id)
    job.is_deleted = True
    db.session.commit()
    flash('Job soft-deleted successfully', 'success')
    return redirect(url_for('admin_jobs'))

@app.route('/admin/jobs/<job_hashid>/activate', methods=['POST'])
@login_required
@role_required('admin')
def admin_activate_job(job_hashid):
    decoded = hashids.decode(job_hashid)
    if not decoded:
        abort(404)
    job_id = decoded[0]
    job = Job.query.get_or_404(job_id)
    job.is_deleted = False
    db.session.commit()
    flash('Job activated successfully', 'success')
    return redirect(url_for('admin_jobs'))

# --- Admin User Management Routes ---
@app.route('/admin/users')
@login_required
@role_required('admin')
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/users/create', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def admin_create_user():
    # TODO: Implement user creation logic
    return 'User creation form here'

@app.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def admin_edit_user(user_id):
    # TODO: Implement user edit logic
    return f'Edit user {user_id}'

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def admin_delete_user(user_id):
    # TODO: Implement user delete logic
    return f'Delete user {user_id}'

@app.route('/admin/categories')
@login_required
@role_required('admin')
def admin_categories():
    categories = Category.query.order_by(Category.id).all()
    return render_template('admin_categories.html', categories=categories)

@app.route('/admin/categories/create', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def admin_create_category():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description')
        icon_class = request.form.get('icon_class')
        is_active = bool(request.form.get('is_active', True))
        category = Category(name=name, description=description, icon_class=icon_class, is_active=is_active)
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully.', 'success')
        return redirect(url_for('admin_categories'))
    return render_template('admin_category_form.html')

@app.route('/admin/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def admin_edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == 'POST':
        category.name = request.form['name']
        category.description = request.form.get('description')
        category.icon_class = request.form.get('icon_class')
        category.is_active = bool(request.form.get('is_active', True))
        db.session.commit()
        flash('Category updated successfully.', 'success')
        return redirect(url_for('admin_categories'))
    return render_template('admin_category_form.html', category=category)

@app.route('/admin/categories/<int:category_id>/deactivate')
@login_required
@role_required('admin')
def admin_deactivate_category(category_id):
    category = Category.query.get_or_404(category_id)
    category.is_active = False
    db.session.commit()
    flash('Category deactivated.', 'info')
    return redirect(url_for('admin_categories'))

@app.route('/admin/categories/<int:category_id>/activate')
@login_required
@role_required('admin')
def admin_activate_category(category_id):
    category = Category.query.get_or_404(category_id)
    category.is_active = True
    db.session.commit()
    flash('Category activated.', 'success')
    return redirect(url_for('admin_categories'))

# --- Admin Dashboard Route Example ---
@app.route('/admin/dashboard')
@login_required
@role_required('admin')
def admin_dashboard():
    # Example: show admin dashboard template
    return render_template('admin_dashboard.html')

def send_otp(user):
    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    
    # Development mode - just store the OTP without sending SMS
    print(f"[DEV MODE] OTP for {user.phone_number}: {otp}")
    
    # Store OTP and its creation time
    user.otp = otp
    user.otp_created_at = datetime.utcnow()
    db.session.commit()
    
    return True

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Configure upload folder for resumes
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)