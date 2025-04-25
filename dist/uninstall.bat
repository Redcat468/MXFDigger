@echo off
REM ── uninstall_mxfdigger_service.bat ────────────────
REM Supprime MXFDiggerService via NSSM
setlocal

set "NSSM_EXE=%~dp0nssm.exe"
set "SERVICE_NAME=MXFDiggerService"

if not exist "%NSSM_EXE%" (
    echo ERREUR : nssm.exe introuvable dans %~dp0
    exit /b 1
)

echo ================================
echo   Désinstallation du service : %SERVICE_NAME%
echo ================================
echo.

"%NSSM_EXE%" stop "%SERVICE_NAME%"
"%NSSM_EXE%" remove "%SERVICE_NAME%" confirm

echo Service %SERVICE_NAME% supprimé.
endlocal
exit /b 0
