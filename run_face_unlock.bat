@echo off
echo ================================
echo Face Unlock System Starting...
echo ================================
echo.

cd /d "C:\face_unlock"
echo Current directory: %CD%
echo.

echo Activating virtual environment...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated!
) else (
    echo ERROR: Virtual environment not found!
    echo Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo Installing required packages...
    pip install opencv-python face_recognition numpy
)

echo.
echo Running face unlock script...
python face_unlock.py

echo.
echo ================================
echo Script finished.
echo ================================
pause
