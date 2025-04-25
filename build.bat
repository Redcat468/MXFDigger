@echo off
REM ──────── build.bat ──────────────────────────────────────
REM Script de compilation de l'application MXFDigger
setlocal enabledelayedexpansion

echo.
echo ================================
echo   Compilation de MXFDigger
echo ================================
echo.

REM Vérifier que PyInstaller est installé
where pyinstaller >nul 2>&1
if ERRORLEVEL 1 (
    echo ERREUR : PyInstaller n'est pas installé.
    echo Lancez "pip install pyinstaller" puis relancez ce script.
    exit /b 1
)

REM Nettoyer les anciennes builds
if exist build rd /s /q build
if exist MXFDigger.spec del /q MXFDigger.spec

echo Démarrage de la compilation avec PyInstaller...

REM Construire la commande PyInstaller
set "PYI_CMD=pyinstaller --noconfirm --clean --onefile --name MXFDigger"
set "PYI_CMD=!PYI_CMD!^ --add-data "static\images\logo.ico;static/images""
set "PYI_CMD=!PYI_CMD!^ --add-data "static\images\banner.svg;static/images""
set "PYI_CMD=!PYI_CMD! app.py"

echo !PYI_CMD!
%PYI_CMD%
if ERRORLEVEL 1 (
    echo ERREUR : Échec de la compilation.
    exit /b 1
)

echo.
echo Compilation terminée avec succès.
echo Le binaire et les assets se trouvent dans dist\
endlocal
exit /b 0

