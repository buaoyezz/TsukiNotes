import os
import logging
import subprocess
import sys
logger = logging.getLogger(__name__)

class CrashReport:
    @staticmethod
    def crash_report():
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 直接使用列表存储可能的文件名
            possible_files = ['CrashReport.exe', 'CrashReport.py']
            crash_report_path = None
            
            # 遍历查找存在的文件
            for file_name in possible_files:
                path = os.path.join(current_dir, '..', '..', file_name)
                if os.path.exists(path):
                    crash_report_path = path
                    break
                    
            if not crash_report_path:
                logger.error("未找到崩溃报告程序")
                return
                
            # 使用subprocess.Popen静默运行
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            # 根据文件类型选择启动方式
            if crash_report_path.endswith('.py'):
                process = subprocess.Popen([sys.executable, crash_report_path], startupinfo=startupinfo)
            else:
                process = subprocess.Popen([crash_report_path], startupinfo=startupinfo)
            
            # 不等待进程完成,让它在后台运行
            try:
                process.wait(timeout=0.1) # 仅等待很短时间确保进程启动
            except subprocess.TimeoutExpired:
                pass # 超时说明进程正在运行,这是预期行为
                
        except Exception as e:
            if "timed out" in str(e):
                # 超时说明进程仍在运行,实际上是成功的
                pass
            else:
                logger.error(f"启动崩溃报告程序失败: {str(e)}")