@echo off
echo Installing SEEKER dependencies...
echo.

echo Installing requests library...
pip install requests

echo.
echo Installing python-dotenv...
pip install python-dotenv

echo.
echo Installing FastAPI and uvicorn...
pip install fastapi uvicorn

echo.
echo Dependencies installed successfully!
echo.
echo Next steps:
echo 1. Install MongoDB from: https://www.mongodb.com/try/download/community
echo 2. Run: python check_mongodb.py

echo 3. Start SEEKER: uvicorn app.main:app --reload
echo.
pause 