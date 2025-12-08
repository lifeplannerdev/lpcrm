# Cloud Deployment Configuration for LPCRM

## Files Structure
```
lpcrm/
├── manage.py
├── Dockerfile              # Build file for cloud deployment
├── .dockerignore
├── requirements.txt
├── lpcrm/
│   ├── settings.py
│   ├── wsgi.py
│   └── ...
├── accounts/
├── leads/
└── ... (other apps)
```

## Cloud Deployment Platforms

### 1. AWS (Elastic Container Service - ECS)

```bash
# Build image
docker build -t lpcrm:latest .

# Tag for ECR
docker tag lpcrm:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/lpcrm:latest

# Push to ECR
aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com
docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/lpcrm:latest
```

**Environment Variables to set in ECS Task Definition:**
```
DEBUG=False
SECRET_KEY=your-secure-key
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:password@rds-endpoint:5432/lpcrm_db
CLOUDINARY_URL=cloudinary://...
```

### 2. Google Cloud Run

```bash
# Build and push directly
gcloud run deploy lpcrm \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Set environment variables in Cloud Run:**
- Go to Cloud Run console → Select service → Edit & Deploy
- Add environment variables in the Containers section

### 3. Azure Container Instances

```bash
# Build and push to ACR
az acr build --registry <REGISTRY_NAME> --image lpcrm:latest .

# Deploy
az container create \
  --resource-group <RESOURCE_GROUP> \
  --name lpcrm-container \
  --image <REGISTRY_NAME>.azurecr.io/lpcrm:latest \
  --environment-variables \
    DEBUG=False \
    SECRET_KEY=your-key \
    DATABASE_URL=postgresql://...
```

### 4. Heroku

```bash
# Create app
heroku create your-app-name

# Add buildpack
heroku buildpacks:add heroku/docker

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-key
heroku config:set DATABASE_URL=postgresql://...

# Deploy
git push heroku main
```

### 5. DigitalOcean App Platform

```bash
# Create app.yaml in project root
```

Create `app.yaml`:
```yaml
name: lpcrm
services:
  - name: web
    github:
      branch: main
      repo: your-username/lpcrm
    build_command: pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
    run_command: gunicorn lpcrm.wsgi:application
    envs:
      - key: DEBUG
        value: "False"
      - key: SECRET_KEY
        value: ${SECRET_KEY}
      - key: DATABASE_URL
        value: ${db.connection_string}
    http_port: 8000

databases:
  - name: db
    engine: PG
    version: "15"
    production: true
```

Then deploy:
```bash
doctl apps create --spec app.yaml
```

### 6. Render

1. Push code to GitHub
2. Go to https://render.com
3. Create new Web Service
4. Select your repository
5. Set build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
6. Set start command: `gunicorn lpcrm.wsgi:application`
7. Add environment variables:
   - `DEBUG=False`
   - `SECRET_KEY=your-key`
   - `DATABASE_URL=postgresql://...`

## Important Configuration Steps

### 1. Update Django settings.py for production

```python
# In lpcrm/settings.py

# Security Settings
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Database
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
    )
}

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media Files (use cloud storage)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Cloudinary
import cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
)

# CORS
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')

# HTTPS/Security
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
```

### 2. Create a .env file for local testing

```env
DEBUG=False
SECRET_KEY=your-very-secure-random-key
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
DATABASE_URL=postgresql://user:password@db-host:5432/lpcrm_db
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
CORS_ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

### 3. Test Docker image locally

```bash
# Build
docker build -t lpcrm:latest .

# Run
docker run -p 8000:8000 \
  -e DEBUG=False \
  -e SECRET_KEY=your-key \
  -e DATABASE_URL=postgresql://user:pass@localhost:5432/lpcrm \
  lpcrm:latest
```

## Pre-deployment Checklist

- [ ] Update `settings.py` with environment variable configuration
- [ ] Set `DEBUG=False` in production
- [ ] Create strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up database (PostgreSQL recommended)
- [ ] Configure static files collection
- [ ] Set up media file storage (Cloudinary or S3)
- [ ] Test Docker build locally
- [ ] Set all required environment variables in cloud platform
- [ ] Test application after deployment
- [ ] Set up monitoring and logging
- [ ] Enable HTTPS/SSL
- [ ] Configure backup strategy

## Useful Commands

```bash
# Build locally
docker build -t lpcrm:latest .

# Run locally
docker run -p 8000:8000 lpcrm:latest

# View logs
docker logs <container-id>

# Check image size
docker images lpcrm

# Push to registry
docker push your-registry/lpcrm:latest
```

## Troubleshooting

1. **Static files not loading**: Ensure `STATIC_ROOT` is set and `collectstatic` is run
2. **Database connection errors**: Verify `DATABASE_URL` format
3. **Port issues**: Container exposes port 8000, map it to your cloud platform
4. **Memory issues**: Increase container memory or reduce worker count in Dockerfile CMD
5. **Permission errors**: User `appuser` (UID 1000) should have proper permissions

## Support Resources

- [Django Deployment](https://docs.djangoproject.com/en/5.2/howto/deployment/)
- [Docker Documentation](https://docs.docker.com/)
- [Gunicorn Configuration](https://docs.gunicorn.org/)
