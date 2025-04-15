from app import app, db
from models import User, Company, Job, Category, JobType, ExperienceLevel, Skill, JobSkill
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def seed_data():
    with app.app_context():
        # Create sample employers
        employers = [
            {
                'username': 'google_hr',
                'phone_number': '1234567890',
                'email': 'hr@google.com',
                'password_hash': generate_password_hash('password123'),
                'is_verified': True,
                'is_employer': True,
                'full_name': 'Google HR'
            },
            {
                'username': 'microsoft_hr',
                'phone_number': '2345678901',
                'email': 'hr@microsoft.com',
                'password_hash': generate_password_hash('password123'),
                'is_verified': True,
                'is_employer': True,
                'full_name': 'Microsoft HR'
            }
        ]
        
        employer_objects = []
        for employer_data in employers:
            employer = User(**employer_data)
            db.session.add(employer)
            db.session.flush()  # Get the ID
            employer_objects.append(employer)
        
        # Create sample companies
        companies = [
            {
                'name': 'Google',
                'description': 'A leading technology company specializing in search, cloud computing, and AI.',
                'website': 'https://google.com',
                'location': 'Mountain View, CA',
                'owner_id': employer_objects[0].id
            },
            {
                'name': 'Microsoft',
                'description': 'A multinational technology company focused on software, cloud, and gaming.',
                'website': 'https://microsoft.com',
                'location': 'Redmond, WA',
                'owner_id': employer_objects[1].id
            }
        ]
        
        company_objects = []
        for company_data in companies:
            company = Company(**company_data)
            db.session.add(company)
            db.session.flush()  # Get the ID
            company_objects.append(company)
        
        # Get categories
        software_dev = Category.query.filter_by(name='Software Development').first()
        
        # Create sample jobs
        jobs = [
            {
                'title': 'Senior Software Engineer',
                'description': '''
                We are looking for a Senior Software Engineer to join our team.
                
                Requirements:
                - 5+ years of experience in software development
                - Strong expertise in Python, Java, or C++
                - Experience with distributed systems
                - Excellent problem-solving skills
                
                Benefits:
                - Competitive salary
                - Health insurance
                - Stock options
                - Flexible work hours
                ''',
                'location': 'Mountain View, CA',
                'salary_min': 150000,
                'salary_max': 250000,
                'job_type': JobType.FULL_TIME,
                'experience_level': ExperienceLevel.SENIOR,
                'company_id': company_objects[0].id,
                'category_id': software_dev.id,
                'user_id': employer_objects[0].id,
                'is_active': True
            },
            {
                'title': 'Full Stack Developer',
                'description': '''
                Join our dynamic team as a Full Stack Developer.
                
                Requirements:
                - 3+ years of experience in web development
                - Proficiency in React and Node.js
                - Experience with cloud platforms (AWS/Azure)
                - Strong communication skills
                
                Benefits:
                - Remote work options
                - Health and dental coverage
                - 401(k) matching
                - Professional development budget
                ''',
                'location': 'Redmond, WA (Remote)',
                'salary_min': 120000,
                'salary_max': 180000,
                'job_type': JobType.FULL_TIME,
                'experience_level': ExperienceLevel.MID,
                'company_id': company_objects[1].id,
                'category_id': software_dev.id,
                'user_id': employer_objects[1].id,
                'is_active': True
            },
            {
                'title': 'Machine Learning Engineer',
                'description': '''
                Looking for an experienced Machine Learning Engineer to work on cutting-edge AI projects.
                
                Requirements:
                - MS/PhD in Computer Science or related field
                - Strong background in machine learning and deep learning
                - Experience with TensorFlow or PyTorch
                - Publication record is a plus
                
                Benefits:
                - Industry-leading compensation
                - Research opportunities
                - Conference attendance
                - Relocation assistance
                ''',
                'location': 'Mountain View, CA',
                'salary_min': 180000,
                'salary_max': 300000,
                'job_type': JobType.FULL_TIME,
                'experience_level': ExperienceLevel.SENIOR,
                'company_id': company_objects[0].id,
                'category_id': software_dev.id,
                'user_id': employer_objects[0].id,
                'is_active': True
            }
        ]
        
        # Add jobs
        for job_data in jobs:
            job = Job(**job_data)
            db.session.add(job)
        
        # Create common skills
        skills = [
            'Python', 'Java', 'JavaScript', 'React', 'Node.js', 'AWS', 'Azure',
            'Machine Learning', 'TensorFlow', 'PyTorch', 'SQL', 'NoSQL',
            'Docker', 'Kubernetes', 'CI/CD'
        ]
        
        skill_objects = {}
        for skill_name in skills:
            # Check if skill already exists
            skill = Skill.query.filter_by(name=skill_name).first()
            if not skill:
                skill = Skill(name=skill_name)
                db.session.add(skill)
                db.session.flush()  # Get the ID
            skill_objects[skill_name] = skill
        
        # Commit all changes
        db.session.commit()
        print("Sample data seeded successfully!")

if __name__ == '__main__':
    seed_data()
