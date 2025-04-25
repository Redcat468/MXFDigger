@echo off
REM ─── install_mxfdigger_service.bat ───────────────────
REM Installe MXFDiggerService via NSSM
setlocal

set "NSSM_EXE=%~dp0nssm.exe"
set "SERVICE_NAME=MXFDiggerService"
set "BIN_PATH=%~dp0MXFDigger.exe"

if not exist "%NSSM_EXE%" (
    echo ERREUR : nssm.exe introuvable dans %~dp0
    exit /b 1
)

echo ================================
echo   Installation du service : %SERVICE_NAME%
echo ================================
echo.

"%NSSM_EXE%" install "%SERVICE_NAME%" "%BIN_PATH%"
"%NSSM_EXE%" set "%SERVICE_NAME%" Start SERVICE_AUTO_START

echo Service %SERVICE_NAME% installé avec NSSM.
echo Démarrage du service…
"%NSSM_EXE%" start "%SERVICE_NAME%"

endlocal
exit /b 0
