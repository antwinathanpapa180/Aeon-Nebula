@echo off
title Aeon Nebula System Gateway
cls

echo ===================================================
echo [ AEON NEBULA ] - STARTING INTERNAL MATRIX GATEWAY
echo ===================================================
echo.

:: 1. Initialize Conda environment path natively
call %USERPROFILE%\anaconda3\Scripts\activate.bat %USERPROFILE%\anaconda3

:: 2. Activate your dedicated virtual environment
call conda activate aeon_nebula

:: 3. Launch the presentation layer cleanly
streamlit run aeon_nebula_ui.py --client.toolbarMode=hidden

pause