# 🚀 Railway Deployment Guide for JobConnect

## Step 1: Create Railway Account and Project

1. **Go to Railway**: Visit [railway.app](https://railway.app)
2. **Sign Up/Login**: Use your GitHub account to sign in
3. **Create New Project**: Click "New Project"
4. **Deploy from GitHub**: Select "Deploy from GitHub repo"
5. **Select Repository**: Choose your `jobconnect-app` repository
6. **Select Branch**: Choose `development` or `main` branch

## Step 2: Configure Environment Variables

After your project is created, you need to set up environment variables:

1. **Go to Variables Tab**: In your Railway project dashboard
2. **Add the following variables**:

```env
FLASK_SECRET_KEY=your-super-secret-key-here-change-this
```

**Note**: Railway automatically provides `DATABASE_URL` for PostgreSQL, so you don't need to set it manually.

## Step 3: Add PostgreSQL Database

1. **In Railway Dashboard**: Click "New" → "Database" → "Add PostgreSQL"
2. **Database will be created**: Railway automatically connects it to your app
3. **DATABASE_URL**: Will be automatically available to your application

## Step 4: Deploy the Application

1. **Automatic Deployment**: Railway will automatically start deploying
2. **Monitor Logs**: Watch the deployment logs in the Railway dashboard
3. **Build Process**: Railway will:
   - Install Python dependencies
   - Run database initialization
   - Start your Flask application

## Step 5: Initialize Database (First Time Only)

After successful deployment:

1. **Open Railway Console**: In your project dashboard
2. **Run Database Initialization**:
```bash
python init_db.py
```

This will:
- Create all database tables
- Add sample job categories
- Create an admin user (admin@jobconnect.com / admin123)

## Step 6: Access Your Application

1. **Get Domain**: Railway provides a public URL (e.g., `your-app.railway.app`)
2. **Test the Application**: Visit the URL to see your JobConnect app
3. **Admin Login**: Use `admin@jobconnect.com` / `admin123` to access admin features

## Step 7: Custom Domain (Optional)

1. **In Railway Dashboard**: Go to Settings → Domains
2. **Add Custom Domain**: Enter your domain name
3. **Configure DNS**: Point your domain to Railway's servers

## 🔧 Troubleshooting

### If Deployment Fails:

1. **Check Logs**: Look at build and deploy logs in Railway dashboard
2. **Common Issues**:
   - Missing environment variables
   - Database connection issues
   - Python version conflicts

### If Database Issues:

1. **Recreate Database**: Delete and recreate PostgreSQL service
2. **Run Init Script**: Execute `python init_db.py` in Railway console
3. **Check Migrations**: Ensure all migrations are applied

### If App Won't Start:

1. **Check Procfile**: Ensure it's correctly configured
2. **Verify Port**: App should bind to `$PORT` environment variable
3. **Check Dependencies**: All packages in requirements.txt should install

## 📋 Post-Deployment Checklist

- [ ] Application loads successfully
- [ ] Database tables are created
- [ ] Admin user can login
- [ ] Job categories are visible
- [ ] Users can register and login
- [ ] Job posting works for employers
- [ ] Job applications work for job seekers

## 🔐 Security Notes

1. **Change Admin Password**: Login and change the default admin password
2. **Update Secret Key**: Use a strong, unique FLASK_SECRET_KEY
3. **Environment Variables**: Never commit sensitive data to GitHub

## 🎉 Success!

Your JobConnect application should now be live on Railway! 

**Next Steps**:
- Test all functionality
- Add real job categories and companies
- Configure email notifications (optional)
- Set up monitoring and analytics