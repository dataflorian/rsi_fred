# 🚀 Deployment Guide

Complete guide to deploy your RSI Crypto Screener to free hosting platforms.

## 🌟 Recommended: Render.com (Free Tier)

### Why Render?
- **750 free hours/month** (enough for 24/7 operation)
- **Automatic deployments** from GitHub
- **SSL/HTTPS included** at no cost
- **Easy environment variable management**
- **Python support** out of the box

### Step-by-Step Deployment

#### 1. Prepare Your Repository
```bash
# Ensure all files are committed
git add .
git commit -m "Production ready RSI Crypto Screener"
git push origin main
```

#### 2. Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Verify your email

#### 3. Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select the `RSI_Fred` repository

#### 4. Configure Service
- **Name**: `rsi-crypto-screener` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn run:app --bind 0.0.0.0:$PORT`

#### 5. Set Environment Variables
Click "Environment" tab and add:
```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
RSI_PERIOD=14
TOP_COINS_LIMIT=10
REFRESH_INTERVAL_MINUTES=15
```

#### 6. Deploy
1. Click "Create Web Service"
2. Wait for build to complete (5-10 minutes)
3. Your app will be available at `https://your-app-name.onrender.com`

## 🚂 Alternative: Railway.app

### Why Railway?
- **500 free hours/month**
- **GitHub integration**
- **Custom domains support**
- **Easy scaling**

### Deployment Steps

#### 1. Railway Setup
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"

#### 2. Configure Project
- **Repository**: Select your `RSI_Fred` repo
- **Branch**: `main`
- **Root Directory**: `/` (leave default)

#### 3. Set Environment Variables
In Railway dashboard:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key
PORT=8000
```

#### 4. Deploy
1. Railway will auto-detect Python
2. Build and deploy automatically
3. Get your live URL from dashboard

## 🔧 Production Configuration

### Environment Variables
```bash
# Required for production
FLASK_ENV=production
SECRET_KEY=your-very-long-random-string

# Optional customizations
RSI_PERIOD=14
TOP_COINS_LIMIT=15
REFRESH_INTERVAL_MINUTES=10
LOG_LEVEL=WARNING
```

### Generate Secret Key
```python
import secrets
print(secrets.token_urlsafe(32))
```

### Update run.py for Production
```python
from app import create_app
from config import get_config

app = create_app()
app.config.from_object(get_config())

if __name__ == '__main__':
    app.run()
```

## 📊 Monitoring & Maintenance

### Health Checks
- **Auto-refresh**: Verify 15-minute updates work
- **API connectivity**: Check Binance API status
- **Error logs**: Monitor for any issues

### Performance Monitoring
- **Response times**: Should be under 5 seconds
- **Memory usage**: Monitor for leaks
- **API rate limits**: Ensure we're within Binance limits

### Regular Maintenance
- **Weekly**: Check for dependency updates
- **Monthly**: Review error logs
- **Quarterly**: Performance optimization review

## 🚨 Troubleshooting

### Common Issues

#### Build Failures
```bash
# Check requirements.txt
pip install -r requirements.txt

# Verify Python version
python --version  # Should be 3.8+
```

#### Runtime Errors
```bash
# Check logs in hosting platform
# Verify environment variables
# Test locally first
```

#### Performance Issues
- **Slow loading**: Normal for first visit
- **Refresh delays**: Expected due to API calls
- **Memory issues**: Check for memory leaks

### Debug Mode (Temporary)
```bash
# Set for debugging (remove in production)
FLASK_ENV=development
DEBUG=true
```

## 🔒 Security Checklist

### Production Security
- [ ] `FLASK_ENV=production`
- [ ] Strong `SECRET_KEY` set
- [ ] HTTPS/SSL enabled
- [ ] Error messages don't expose internals
- [ ] No debug information in production

### API Security
- [ ] Rate limiting enabled
- [ ] Input validation working
- [ ] No sensitive data in logs
- [ ] CORS properly configured

## 📱 Mobile Testing

### Responsive Design
- [ ] Test on mobile devices
- [ ] Verify table scrolling
- [ ] Check button sizes
- [ ] Test touch interactions

### Browser Compatibility
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (mobile/desktop)
- [ ] Mobile browsers

## 🎯 Next Steps After Deployment

### Immediate Actions
1. **Test all functionality** on live site
2. **Verify auto-refresh** works correctly
3. **Check mobile responsiveness**
4. **Monitor error logs**

### Future Enhancements
1. **Custom domain** setup
2. **Analytics integration** (Google Analytics)
3. **Performance monitoring** tools
4. **User feedback** collection

### Marketing & Sharing
1. **Social media** announcements
2. **Crypto community** posts
3. **GitHub** repository promotion
4. **Documentation** sharing

## 🆘 Support & Help

### Getting Help
- **GitHub Issues**: Report bugs
- **Documentation**: Check README.md
- **Community**: Join crypto trading forums
- **Hosting Support**: Platform-specific help

### Useful Resources
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app/)

---

**🎉 Congratulations! Your RSI Crypto Screener is now live and helping traders worldwide!**

*Remember: This is a tool for educational purposes. Always do your own research before making investment decisions.*
