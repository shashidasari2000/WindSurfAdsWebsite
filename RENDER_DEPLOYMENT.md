# 🚀 Deploy JobConnect to Render.com (FREE)

## Why Render.com?
- ✅ **Free Tier Available** (750 hours/month)
- ✅ **PostgreSQL Database** included
- ✅ **GitHub Integration**
- ✅ **Automatic HTTPS**
- ✅ **Easy to use**

## Step-by-Step Deployment:

### 1. **Create Render Account**
- Go to [render.com](https://render.com)
- Sign up with your GitHub account

### 2. **Create Web Service**
- Click "New +" → "Web Service"
- Connect your GitHub repository: `jobconnect-app`
- Select branch: `development` or `main`

### 3. **Configure Web Service**
```
Name: jobconnect-app
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

### 4. **Add Environment Variables**
In the Environment section, add:
```
FLASK_SECRET_KEY = (click "Generate" for auto-generated key)
```

### 5. **Create PostgreSQL Database**
- Click "New +" → "PostgreSQL"
- Name: `jobconnect-db`
- Plan: **Free**
- Create database

### 6. **Connect Database to App**
- Go back to your web service
- In Environment Variables, add:
```
DATABASE_URL = (copy from your PostgreSQL service)
```

### 7. **Deploy & Initialize**
- Click "Deploy"
- After deployment, go to your app's shell and run:
```bash
python init_db.py
```

### 8. **Access Your App**
- Render provides a URL like: `https://jobconnect-app.onrender.com`
- Visit it to see your live application!

## 🎉 Admin Access:
- **Email**: admin@jobconnect.com
- **Password**: admin123

## 💡 Free Tier Limitations:
- **Sleep after 15 minutes** of inactivity
- **750 hours/month** (about 31 days if always on)
- **500MB storage** for database

Perfect for development and portfolio projects!