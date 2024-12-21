@echo off
chcp 936 >nul
title TsukiNotes Build Tools B2 -Release
color 0E
echo ================================================
echo         TsukiNotes Build Tools B2
echo                Release Version
echo ================================================
echo.
echo [提示] 本脚本适配TsukiNotesVer1.6.3版本
echo [提示] 初始化完成，等待脚本执行.....
timeout /t 3 >nul

:: 检查主程序文件
echo [提示] Starting....
echo [检查] 正在检查项目文件...
if not exist "TsukiNotes.py" (
    color 0C
    echo [错误] 未找到 TsukiNotes.py！
    echo [提示] 请确保在正确的目录下运行此脚本
    echo [提示] 当前目录: %CD%
    goto :error
)
echo [成功] 找到主程序文件！
echo.

:: 检查项目结构
echo [检查] 正在检查项目结构...
if not exist "tsuki" (
    color 0C
    echo [错误] 未找到 tsuki 目录！
    echo [提示] 请确保完整的项目结构存在
    goto :error
)
if not exist "tsuki\assets" (
    color 0C
    echo [错误] 未找到 assets 目录！
    goto :error
)
echo [成功] 项目结构检查通过！
echo.

:: 检查 Python 环境
echo [检查] 正在检查 Python 环境...
python --version > nul 2>&1
if errorlevel 1 (
    color 0C
    echo [错误] 未检测到 Python 环境，请确保已安装 Python！
    goto :error
)
echo [成功] Python 环境检查通过！
echo.

:: 检查 PyInstaller
echo [检查] 正在检查 PyInstaller...
pyinstaller --version > nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装 PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        color 0C
        echo [错误] PyInstaller 安装失败！
        goto :error
    )
)
echo [成功] PyInstaller 准备就绪！
echo.

echo [信息] 开始构建 TsukiNotes...
echo [信息] 这可能需要几分钟时间，请耐心等待...
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
    echo [错误] 构建过程中出现错误！
    goto :error
)

echo.
echo ================================================
echo [成功] TsukiNotes 构建完成！
echo [信息] 输出目录: %CD%\dist\TsukiNotes
echo ================================================
echo.
goto :end

:error
echo.
echo 构建过程中断！
echo 请检查错误信息后重试...
echo.
pause
exit /b 1

:end
echo 按任意键退出...
pause > nul