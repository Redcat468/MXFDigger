:: uninstall_mxfdigger_service.bat
@echo off
setlocal enabledelayedexpansion

set SERVICE_NAME=MXFDiggerService
set NSSM_PATH=%~dp0nssm.exe
set INSTALL_DIR=C:\Program Files\MXFDigger

:: Vérifier les droits administrateur
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Erreur : exécutez ce script en tant qu’Administrateur !
    pause
    exit /b 1
)

echo.
echo ================================
echo   Désinstallation du service : %SERVICE_NAME%
echo   Dossier cible             : %INSTALL_DIR%
echo ================================

echo Arrêt du service...
"%NSSM_PATH%" stop "%SERVICE_NAME%"

echo Suppression du service...
"%NSSM_PATH%" remove "%SERVICE_NAME%" confirm

:: Supprimer le dossier d’installation
if exist "%INSTALL_DIR%" (
    echo 🗑️ Suppression du dossier %INSTALL_DIR%...
    rmdir /s /q "%INSTALL_DIR%"
) else (
    echo ✅ Dossier %INSTALL_DIR% déjà supprimé.
)

echo 🎉 Désinstallation terminée avec succès !
pause
exit /b 0