@echo off
title TRENVO - Music Trend Predictor
echo =======================================================
echo          Starting TRENVO Music Trend Predictor...
echo =======================================================
echo.

set "PY_EXE=C:\Users\Dell\AppData\Local\Python\pythoncore-3.14-64\python.exe"

if exist "%PY_EXE%" (
    set "PYTHON_CMD=%PY_EXE%"
) else (
    set "PYTHON_CMD=python"
)

if exist "gui\app.py" (
    "%PYTHON_CMD%" -m streamlit run gui\app.py
) else if exist "app.py" (
    "%PYTHON_CMD%" -m streamlit run app.py
) else if exist "..\gui\app.py" (
    cd ..
    "%PYTHON_CMD%" -m streamlit run gui\app.py
) else (
    echo [ERROR] Could not find gui\app.py!
)

echo.
pause
