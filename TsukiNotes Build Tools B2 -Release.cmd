@echo off
chcp 936 >nul
title TsukiNotes Build Tools B2 -Release
color 0E
echo ================================================
echo         TsukiNotes Build Tools B2
echo                Release Version
echo ================================================
echo.
echo [��ʾ] ���ű�����TsukiNotesVer1.6.3�汾
echo [��ʾ] ��ʼ����ɣ��ȴ��ű�ִ��.....
timeout /t 3 >nul

:: ����������ļ�
echo [��ʾ] Starting....
echo [���] ���ڼ����Ŀ�ļ�...
if not exist "TsukiNotes.py" (
    color 0C
    echo [����] δ�ҵ� TsukiNotes.py��
    echo [��ʾ] ��ȷ������ȷ��Ŀ¼�����д˽ű�
    echo [��ʾ] ��ǰĿ¼: %CD%
    goto :error
)
echo [�ɹ�] �ҵ��������ļ���
echo.

:: �����Ŀ�ṹ
echo [���] ���ڼ����Ŀ�ṹ...
if not exist "tsuki" (
    color 0C
    echo [����] δ�ҵ� tsuki Ŀ¼��
    echo [��ʾ] ��ȷ����������Ŀ�ṹ����
    goto :error
)
if not exist "tsuki\assets" (
    color 0C
    echo [����] δ�ҵ� assets Ŀ¼��
    goto :error
)
echo [�ɹ�] ��Ŀ�ṹ���ͨ����
echo.

:: ��� Python ����
echo [���] ���ڼ�� Python ����...
python --version > nul 2>&1
if errorlevel 1 (
    color 0C
    echo [����] δ��⵽ Python ��������ȷ���Ѱ�װ Python��
    goto :error
)
echo [�ɹ�] Python �������ͨ����
echo.

:: ��� PyInstaller
echo [���] ���ڼ�� PyInstaller...
pyinstaller --version > nul 2>&1
if errorlevel 1 (
    echo [��ʾ] ���ڰ�װ PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        color 0C
        echo [����] PyInstaller ��װʧ�ܣ�
        goto :error
    )
)
echo [�ɹ�] PyInstaller ׼��������
echo.

echo [��Ϣ] ��ʼ���� TsukiNotes...
echo [��Ϣ] �������Ҫ������ʱ�䣬�����ĵȴ�...
echo.
echo ================================================

pyinstaller --name TsukiNotes ^
            --icon tsuki/assets/resources/GUI/logo.png ^
            --add-data "tsuki/assets;tsuki/assets" ^
            --add-data "tsuki/core;tsuki/core" ^
            --add-data "tsuki/pages;tsuki/pages" ^
            --add-data "tsuki/ui;tsuki/ui" ^
            --add-data "VERSION;." ^
            --add-data "requirements.txt;." ^
            --hidden-import PyQt5 ^
            --hidden-import markdown2 ^
            --hidden-import html2text ^
            --hidden-import chardet ^
            --hidden-import configparser ^
            --hidden-import colorlog ^
            --hidden-import sympy ^
            --hidden-import ping3 ^
            --noconsole ^
            --noconfirm ^
            TsukiNotes.py

if errorlevel 1 (
    color 0C
    echo.
    echo [����] ���������г��ִ���
    goto :error
)

echo.
echo ================================================
echo [�ɹ�] TsukiNotes ������ɣ�
echo [��Ϣ] ���Ŀ¼: %CD%\dist\TsukiNotes
echo ================================================
echo.
goto :end

:error
echo.
echo ���������жϣ�
echo ���������Ϣ������...
echo.
pause
exit /b 1

:end
echo ��������˳�...
pause > nul