@echo off 
title TsukiNotes Build Tools B1.0.0 -Preview version
echo TsukiNotes Build Tools b1.0.0[Preview]
echo Start Building.......
echo ========================================
pyinstaller --noconfirm --onedir --windowed --icon=".\tsuki\assets\GUI\resources\GUI\logo.png" --add-data "./tsuki/ui;tsuki/ui" --add-data "./tsuki/utils;tsuki/utils" --add-data "./tsuki/widgets;tsuki/widgets" --add-data "./tsuki/assets;tsuki/assets" TsukiNotes.py
echo ========================================
echo Done
pause