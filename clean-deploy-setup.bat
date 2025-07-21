@echo off
echo 🚀 KENTECH MULTIBOT Clean Deployment Setup
echo ==========================================

echo.
echo This script will create a clean deployment directory
echo without any "levanter" references in the path.
echo.

set "CLEAN_DIR=C:\kentech-multibot"

echo ✅ Creating clean directory: %CLEAN_DIR%
if exist "%CLEAN_DIR%" (
    echo ⚠️ Directory already exists. Removing...
    rmdir /s /q "%CLEAN_DIR%"
)

mkdir "%CLEAN_DIR%"

echo ✅ Copying KENTECH MULTIBOT files...
xcopy /e /h /k /y * "%CLEAN_DIR%\" > nul

echo ✅ Navigating to clean directory...
cd /d "%CLEAN_DIR%"

echo.
echo 🎉 Clean setup complete!
echo.
echo ✅ Your KENTECH MULTIBOT is now in: %CLEAN_DIR%
echo ✅ No more "levanter" path references!
echo ✅ You can now run deploy.sh from this clean location
echo.

echo Opening clean directory...
explorer "%CLEAN_DIR%"

echo.
echo 📋 Next steps:
echo 1. Use the files in: %CLEAN_DIR%
echo 2. Run deploy.sh from there
echo 3. All paths will show "kentech-multibot" instead of "levanter"
echo.

pause
