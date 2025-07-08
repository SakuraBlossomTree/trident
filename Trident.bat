@echo off
REM This batch script is a launcher for the Trident chess engine.
REM It starts the engine using the bundled PyPy interpreter.

REM The special variable %~dp0 expands to the directory where this batch script is located.
REM This makes the script portable, so it doesn't matter where you place the TridentPy folder.

REM Execute the engine:
REM 1. Call the pypy3.exe located in the 'pypy' subfolder.
REM 2. Pass main.py as the script to run.
"%~dp0pypy\pypy3.11.exe" "%~dp0main.py"