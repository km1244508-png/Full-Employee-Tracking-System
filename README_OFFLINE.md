# 🕒 Attendance & Work Progress Tracker

A professional, modern Streamlit application for tracking employee attendance, working hours, and task progress with **complete offline capability**.

## ✨ Features

### Attendance Management
- ✅ Digital check-in/check-out system
- ✅ Real-time hours tracking
- ✅ Late arrival detection with grace period
- ✅ Overtime calculation
- ✅ Half-day and absence tracking
- ✅ Custom shift schedules per employee

### Work Progress Tracking
- ✅ Task assignment and management
- ✅ Task status tracking (Not Started, In Progress, Completed, On Hold)
- ✅ Deadline management
- ✅ Progress reports and analytics

### Reporting & Analytics
- ✅ Real-time dashboard with KPIs
- ✅ Daily, weekly, and monthly reports
- ✅ Excel export capabilities
- ✅ PDF report generation
- ✅ Individual and comparative analytics

### Administration
- ✅ Employee management (add, edit, deactivate)
- ✅ Role-based access control (Admin, Employee)
- ✅ User account management
- ✅ Password management and reset
- ✅ Department and designation tracking

### Technology
- ✅ **Completely Offline** - Works without internet after setup
- ✅ **Modern Dark UI** - Professional and eye-friendly
- ✅ **SQLite Database** - No server required
- ✅ **Secure Authentication** - BCrypt password hashing
- ✅ **Session Persistence** - Browser cookies for seamless access
- ✅ **Cross-Platform** - Windows, Mac, Linux

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- ~100MB disk space

### Installation (5 minutes)

#### Windows
```bash
# Navigate to application folder
cd attendance_app

# Run setup script (automatic)
start_app.bat
```

#### Mac/Linux
```bash
# Navigate to application folder
cd attendance_app

# Make script executable
chmod +x start_app.sh

# Run setup script (automatic)
./start_app.sh
```

#### Manual Setup
```bash
# Install dependencies (only needed once)
pip install -r requirements.txt

# Start the application
streamlit run app.py
```

### First Login
- **Default Username**: `admin`
- **Default Password**: `admin123`

⚠️ **Change the admin password immediately!**
- Go to Employee Management → Change My Password

---

## 📖 Usage Guide

### For Administrators

#### Employee Management
1. Navigate to **Employee Management** page
2. **Add Employee**: Click "Add New Employee", fill details
3. **Edit Employee**: Select employee and update information
4. **Deactivate**: Disable employee account while keeping records

#### Mark Attendance
1. Go to **Mark Attendance**
2. Select employee (or auto-selected for non-admins)
3. Click **Check In** at start of shift
4. Click **Check Out** at end of shift
5. System automatically calculates hours and status

#### Dashboard
- Real-time overview of all employees
- Attendance status summary
- Work progress metrics
- Quick KPIs

#### Reports
- **Daily Report**: Single day overview
- **Weekly Report**: 7-day summary
- **Monthly Report**: Full month analytics
- Export to Excel or PDF

#### Work Progress
- Assign tasks to employees
- Track progress
- Set deadlines
- Monitor completion

### For Employees

#### Personal Dashboard
- View your attendance status
- Check today's hours worked
- See work progress status

#### Attendance Records
- View your attendance history
- Export reports as PDF/Excel
- Check calculated hours and overtime

#### Work Progress
- View assigned tasks
- Update task status
- Comment on tasks

---

## 🔒 Security & Data Protection

### Built-in Security
- **Password Hashing**: BCrypt (industry standard)
- **Session Cookies**: Encrypted browser storage
- **Access Control**: Role-based permissions
- **Input Validation**: SQL injection prevention

### Data Backup
```bash
# Create backup
copy attendance.db attendance_backup_DATE.db

# Restore from backup
copy attendance_backup_DATE.db attendance.db
```

### Best Practices
1. ✅ Change default admin password immediately
2. ✅ Use strong passwords (minimum 6 characters recommended: 12+)
3. ✅ Regular database backups (daily recommended)
4. ✅ Restrict admin access to trusted users
5. ✅ Review user accounts regularly

---

## 📊 Database Information

### Storage Location
- **Windows**: `attendance_app\attendance.db`
- **Mac/Linux**: `attendance_app/attendance.db`

### Database Type
- SQLite3 (no server required)
- Self-contained single file
- Automatic backup friendly

### Data Structure
- **Users Table**: Login credentials and roles
- **Employees Table**: Employee information
- **Attendance Table**: Check-in/check-out records
- **Tasks Table**: Work progress tracking

