# Quick Setup Guide for SEEKER

## Step 1: Install Missing Dependencies

First, install the missing Python packages:

```powershell
pip install requests
pip install python-dotenv
```

## Step 2: Install MongoDB

### Download MongoDB:
1. Go to: https://www.mongodb.com/try/download/community
2. Select:
   - Version: 7.0
   - Platform: Windows
   - Package: msi
3. Click "Download"

### Install MongoDB:
1. Run the downloaded `.msi` file
2. Choose "Complete" installation
3. ✅ **Install MongoDB as a Service** (IMPORTANT!)
4. ✅ Install MongoDB Compass (optional GUI)
5. Complete installation

## Step 3: Verify Installation

Run the check script:
```powershell
python check_mongodb.py
```

## Step 4: Start MongoDB Service (if needed)

If MongoDB service is not running:
```powershell
Start-Service -Name "MongoDB"
```

## Step 5: Test SEEKER

Once MongoDB is running:
```powershell
# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, test the API
python test_seeker.py
```

## Troubleshooting

### If MongoDB service not found:
- Reinstall MongoDB with "Install as Service" option

### If connection refused:
- Check if MongoDB service is running: `Get-Service MongoDB`
- Start service: `Start-Service MongoDB`

### If uvicorn not found:
- Install FastAPI: `pip install fastapi uvicorn`

### If requests not found:
- Install requests: `pip install requests`

## Expected Results

After successful setup:
- ✅ MongoDB service running
- ✅ SEEKER server starts without errors
- ✅ API endpoints work with database persistence
- ✅ Test suite runs successfully 