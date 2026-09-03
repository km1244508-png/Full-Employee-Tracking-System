# ⚡ Quick Reference Guide

## 🚀 START HERE

### Windows
```bash
cd attendance_app
start_app.bat
```

### Mac/Linux  
```bash
cd attendance_app
chmod +x start_app.sh
./start_app.sh
```

### Access App
Open: `http://localhost:8501`

---

## 🔑 Default Login

| Field | Value |
|-------|-------|
| **Username** | admin |
| **Password** | admin123 |

⚠️ **CHANGE PASSWORD IMMEDIATELY!**

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **README_OFFLINE.md** | Complete user guide + features |
| **DEPLOYMENT_GUIDE.md** | Setup + deployment instructions |
| **COMPLETION_SUMMARY.md** | What was changed/updated |
| **FINAL_REPORT.md** | Executive summary + status |
| **.env.example** | Environment configuration |

---

## 🎯 Common Tasks

### Change Admin Password
1. Click **Employee Management**
2. Click **Change My Password**
3. Enter old (admin123) and new password
4. Done ✅

### Add New Employee
1. Click **Employee Management**
2. Click **Add New Employee**
3. Fill form and submit
4. Employee can now login ✅

### Mark Attendance
1. Click **Mark Attendance**
2. Select employee
3. Click **Check In** / **Check Out**
4. View status ✅

### Generate Report
1. Click **Reports**
2. Select date range
3. Click **Generate**
4. Export to Excel/PDF ✅

### Backup Database
```bash
# Copy the attendance.db file
cp attendance_app/attendance.db backup_location/attendance.db
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| App won't start | Delete `.streamlit/cache` folder |
| Can't login | Make sure Python installed correctly |
| Slow | Close other programs, restart app |
| Port in use | Run: `streamlit run app.py --server.port 8502` |
| Lost data | Restore from backup: `cp backup.db attendance.db` |

---

## 📋 System Requirements

✅ Python 3.8+  
✅ 4GB RAM  
✅ 100MB disk space  
✅ Windows/Mac/Linux  
✅ No internet (after setup)  

---

## 🔒 Important Files

| File | Purpose |
|------|---------|
| `attendance.db` | **DATABASE** - Back it up daily! |
| `.streamlit/` | Config files |
| `.env` | Environment variables (optional) |
| `start_app.bat/sh` | Launcher scripts |

---

## 🎯 Key Features

✅ Attendance tracking  
✅ Hours calculation  
✅ Overtime detection  
✅ Work progress tracking  
✅ Real-time dashboard  
✅ Excel/PDF reports  
✅ Employee management  
✅ Role-based access  
✅ Completely offline  

---

## ✨ Modern Dark Theme

- 🌙 Easy on eyes
- 🎨 Professional look  
- 📱 Mobile friendly
- 🚀 Fast performance

---

## 💾 Backup Procedure

```bash
# Create daily backup
copy attendance.db attendance_backup_DATE.db

# Restore from backup if needed
copy attendance_backup_DATE.db attendance.db
```

---

## 🌐 Network Deployment (Optional)

### Share on Local Network
```bash
# Get your IP
ipconfig getifaddr en0  # Mac
hostname -I              # Linux

# Run on network
streamlit run app.py --server.address 0.0.0.0

# Access from other computers
# http://YOUR_IP:8501
```

---

## 📞 Help Resources

- **README_OFFLINE.md** → Full user guide
- **DEPLOYMENT_GUIDE.md** → Setup details  
- **FINAL_REPORT.md** → Technical summary
- In-app help sections → Built-in guidance

---

## ✅ Verification

### Check Installation
```bash
python -m streamlit --version
sqlite3 attendance.db ".tables"
```

### Test Offline Mode
1. Disconnect internet
2. Run: `streamlit run app.py`
3. All features should work ✅

---

## 🎉 You're All Set!

Your Attendance Tracker is:
✅ Ready to use
✅ Fully offline  
✅ Professionally styled
✅ Well documented

**Start here: `start_app.bat` (Windows) or `start_app.sh` (Mac/Linux)**

Enjoy! 🚀

---

*Quick Reference v1.0*  
*Attendance & Work Progress Tracker*  
*All offline. All local. All good.* ✨
