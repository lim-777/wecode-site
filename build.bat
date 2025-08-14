@echo off
REM ============================
REM  WECODE 핑퐁 exe 빌드 스크립트
REM ============================

echo [1/3] PyInstaller 설치 여부 확인 중...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller가 없습니다. 설치 중...
    pip install pyinstaller
)

echo [2/3] EXE 빌드 시작...
pyinstaller --noconfirm --onefile --windowed ^
    --add-data "인트로.mp4;." ^
    --add-data "인트로.mp3;." ^
    pingpong_game.py

echo [3/3] 빌드 완료!
echo dist\pingpong_game.exe 파일을 실행하면 됩니다.

pause
