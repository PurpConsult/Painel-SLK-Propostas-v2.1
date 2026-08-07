@echo off
echo ===================================
echo    SLK Propostas Pro - VendAI
echo ===================================
echo.
echo Verificando dependencias...
pip install -r requirements.txt >nul 2>&1
echo.
echo Iniciando servidor...
echo Acesse: http://localhost:5000
echo.
python app.py
pause
