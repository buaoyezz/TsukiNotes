import os
import re
import datetime
import logging

logger = logging.getLogger(__name__)

class DeleteOldTemp():
    def delete_old_logs(directory, time_threshold_days=3):
        # 确保目录存在
        try:
            os.makedirs(directory, exist_ok=True)
        except Exception as e:
            logger.error(f"创建日志目录失败: {e}")
            return

        if not os.path.exists(directory):
            logger.error(f"目录不存在: {directory}")
            return

        now = datetime.datetime.now()
        logs_by_date = {}

        try:
            for filename in os.listdir(directory):
                if filename.endswith('.log'):
                    match = re.match(r'TsukiNotes_Log_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})\.log', filename)
                    if match:
                        date_str = match.group(1)
                        time_str = match.group(2)
                        timestamp_str = f"{date_str}_{time_str}"
                        try:
                            log_time = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d_%H-%M-%S')
                            time_difference = (now - log_time).days

                            if time_difference > time_threshold_days:
                                file_path = os.path.join(directory, filename)
                                try:
                                    os.remove(file_path)
                                    logger.info(f"删除过期日志文件: {file_path}")
                                except Exception as e:
                                    logger.error(f"删除文件失败 {file_path}: {e}")
                            else:
                                if date_str not in logs_by_date:
                                    logs_by_date[date_str] = []
                                logs_by_date[date_str].append((log_time, filename))
                        except ValueError as e:
                            logger.error(f"时间戳解析错误: {timestamp_str} - {e}")
        except Exception as e:
            logger.error(f"处理日志文件时发生错误: {e}")

    log_directory = os.path.join('tsuki', 'assets', 'log', 'temp')
    delete_old_logs(log_directory)