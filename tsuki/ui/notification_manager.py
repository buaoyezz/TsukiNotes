from PyQt5.QtCore import QObject, QPoint, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QTimer
from PyQt5.QtWidgets import QDesktopWidget, QApplication
from .overlay_notification import OverlayNotification

class NotificationManager(QObject):
    _instance = None
    
    def __new__(cls):
        # 单例模式确保全局只有一个通知管理器
        if cls._instance is None:
            cls._instance = super(NotificationManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        super().__init__()
        self.notifications = []
        self.NOTIFICATION_SPACING = 80
        self.BASE_Y = 60
        self.MAX_NOTIFICATIONS = 3
        self.animation_groups = {}
        self.removing_notification = False
        self.pending_removals = set()
        self.pending_shows = []
        self.show_timer = QTimer()
        self.show_timer.timeout.connect(self._process_next_notification)
        self.SHOW_INTERVAL = 100
        self._initialized = True

    def show_message(self, title="", msg="", icon=None, duration=3000):
        """显示通知消息"""
        print(f"准备显示消息: {title} - {msg}")
        
        # 如果 icon 是字符串路径，转换为 QPixmap
        if isinstance(icon, str):
            from PyQt5.QtGui import QPixmap
            try:
                icon = QPixmap(icon)
            except:
                icon = None
        
        # 将新通知添加到待显示队列
        self.pending_shows.append({
            'title': title,
            'msg': msg,
            'icon': icon,
            'duration': duration
        })
        
        # 如果没有正在进行的移除操作，启动显示定时器
        if not self.removing_notification and not self.show_timer.isActive():
            self.show_timer.start(self.SHOW_INTERVAL)

    def _process_next_notification(self):
        """处理下一个待显示的通知"""
        # 先清理已关闭的通知
        self.notifications = [n for n in self.notifications if n.isVisible()]
        
        if self.pending_shows and len(self.notifications) < self.MAX_NOTIFICATIONS:
            notification_data = self.pending_shows.pop(0)
            self._create_notification(**notification_data)
            self._rearrange_notifications()
        else:
            self.show_timer.stop()

    def _create_notification(self, title, msg, icon, duration):
        """创建新的通知"""
        # 检查是否达到最大显示数量
        if len(self.notifications) >= self.MAX_NOTIFICATIONS:
            return
            
        notification = OverlayNotification()
        notification.closed.connect(lambda: self._remove_notification(notification))
        
        screen = QApplication.primaryScreen().geometry()
        target_x = screen.width() - notification.width() - 40
        target_y = self.BASE_Y + len(self.notifications) * self.NOTIFICATION_SPACING
        
        notification.move(screen.width() + 50, target_y)
        
        # 创建弹出动画
        anim = QPropertyAnimation(notification, b"pos")
        anim.setDuration(500)
        anim.setStartValue(QPoint(screen.width() + 50, target_y))
        anim.setEndValue(QPoint(target_x, target_y))
        anim.setEasingCurve(QEasingCurve.OutElastic)
        
        self.animation_groups[notification] = anim
        self.notifications.append(notification)
        
        notification.show()
        notification.show_message(title=title, message=msg, icon=icon, duration=duration)
        anim.start()

    def _remove_notification(self, notification):
        """移除通知"""
        if notification not in self.notifications or notification in self.pending_removals:
            return
            
        self.pending_removals.add(notification)
        self.removing_notification = True
        
        # 从列表中移除
        if notification in self.notifications:
            self.notifications.remove(notification)
        
        # 停止并清理相关动画
        if notification in self.animation_groups:
            anim = self.animation_groups.pop(notification)
            anim.stop()
            anim.deleteLater()
        
        # 强制关闭通知
        try:
            notification.timer.stop()
            notification.exit_animation_group.stop()
            notification.hide()
            # 不在这里调用 deleteLater，而是等待系统自动清理
        except RuntimeError:
            pass  # 对象可能已经被删除
        
        # 延迟处理其他操作
        QTimer.singleShot(300, self._handle_after_removal)

    def _handle_after_removal(self):
        """处理通知移除后的操作"""
        # 清理所有标记为删除的通知
        for notification in list(self.pending_removals):
            try:
                if notification in self.notifications:
                    self.notifications.remove(notification)
                if notification in self.animation_groups:
                    anim = self.animation_groups.pop(notification)
                    anim.stop()
                    anim.deleteLater()
            except RuntimeError:
                pass  # 对象可能已经被删除
            
        self.pending_removals.clear()
        self.removing_notification = False
        
        # 重新排列剩余通知
        self._rearrange_notifications()
        
        # 如果还有待显示的通知，重新启动显示定时器
        if self.pending_shows:
            self.show_timer.start(self.SHOW_INTERVAL)

    def _rearrange_notifications(self):
        """重新排列所有可见的通知"""
        # 清理不可见的通知
        self.notifications = [n for n in self.notifications if n.isVisible()]
        
        screen = QApplication.primaryScreen().geometry()
        
        for i, notif in enumerate(self.notifications):
            if notif.isVisible() and notif not in self.pending_removals:
                target_y = self.BASE_Y + i * self.NOTIFICATION_SPACING
                target_x = screen.width() - notif.width() - 40
                
                if notif in self.animation_groups:
                    old_anim = self.animation_groups.pop(notif)
                    old_anim.stop()
                    old_anim.deleteLater()
                
                QTimer.singleShot(i * 100, 
                    lambda n=notif, x=target_x, y=target_y: self._start_delayed_animation(n, x, y))

    def _start_delayed_animation(self, notification, target_x, target_y):
        """启动延迟动画"""
        if notification not in self.pending_removals and notification.isVisible():
            anim = QPropertyAnimation(notification, b"pos")
            anim.setDuration(300)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            anim.setEndValue(QPoint(target_x, target_y))
            
            self.animation_groups[notification] = anim
            anim.start()