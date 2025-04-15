from app import app, db
from models import User, Company, Category, Job, JobType, ExperienceLevel
from datetime import datetime, timedelta

def create_sample_data():
    with app.app_context():
        # Create sample categories
        categories = {
            'Software Development': 'Software engineering and development roles',
            'Marketing': 'Digital marketing and brand management',
            'Design': 'UI/UX and graphic design',
            'Data Science': 'Data analysis and machine learning',
            'Product Management': 'Product strategy and development',
            'Sales': 'Sales and business development'
        }
        
        db_categories = {}
        for name, description in categories.items():
            category = Category.query.filter_by(name=name).first()
            if not category:
                category = Category(name=name, description=description)
                db.session.add(category)
            db_categories[name] = category
        
        # Create sample companies
        companies = {
            'TechCorp Solutions': 'Leading software development company',
            'BrandGrowth Inc': 'Digital marketing agency',
            'DesignHub': 'Creative design studio',
            'DataMinds Analytics': 'Data science consulting firm',
            'InnovatePro': 'Product development company',
            'CloudTech Systems': 'Cloud infrastructure provider'
        }
        
        db_companies = {}
        for name, description in companies.items():
            company = Company.query.filter_by(name=name).first()
            if not company:
                company = Company(name=name, description=description, website=f"https://www.{name.lower().replace(' ', '')}.com")
                db.session.add(company)
            db_companies[name] = company
        
        # Create sample jobs
        jobs = [
            {
                'title': 'Senior Software Engineer',
                'company': 'TechCorp Solutions',
                'category': 'Software Development',
                'description': 'Looking for an experienced software engineer to lead development projects.',
                'location': 'San Francisco, CA',
                'job_type': JobType.FULL_TIME,
                'experience_level': ExperienceLevel.SENIOR,
                'salary_min': 120000,
                'salary_max': 180000,
                'is_active': True
            },
            {
                'title': 'Marketing Manager',
                'company': 'BrandGrowth Inc',
                'category': 'Marketing',
                'description': 'Lead digital marketing campaigns and brand strategy.',
                'location': 'New York, NY',
                'job_type': JobType.FULL_TIME,
                'experience_level': ExperienceLevel.MID,
                'salary_min': 80000,
                'salary_max': 120000,
                'is_active': True
            },
            {
                'title': 'UX/UI Designer',
                'company': 'DesignHub',
                'category': 'Design',
                'description': 'Create beautiful and intuitive user interfaces.',
                'location': 'Remote',
                'job_type': JobType.CONTRACT,
                'experience_level': ExperienceLevel.MID,
                'salary_min': 70000,
                'salary_max': 100000,
                'is_active': True
            },
            {
                'title': 'Junior Data Scientist',
                'company': 'DataMinds Analytics',
                'category': 'Data Science',
                'description': 'Help analyze data and build machine learning models.',
                'location': 'Boston, MA',
                'job_type': JobType.FULL_TIME,
                'experience_level': ExperienceLevel.ENTRY,
                'salary_min': 70000,
                'salary_max': 90000,
                'is_active': True
            },
            {
                'title': 'Product Manager',
                'company': 'InnovatePro',
                'category': 'Product Management',
                'description': 'Drive product strategy and development.',
                'location': 'Austin, TX',
                'job_type': JobType.FULL_TIME,
                'experience_level': ExperienceLevel.SENIOR,
                'salary_min': 110000,
                'salary_max': 160000,
                'is_active': True
            },
            {
                'title': 'DevOps Engineer',
                'company': 'CloudTech Systems',
                'category': 'Software Development',
                'description': 'Manage cloud infrastructure and CI/CD pipelines.',
                'location': 'Seattle, WA',
                'job_type': JobType.FULL_TIME,
                'experience_level': ExperienceLevel.MID,
                'salary_min': 100000,
                'salary_max': 150000,
                'is_active': True
            }
        ]
        
        # Add jobs to database
        for job_data in jobs:
            # Check if job already exists
            existing_job = Job.query.filter_by(
                title=job_data['title'],
                company=db_companies[job_data['company']]
            ).first()
            
            if not existing_job:
                job = Job(
                    title=job_data['title'],
                    company=db_companies[job_data['company']],
                    category=db_categories[job_data['category']],
                    description=job_data['description'],
                    location=job_data['location'],
                    job_type=job_data['job_type'],
                    experience_level=job_data['experience_level'],
                    salary_min=job_data['salary_min'],
                    salary_max=job_data['salary_max'],
                    is_active=job_data['is_active'],
                    created_at=datetime.now() - timedelta(days=len(jobs) % 7),
                    user_id=1  # Assuming admin user has ID 1
                )
                db.session.add(job)
        
        # Commit all changes
        db.session.commit()
        print("Sample data has been added successfully!")

if __name__ == '__main__':
    create_sample_data()
