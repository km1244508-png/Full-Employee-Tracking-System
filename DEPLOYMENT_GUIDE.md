# 🕒 Attendance & Work Progress Tracker - Offline Deployment Guide

## Overview
This Streamlit application is designed to work **completely offline** after initial setup. No internet connection or GitHub access is required for daily operation.

## Features
✅ **Completely Offline** - All data stored locally  
✅ **No External Dependencies** - Uses SQLite database  
✅ **No GitHub Required** - Self-contained application  
✅ **User Registration** - Self-service employee sign-ups  
✅ **Attendance Tracking** - Check-in/check-out system  
✅ **Reports & Analytics** - Excel & PDF exports  
✅ **Dark Modern UI** - Professional-grade interface  

---

## System Requirements
- **Python** 3.8 or higher
- **Windows/Mac/Linux**
- **4GB RAM** (recommended)
- **100MB disk space**

---

## Installation (Offline Setup)

### Step 1: Download or Copy Application
Place the entire `attendance_app` folder on your computer.

### Step 2: Install Python Packages (WITH Internet)
You need internet connection **only once** to install packages.

```bash
cd attendance_app
pip install -r requirements.txt
```

#### Alternative: Create Offline Package
If you need to transfer the app to a machine without internet:

```bash
# On machine WITH internet:
pip install -r requirements.txt --download ./offline_packages

# Transfer both 'offline_packages' and 'attendance_app' folders to offline machine

# On machine WITHOUT internet:
pip install --no-index --find-links ./offline_packages -r requirements.txt
```

### Step 3: Verify Installation
```bash
python -m streamlit --version
```

---

## Running the Application

### Start the App
```bash
cd attendance_app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### First Time Setup
1. **Default Admin Credentials:**
   - Username: `admin`
   - Password: `admin123`

2. ⚠️ **IMPORTANT**: Change the admin password immediately!
   - Go to **Employee Management → Change My Password**
   - Set a strong password

### Add Employees
1. Log in as Admin
2. Go to **Employee Management**
3. Click **Add New Employee**
4. Fill in details and create login credentials

---

## Using the Application

### For Admins
- **Mark Attendance** - Record check-in/check-out for any employee
- **Employee Management** - Create/edit employee profiles & permissions
- **Dashboard** - Real-time overview of all attendance
- **Reports** - Generate daily/weekly/monthly reports
- **Work Progress** - Assign and track tasks

### For Employees
- **Dashboard** - View your attendance status
- **Reports** - Export your own attendance history
- **Work Progress** - View and update assigned tasks

---

## Data Storage

### Database Location
- **Windows**: `attendance_app/attendance.db` (SQLite file)
- **Mac/Linux**: Same location

### Database Backup
```bash
# Manual backup
cp attendance_app/attendance.db attendance_app/attendance_backup_DATE.db

# Or copy from file explorer
```

### Change Database Location
Edit `config.py`:
```python
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///attendance.db")
# Change to:
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///C:/path/to/custom/location/attendance.db")
```

---

## Security Best Practices

1. **Change Default Password**
   - ✅ Done immediately after first login

2. **Set Environment Variables** (Production)
   Create `.env` file in `attendance_app/` folder:
   ```
   COOKIE_PASSWORD=your-secure-random-string
   COMPANY_NAME=Your Company Name
   ```

3. **Database Backup**
   - Back up `attendance.db` regularly
   - Store backups in separate location

4. **Access Control**
   - Use strong passwords (minimum 6 characters)
   - Only give admin access to trusted users
   - Review employee permissions regularly

---

## Troubleshooting

### App Won't Start
```bash
# Clear cache and restart
rm -rf .streamlit/cache
streamlit run app.py --logger.level=debug
```

### Database Lock Error
- Close all instances of the app
- Wait 10 seconds
- Restart the app

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Can't See Changes After Code Edit
```bash
# Restart with --logger.level=debug
streamlit run app.py --logger.level=debug
```

---

## Export & Reporting

### Excel Export
- Go to **Reports** page
- Select date range
- Click **Download Excel**

### PDF Export
- Go to **Reports** page
- Click **Download PDF**

### Bulk Data Export
- Exports are stored in `exports/` folder
- Can be imported to other systems

---

## Offline Operation Checklist

- [x] Python installed locally
- [x] All dependencies installed (pip install -r requirements.txt)
- [x] Database created on first run
- [x] Admin password changed
- [x] Test with sample employee data
- [x] Create regular backups of `attendance.db`

---

## Network Deployment (Optional)

### Share on LAN (Local Network)

```bash
# Find your computer's IP address
ipconfig getifaddr en0  # Mac
hostname -I            # Linux
ipconfig                # Windows (look for IPv4 Address)

# Start app listening on all network interfaces
streamlit run app.py --server.address 0.0.0.0
```

Then access from other computers:
```
http://YOUR_IP_ADDRESS:8501
```

### Important Notes:
- ⚠️ **Not secure for internet** - use only on trusted networks
- ⚠️ **Single database** - only one write at a time
- ⚠️ **Production** - use proper web server (Nginx, etc.)

---

## Cloud Deployment (Optional - With Internet)

To deploy on Streamlit Cloud (requires internet):

1. Push code to GitHub
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Create account and connect GitHub
4. Deploy repository
5. Set secrets in Cloud Settings

---

## Contact & Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review application logs: `streamlit run app.py --logger.level=debug`
3. Check database integrity: See if `attendance.db` exists and is readable

---

## Version Info
- **Streamlit**: 1.36.0+
- **Python**: 3.8+
- **Database**: SQLite (offline)
- **UI**: Modern Dark Theme

**Last Updated**: 2024
**Status**: ✅ Fully Offline Compatible
