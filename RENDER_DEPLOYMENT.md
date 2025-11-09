# 🚀 Deploy ALX Travel App to Render

**Complete Step-by-Step Deployment Guide for Milestone 6**

This guide will walk you through deploying your Django application with Celery background tasks and publicly accessible Swagger documentation to Render.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Prepare Your Application](#prepare-your-application)
3. [Deploy to Render](#deploy-to-render)
4. [Configure Celery Worker](#configure-celery-worker)
5. [Test Your Deployment](#test-your-deployment)
6. [Access Swagger Documentation](#access-swagger-documentation)
7. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

Before you begin, ensure you have:

- ✓ GitHub account
- ✓ Render account (sign up at https://render.com - free tier available)
- ✓ Your Django app pushed to a GitHub repository
- ✓ CloudAMQP account for RabbitMQ (free tier: https://www.cloudamqp.com/)

---

## 🔧 Prepare Your Application

### Step 1: Install Required Dependencies

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should include:
- Django
- djangorestframework
- drf-yasg (Swagger)
- celery
- gunicorn
- whitenoise
- psycopg2-binary
- dj-database-url

### Step 2: Create Build Script

Create a file named `build.sh` in your project root:

```bash
#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
```

Make it executable:
```bash
chmod +x build.sh
```

### Step 3: Verify Settings Configuration

Your `settings.py` should already be configured (already done):
- ✓ SECRET_KEY from environment
- ✓ DEBUG from environment
- ✓ ALLOWED_HOSTS from environment
- ✓ DATABASE_URL support (PostgreSQL)
- ✓ WhiteNoise middleware
- ✓ drf-yasg installed
- ✓ Swagger configured with public access
- ✓ Celery broker from environment

### Step 4: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Prepare for Render deployment"

# Create GitHub repository and push
git remote add origin https://github.com/YOUR_USERNAME/alx_travel_app_0x03.git
git branch -M main
git push -u origin main
```

---

## 🌐 Deploy to Render

### Step 1: Set Up RabbitMQ on CloudAMQP

1. Go to https://www.cloudamqp.com/
2. Sign up for a free account
3. Create a new instance:
   - **Name**: `alx-travel-rabbitmq`
   - **Plan**: Little Lemur (Free)
   - **Region**: Choose closest to your users
4. Click on your instance
5. **Copy the AMQP URL** (looks like: `amqps://username:password@server.cloudamqp.com/vhost`)
6. Keep this URL handy - you'll need it for environment variables

### Step 2: Create PostgreSQL Database on Render

1. Log in to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `alx-travel-db`
   - **Database**: `alx_travel_db`
   - **User**: `alx_user`
   - **Region**: Choose closest to your users
   - **Plan**: Free
4. Click **"Create Database"**
5. Wait for database to provision
6. **Copy the Internal Database URL** from the database dashboard

### Step 3: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository:
   - Click **"Connect a repository"**
   - Select your `alx_travel_app_0x03` repository
3. Configure the service:
   - **Name**: `alx-travel-app`
   - **Region**: Same as your database
   - **Branch**: `main`
   - **Root Directory**: Leave empty (unless app is in subdirectory)
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn alx_travel_app.wsgi:application --bind 0.0.0.0:$PORT`
   - **Plan**: Free

### Step 4: Configure Environment Variables

In your web service settings, click **"Environment"** and add these variables:

| Key | Value | Notes |
|-----|-------|-------|
| `SECRET_KEY` | (Generate a secure key) | Use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` | IMPORTANT: Never use True in production |
| `ALLOWED_HOSTS` | `alx-travel-app.onrender.com,localhost` | Replace with your actual Render URL |
| `DATABASE_URL` | (Paste Internal Database URL) | From Step 2 |
| `CELERY_BROKER_URL` | (Paste CloudAMQP AMQP URL) | From Step 1 |
| `CELERY_RESULT_BACKEND` | `rpc://` | Default RPC backend |
| `CHAPA_SECRET_KEY` | (Your Chapa API key) | If using Chapa payments |
| `EMAIL_HOST_USER` | (Your email) | For sending notifications |
| `EMAIL_HOST_PASSWORD` | (Your email password) | App password recommended |

### Step 5: Deploy Web Service

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Run `build.sh`
   - Start your application with Gunicorn
3. Wait for deployment (3-5 minutes)
4. Check the logs for any errors

---

## ⚙️ Configure Celery Worker

### Step 1: Create Background Worker Service

1. In Render dashboard, click **"New +"** → **"Background Worker"**
2. Connect the same GitHub repository
3. Configure:
   - **Name**: `alx-travel-celery-worker`
   - **Region**: Same as web service
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `celery -A alx_travel_app worker --loglevel=info`
   - **Plan**: Free

### Step 2: Add Environment Variables to Worker

Add the **SAME environment variables** as the web service (especially):
- `DATABASE_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `SECRET_KEY`
- `DEBUG=False`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`

### Step 3: Deploy Worker

1. Click **"Create Background Worker"**
2. Render will start the Celery worker
3. Monitor logs to ensure it connects to RabbitMQ successfully

You should see logs like:
```
[2024-11-08 10:00:00,000: INFO/MainProcess] Connected to amqps://...
[2024-11-08 10:00:00,000: INFO/MainProcess] celery@hostname ready.
```

---

## 🧪 Test Your Deployment

### 1. Access Your Application

Visit: `https://alx-travel-app.onrender.com` (replace with your actual URL)

You should see your application running!

### 2. Test Admin Panel

1. Create a superuser (one-time setup):
   - In Render dashboard, go to your **web service**
   - Click **"Shell"** tab
   - Run:
     ```bash
     python manage.py createsuperuser
     ```
   - Follow prompts to create admin user

2. Access admin: `https://alx-travel-app.onrender.com/admin/`

### 3. Test API Endpoints

Test your listings endpoints:

```bash
# Get all listings
curl https://alx-travel-app.onrender.com/api/listings/

# Create a booking (adjust payload as needed)
curl -X POST https://alx-travel-app.onrender.com/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "listing_id": 1,
    "user_name": "Test User",
    "email": "test@example.com",
    "start_date": "2024-12-01",
    "end_date": "2024-12-07"
  }'
```

### 4. Test Celery Background Tasks

1. Create a booking through the API (above)
2. Check Celery worker logs in Render:
   - Go to **alx-travel-celery-worker** service
   - Click **"Logs"**
   - You should see task execution logs:
     ```
     [INFO] Task alx_travel_app.listings.tasks.send_booking_confirmation_email succeeded
     ```

3. Check email inbox for confirmation email

---

## 📚 Access Swagger Documentation

### Public Swagger UI

Your Swagger documentation is **publicly accessible** at:

**URL**: `https://alx-travel-app.onrender.com/swagger/`

### What You'll See

- Complete API documentation
- All endpoints with descriptions
- Interactive "Try it out" buttons
- Request/response schemas
- No login required (public access enabled)

### Alternative Documentation

- **ReDoc**: `https://alx-travel-app.onrender.com/redoc/`
- **JSON Schema**: `https://alx-travel-app.onrender.com/swagger.json`
- **YAML Schema**: `https://alx-travel-app.onrender.com/swagger.yaml`

### Verify Swagger Configuration

Confirm these settings in your deployment:

✓ `drf_yasg` in `INSTALLED_APPS`
✓ `permissions.AllowAny` in schema_view
✓ `USE_SESSION_AUTH = False` in `SWAGGER_SETTINGS`
✓ URLs configured in `urls.py`

---

## 🔍 Troubleshooting

### Issue: Application Won't Start

**Symptoms**: Build succeeds but app crashes on start

**Solutions**:
1. Check web service logs in Render
2. Verify `DATABASE_URL` is set correctly
3. Ensure `build.sh` ran migrations successfully
4. Check `ALLOWED_HOSTS` includes your Render URL

```bash
# In Render shell, check:
python manage.py check --deploy
```

### Issue: Static Files Not Loading

**Symptoms**: CSS/JS not working, admin panel looks broken

**Solutions**:
1. Verify `build.sh` runs `collectstatic`:
   ```bash
   python manage.py collectstatic --no-input
   ```

2. Check `settings.py` has WhiteNoise:
   ```python
   MIDDLEWARE = [
       'whitenoise.middleware.WhiteNoiseMiddleware',  # After SecurityMiddleware
       ...
   ]
   ```

3. Run in Render shell:
   ```bash
   python manage.py collectstatic --no-input
   ```

### Issue: Celery Worker Not Connecting

**Symptoms**: Worker logs show connection errors

**Solutions**:
1. Verify `CELERY_BROKER_URL` is correct CloudAMQP URL
2. Check CloudAMQP dashboard for connection limits
3. Ensure worker has same environment variables as web service
4. Restart worker service in Render

### Issue: Database Connection Error

**Symptoms**: `OperationalError: could not connect to server`

**Solutions**:
1. Verify `DATABASE_URL` in environment variables
2. Check database is in same region as web service
3. Ensure database is not sleeping (free tier sleeps after inactivity)
4. Use **Internal Database URL** (not External)

### Issue: Swagger Not Accessible

**Symptoms**: 404 error at `/swagger/`

**Solutions**:
1. Verify `drf_yasg` is installed:
   ```bash
   pip list | grep drf-yasg
   ```

2. Check `urls.py` has Swagger paths

3. Ensure `drf_yasg` in `INSTALLED_APPS`

4. Clear browser cache and try incognito mode

5. Check deployment logs for import errors

### Issue: Email Notifications Not Sending

**Symptoms**: Celery tasks succeed but no emails received

**Solutions**:
1. Check email configuration in settings:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
   EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
   ```

2. If using Gmail:
   - Enable 2FA
   - Generate App Password
   - Use App Password (not account password)

3. Check spam/junk folder

4. Test email manually in Render shell:
   ```python
   python manage.py shell
   from django.core.mail import send_mail
   send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
   ```

### Issue: 500 Internal Server Error

**Symptoms**: App returns 500 errors

**Solutions**:
1. Check error logs in Render
2. Enable better error reporting temporarily:
   - Set `DEBUG=True` temporarily (remember to turn off after debugging)
3. Check database migrations are applied:
   ```bash
   python manage.py showmigrations
   python manage.py migrate
   ```

### Getting Help

If issues persist:

1. **Check Render Logs**:
   - Web Service → Logs
   - Worker Service → Logs
   - Database → Logs

2. **Use Render Shell**:
   - Web Service → Shell
   - Run Django management commands
   - Test database connectivity

3. **CloudAMQP Dashboard**:
   - Check connection count
   - View message rates
   - Check queue status

4. **Render Community**: https://render.com/community

---

## 🎯 Deployment Checklist

Before submitting your project, verify:

- [ ] ✅ Application deployed and accessible at your Render URL
- [ ] ✅ Admin panel accessible at `/admin/`
- [ ] ✅ PostgreSQL database connected
- [ ] ✅ All API endpoints working
- [ ] ✅ Celery worker running (check logs)
- [ ] ✅ RabbitMQ connected (CloudAMQP)
- [ ] ✅ Background tasks executing (test booking emails)
- [ ] ✅ **Swagger UI publicly accessible at `/swagger/`**
- [ ] ✅ Static files loading correctly
- [ ] ✅ DEBUG set to False
- [ ] ✅ No sensitive data in repository
- [ ] ✅ Environment variables properly configured

---

## 📝 Submit Your Work

For your ALX project submission, provide:

1. **GitHub Repository URL**: Your repo with all code
2. **Deployed Application URL**: `https://alx-travel-app.onrender.com`
3. **Swagger Documentation URL**: `https://alx-travel-app.onrender.com/swagger/`
4. **Admin Panel URL**: `https://alx-travel-app.onrender.com/admin/`

### Example Submission:

```
Repository: https://github.com/yourusername/alx_travel_app_0x03
Application: https://alx-travel-app.onrender.com
Swagger API Docs: https://alx-travel-app.onrender.com/swagger/
Admin Panel: https://alx-travel-app.onrender.com/admin/

Test Credentials (for reviewers):
Username: reviewer
Password: [provided separately]
```

---

## 🎉 Success!

Your Django application with Celery background tasks and public Swagger documentation is now live on Render!

**Key Features Deployed**:
- ✅ Django REST API
- ✅ PostgreSQL Database
- ✅ Celery + RabbitMQ (async tasks)
- ✅ Email notifications
- ✅ Public Swagger API documentation
- ✅ Admin interface
- ✅ Static file serving
- ✅ Production security settings

**Next Steps**:
- Monitor application performance in Render
- Set up custom domain (optional)
- Configure automatic deploys from GitHub
- Add more endpoints and features

---

## 📞 Support Resources

- **Render Documentation**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/4.2/howto/deployment/
- **Celery Documentation**: https://docs.celeryproject.org/
- **drf-yasg**: https://drf-yasg.readthedocs.io/

---

**Good luck with your deployment! 🚀**
