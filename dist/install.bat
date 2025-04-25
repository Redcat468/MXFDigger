@echo off
setlocal enabledelayedexpansion

set SERVICE_NAME=MXFDiggerService
set NSSM_PATH=%~dp0nssm.exe
set INSTALL_DIR=%ProgramFiles%\MXFDigger
set EXE_NAME=MXFDigger.exe
set SETTINGS_CONF=settings.conf

:: Vérifier les droits administrateur
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Erreur : exécutez ce script en tant qu’Administrateur !
    pause
    exit /b 1
)

echo.
echo ================================
echo   Installation du service : %SERVICE_NAME%
echo   Dossier cible          : %INSTALL_DIR%
echo ================================
echo.

:: Créer le dossier d’installation
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    if errorlevel 1 (
        echo ERREUR : impossible de créer %INSTALL_DIR%.
        exit /b 1
    )
)

echo Copie de l’exécutable et du fichier de configuration...
copy /y "%~dp0%EXE_NAME%" "%INSTALL_DIR%\%EXE_NAME%" >nul
copy /y "%~dp0%SETTINGS_CONF%" "%INSTALL_DIR%\%SETTINGS_CONF%" >nul
if errorlevel 1 (
    echo ERREUR : échec de la copie des fichiers.
    pause
    exit /b 1
)

:: Supprimer un ancien service si présent
sc query "%SERVICE_NAME%" >nul 2>&1
if not errorlevel 1 (
    echo Ancien service détecté : suppression...
    sc stop "%SERVICE_NAME%" >nul 2>&1
    sc delete "%SERVICE_NAME%" >nul 2>&1
    timeout /t 2 /nobreak >nul
)

:: Installer et démarrer le service via NSSM
"%NSSM_PATH%" install "%SERVICE_NAME%" "%INSTALL_DIR%\%EXE_NAME%"
"%NSSM_PATH%" set "%SERVICE_NAME%" Start SERVICE_AUTO_START
"%NSSM_PATH%" start "%SERVICE_NAME%"

:: Vérifier le statut
echo.
echo Vérification du statut du service...
"%NSSM_PATH%" status "%SERVICE_NAME%"
if errorlevel 1 (
    echo ❌ Le service n’a pas démarré correctement.
    pause
    exit /b 1
)

echo 🎉 Service %SERVICE_NAME% installé et démarré avec succès !
pause
exit /b 0