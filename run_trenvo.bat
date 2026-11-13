@echo off
title TRENVO - Music Trend Predictor
echo =======================================================
echo          Starting TRENVO Music Trend Predictor...
echo =======================================================
echo.

if exist "gui\app.py" (
    streamlit run gui\app.py
) else if exist "TRENVO\gui\app.py" (
    cd TRENVO
    streamlit run gui\app.py
) else (
    echo [ERROR] Could not find gui\app.py!
    pause
)
