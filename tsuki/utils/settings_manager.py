import json
import os
from PyQt5.QtWidgets import QDesktopWidget

class SettingsManager:
    def __init__(self):
        self.settings_file = "settings.json"
        self.default_settings = {
            "window": {
                "width": 0,
                "height": 0,
                "x": 0,
                "y": 0,
                "is_maximized": False
            }
        }
        self.settings = self.load_settings()
        print("加载的设置:", self.settings)
        
    def load_settings(self):
        """加载设置"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    print("从文件加载的设置:", loaded_settings)
                    return loaded_settings
            except Exception as e:
                print(f"加载设置时出错: {e}")
                return self.default_settings.copy()
        print("使用默认设置")
        return self.default_settings.copy()
        
    def save_settings(self):
        """保存设置"""
        try:
            print("正在保存设置:", self.settings)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
            print("设置保存成功")
        except Exception as e:
            print(f"保存设置时出错: {e}")
            
    def get_recommended_size(self):
        """获取推荐的窗口尺寸（适用于1920x1080屏幕）"""
        screen = QDesktopWidget().availableGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        
        # 默认窗口尺寸为1069x577
        width = 1069
        height = 577
        
        # 确保窗口尺寸在合理范围内
        width = max(1050, min(width, screen_width - 100))   # 最小1050px
        height = max(450, min(height, screen_height - 100)) # 最小450px
        
        # 计算居中位置
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        return {
            "width": width,
            "height": height,
            "x": x,
            "y": y
        } 