# MongoDB Setup Guide for SEEKER AI Orchestration System

This guide will help you install and configure MongoDB for the SEEKER AI Orchestration System.

## Prerequisites

- Windows 10/11
- Administrator privileges for installation
- Python 3.8+ (already installed)

## Step 1: Download MongoDB Community Server

1. **Visit the MongoDB Download Page:**
   - Go to: https://www.mongodb.com/try/download/community

2. **Select Download Options:**
   - **Version:** 7.0 (latest stable)
   - **Platform:** Windows
   - **Package:** msi
   - Click **"Download"**

## Step 2: Install MongoDB

1. **Run the Installer:**
   - Double-click the downloaded `.msi` file
   - Click **"Next"** to begin installation

2. **Choose Installation Type:**
   - Select **"Complete"** installation
   - Click **"Next"**

3. **Service Configuration:**
   - ✅ **Install MongoDB as a Service** (recommended)
   - Service Name: `MongoDB`
   - Data Directory: `C:\Program Files\MongoDB\Server\7.0\data`
   - Log Directory: `C:\Program Files\MongoDB\Server\7.0\log`
   - Click **"Next"**

4. **Install MongoDB Compass:**
   - ✅ **Install MongoDB Compass** (recommended - GUI tool)
   - Click **"Next"**

5. **Complete Installation:**
   - Click **"Install"**
   - Wait for installation to complete
   - Click **"Finish"**

## Step 3: Verify Installation

### Option A: Use the Setup Script (Recommended)

Run the provided setup script to automatically check everything:

```powershell
python setup_mongodb.py
```

### Option B: Manual Verification

1. **Check MongoDB Service:**
   ```powershell
   Get-Service -Name "MongoDB"
   ```

2. **Test MongoDB Connection:**
   ```powershell
   mongosh --eval "db.runCommand('ping')"
   ```

3. **Check MongoDB Version:**
   ```powershell
   mongod --version
   ```

## Step 4: Start MongoDB Service (if needed)

If the MongoDB service is not running:

### Method 1: Using PowerShell
```powershell
Start-Service -Name "MongoDB"
```

### Method 2: Using Services Manager
1. Press `Win + R`, type `services.msc`, press Enter
2. Find **"MongoDB"** in the list
3. Right-click and select **"Start"**

### Method 3: Using Command Prompt (as Administrator)
```cmd
net start MongoDB
```

## Step 5: Configure SEEKER for MongoDB

The SEEKER system is already configured to use MongoDB. The default settings are:

- **Connection URI:** `mongodb://localhost:27017`
- **Database Name:** `seeker_db`
- **Port:** `27017`

### Environment Variables

You can customize the MongoDB connection by setting environment variables:

```bash
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
DB_NAME=seeker_db

# Environment Settings
ENVIRONMENT=development
DEBUG=true
```

## Step 6: Test SEEKER with MongoDB

Once MongoDB is running:

1. **Start the SEEKER Server:**
   ```powershell
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Test the API:**
   ```powershell
   python test_seeker.py
   ```

3. **View API Documentation:**
   - Open: http://localhost:8000/docs

## Troubleshooting

### Issue: "MongoDB service not found"
**Solution:** Reinstall MongoDB and ensure "Install as a Service" is selected.

### Issue: "Connection refused on port 27017"
**Solution:** 
1. Check if MongoDB service is running
2. Verify no firewall blocking port 27017
3. Check if another application is using port 27017

### Issue: "Permission denied"
**Solution:** Run PowerShell as Administrator.

### Issue: "MongoDB not in PATH"
**Solution:** 
1. Add MongoDB to PATH: `C:\Program Files\MongoDB\Server\7.0\bin`
2. Or use full path: `"C:\Program Files\MongoDB\Server\7.0\bin\mongosh.exe"`

## MongoDB Compass (GUI Tool)

MongoDB Compass provides a graphical interface to:
- Browse databases and collections
- View and edit documents
- Monitor database performance
- Execute queries

**Launch Compass:**
- Start menu → MongoDB Compass
- Or run: `mongodb-compass`

**Connect to SEEKER Database:**
- Connection string: `mongodb://localhost:27017`
- Database: `seeker_db`

## Data Persistence

MongoDB will automatically store SEEKER data in:
- **Data Directory:** `C:\Program Files\MongoDB\Server\7.0\data`
- **Log Directory:** `C:\Program Files\MongoDB\Server\7.0\log`

The SEEKER system will create the following collections:
- `users` - User information
- `devices` - Device registrations
- `ai_agents` - AI agent configurations
- `task_requests` - User requests
- `agent_responses` - AI agent responses
- `sair_loop_data` - Learning loop data

## Security Considerations

For production deployment:
1. Enable authentication
2. Use SSL/TLS encryption
3. Configure network access controls
4. Regular backups
5. Monitor database performance

## Next Steps

After MongoDB is successfully installed and running:

1. ✅ **Start SEEKER Server:** `uvicorn app.main:app --reload`
2. ✅ **Run Test Suite:** `python test_seeker.py`
3. ✅ **Explore API Docs:** http://localhost:8000/docs
4. ✅ **Monitor with Compass:** Launch MongoDB Compass

## Support

If you encounter issues:
1. Check MongoDB logs: `C:\Program Files\MongoDB\Server\7.0\log\mongod.log`
2. Run the setup script: `python setup_mongodb.py`
3. Verify service status: `Get-Service MongoDB`
4. Test connection: `mongosh --eval "db.runCommand('ping')"`

---

**🎉 Congratulations!** Your SEEKER AI Orchestration System is now ready with full MongoDB persistence! 