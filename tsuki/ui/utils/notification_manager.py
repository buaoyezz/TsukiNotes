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
        self.NOTIFICATION_SPACING = 110 # 垂直间距
        self.BASE_Y = 60
        self.MAX_NOTIFICATIONS = 6
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
        if self.pending_shows and len(self.notifications) < self.MAX_NOTIFICATIONS:
            notification_data = self.pending_shows.pop(0)
            self._create_notification(**notification_data)
            self._rearrange_notifications()
        else:
            self.show_timer.stop()

    def _create_notification(self, title, msg, icon, duration):
        """创建新的通知"""
        try:
            # 清理已关闭和待删除的通知
            self.notifications = [n for n in self.notifications if n.isVisible() and n not in self.pending_removals]
            
            # 检查是否达到最大显示数量
            if len(self.notifications) >= self.MAX_NOTIFICATIONS:
                return
                
            notification = OverlayNotification()
            notification.closed.connect(lambda: self._remove_notification(notification))
            
            screen = QApplication.primaryScreen().geometry()
            target_x = screen.width() - notification.width() - 40
            target_y = self.BASE_Y + len(self.notifications) * self.NOTIFICATION_SPACING
            
            # 设置初始位置在屏幕右侧外
            notification.move(screen.width() + 50, target_y)
            notification.show()  # 先显示以获取正确的大小
            
            # 创建平滑的弹出动画
            anim = QPropertyAnimation(notification, b"pos", self)  # 将动画设为self的子对象
            anim.setDuration(500)
            anim.setStartValue(QPoint(screen.width() + 50, target_y))
            anim.setEndValue(QPoint(target_x, target_y))
            anim.setEasingCurve(QEasingCurve.OutCubic)  # 使用更平滑的缓动曲线
            
            self.animation_groups[notification] = anim
            self.notifications.append(notification)
            
            notification.show_message(title=title, message=msg, icon=icon, duration=duration)
            anim.start()
        except Exception as e:
            print(f"Error creating notification: {e}")

    def _remove_notification(self, notification):
        """移除通知"""
        try:
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
        except Exception as e:
            print(f"Error removing notification: {e}")

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
        # 清理不可见的通知，只保留可见且不在待删除列表中的通知
        visible_notifications = [n for n in self.notifications if n.isVisible() and n not in self.pending_removals]
        self.notifications = visible_notifications
        
        screen = QApplication.primaryScreen().geometry()
        animation_group = QParallelAnimationGroup(self)  # 将动画组设为self的子对象
        
        for i, notif in enumerate(visible_notifications):
            target_y = self.BASE_Y + i * self.NOTIFICATION_SPACING
            target_x = screen.width() - notif.width() - 40
            
            # 安全地停止和清理旧动画
            try:
                if notif in self.animation_groups:
                    old_anim = self.animation_groups.pop(notif)
                    if old_anim and not old_anim.parent():  # 检查动画对象是否有效
                        old_anim.stop()
                        old_anim.deleteLater()
            except RuntimeError:
                pass  # 忽略已删除对象的错误
            
            # 创建新动画
            anim = QPropertyAnimation(notif, b"pos", self)  # 将动画设为self的子对象
            anim.setDuration(300)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            anim.setEndValue(QPoint(target_x, target_y))
            
            self.animation_groups[notif] = anim
            animation_group.addAnimation(anim)
        
        # 启动动画组
        animation_group.start()

class NotificationWidget:
    def __init__(self, message, parent=None):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # 设置样式
        layout = QVBoxLayout()
        self.label = QLabel(message)
        self.label.setStyleSheet("""
            QLabel {
                color: black;
                background-color: rgba(255, 255, 255, 220);
                padding: 10px;
                border-radius: 5px;
                font-family: "Microsoft YaHei";
            }
        """)
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        # 设置大小
        self.adjustSize()
        
        # 3秒后自动关闭
        QTimer.singleShot(3000, self.close)

    def show(self):
        super().show()

    def close(self):
        super().close()

    def move(self, x, y):
        super().move(x, y)

    def isVisible(self):
        return super().isVisible()

    def width(self):
        return super().width()

    def height(self):
        return super().height()

    def y(self):
        return super().y()