---

## ⚙️ Configuration

### Environment Variables (Optional)
Create `.env` file in application folder:

```ini
# Company name
COMPANY_NAME=Your Company Name

# Database (defaults to SQLite)
DATABASE_URL=sqlite:///attendance.db

# Cookie security (production)
COOKIE_PASSWORD=your-secure-key

# Export directory
EXPORT_DIR=exports
```

### Streamlit Configuration
Edit `.streamlit/config.toml` for:
- Port number
- UI theme
- Server settings
- Performance tuning

---

## 🔧 Troubleshooting

### "Command not found: streamlit"
```bash
# Reinstall Streamlit
pip install streamlit --upgrade

# Or use python module
python -m streamlit run app.py
```

### "Module not found" errors
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Database locked / corrupted
```bash
# Delete cache and restart
rm -rf .streamlit/cache
streamlit run app.py
```

### Port already in use
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Slow performance
```bash
# Clear cache and optimize
rm -rf .streamlit/cache
streamlit run app.py --logger.level=warning
```

---

## 📤 Deployment Options

### Local Single-Machine
- Default setup
- Best for small teams
- Backup the `attendance.db` file

### Network Sharing (LAN)
```bash
# Find your IP address
ipconfig getifaddr en0  # Mac
hostname -I             # Linux

# Run on network
streamlit run app.py --server.address 0.0.0.0
```
Access from: `http://YOUR_IP:8501`

### Cloud Deployment (Optional)
- Deploy on Streamlit Cloud (requires GitHub)
- Use custom hosting (requires web server)
- See `DEPLOYMENT_GUIDE.md` for details

---

## 🎯 Offline Operation

### What Works Offline?
✅ All core features  
✅ Attendance tracking  
✅ Reports generation  
✅ Excel/PDF export  
✅ Employee management  
✅ Task tracking  

### No Internet Needed For:
✅ Day-to-day operations  
✅ Report generation  
✅ Employee management  
✅ Data backup  

### Internet Required For:
❌ First-time package installation only  
❌ Cloud deployment (optional)  

---

## 📝 Example Workflows

### Workflow 1: Mark Attendance
1. Employee arrives at work
2. Admin/Employee marks check-in
3. System records time
4. Employee marks check-out
5. System calculates hours and status

### Workflow 2: Generate Weekly Report
1. Go to Reports
2. Select "Weekly"
3. Choose date range
4. Click "Generate Report"
5. Export to Excel/PDF

### Workflow 3: Assign Task
1. Go to Work Progress
2. Click "Assign New Task"
3. Select employee
4. Enter task details and deadline
5. Task appears on employee dashboard

---

## 📞 Support & Documentation

### Help Resources
1. **README.md** - This file
2. **DEPLOYMENT_GUIDE.md** - Offline deployment details
3. **Application Help** - In-app help sections
4. **Config files** - `.env.example`, `.streamlit/config.toml`

### Reporting Issues
When reporting issues, include:
- Error message (copy from terminal)
- Steps to reproduce
- Python version (`python --version`)
- OS information

---

## 🔄 Regular Maintenance

### Daily
- Back up `attendance.db`
- Review attendance reports
- Monitor system status

### Weekly
- Verify all employee accounts
- Check data integrity
- Export reports

### Monthly
- Archive old reports
- Clean up old logs
- Update employee information
- Review security

---

## 📊 Performance Tips

### For Large Teams (100+ employees)
- Run on dedicated machine
- Use SSD for database
- Schedule reports during off-hours
- Optimize network for LAN deployment

### Optimize Database
```bash
# Periodically rebuild index (SQLite)
# This is automatic but can be forced
sqlite3 attendance.db "VACUUM;"
```

---

## 📄 License & Credits

**Application**: Employee Attendance & Work Progress Tracker  
**Built with**: Streamlit, SQLAlchemy, BCrypt  
**Status**: Production Ready  
**Last Updated**: 2024  

---

## ✅ Verification Checklist

Before going live:
- [ ] Python installed and working
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database created (automatic on first run)
- [ ] Admin password changed
- [ ] Sample employees added
- [ ] Attendance marked for testing
- [ ] Report generation tested
- [ ] Database backup created
- [ ] `.env` file configured (if needed)
- [ ] Ready for production use!

---

## 🎉 Ready to Use!

Your application is now configured for **offline operation**. All data is stored locally and no internet connection is needed for daily use.

**Start the app:**
```bash
streamlit run app.py
```

**Access at:** http://localhost:8501

Enjoy! 🚀
