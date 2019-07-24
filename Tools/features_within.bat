@echo off
:: DOS wrapper to db command

setlocal

:: Check args
if "%~3"=="" (
    echo Usage: %~0 ^<db_name^> ^<polygon_file^> ^<feature_type^>
    exit /b 1
)

call myw_db %1 run %~dpn0.py %1 %2 %3
