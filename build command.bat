@echo off
title Build Tool - Build TsukiNotes
echo Start Build The TsukiNotes
echo ���뱣��py�ڵ�ǰ�ļ��У�tsuki�ļ����ڵ�ǰ�ļ���

REM ����Ƿ���� TsukiNotes.py �ļ�
if not exist "TsukiNotes.py" (
    echo Error: TsukiNotes.py �ļ������ڣ�
    pause
    exit /b
)

REM ��� tsuki Ŀ¼�Ƿ����
if not exist "tsuki" (
    echo Error: tsuki �ļ��в����ڣ�
    pause
    exit /b
)

REM ��� tsuki/assets/kernel Ŀ¼�Ƿ����
if not exist "tsuki/assets/kernel" (
    echo Error: tsuki/assets/kernel �ļ��в����ڣ�
    pause
    exit /b
)

REM ��� logo.ico �ļ��Ƿ����
if not exist "tsuki/assets/GUI/ico/logo.ico" (
    echo Error: logo.ico �ļ������ڣ�
    pause
    exit /b
)

REM ��װ pip �� pyinstaller
pip install --upgrade pip
pip install pyinstaller

REM ִ�� pyinstaller ����
pyinstaller --add-data "tsuki/assets/kernel/*.pyd;tsuki/assets/kernel" "TsukiNotes.py" -i "tsuki/assets/GUI/ico/logo.ico" -w

pause
