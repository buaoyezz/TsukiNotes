from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtCore import QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, Qt, QPoint
from assets.pages.home import HomePage
from assets.pages.about import AboutPage
from assets.pages.account_page import AccountPage
from assets.pages.main_functions import GitClonePage
from assets.pages.process_page import ProcessPage
from assets.pages.push_mainfunc import PushMainFuncPage
from assets.utils.style_loader import load_stylesheet


class PageManager:
    _instance = None
    animation_group = None
    @classmethod
    def get_instance(cls):
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = PageManager()
        return cls._instance
    
    def __init__(self):
        if PageManager._instance is not None:
            raise Exception("PageManager 是单例类，请使用 get_instance() 方法获取实例")
            
        super().__init__()
        self.stack = QStackedWidget()
        self.stack.setStyleSheet(load_stylesheet('content.qss'))
        
        # 记录当前页面索引
        self._current_index = 0
        
        # 侧边栏按钮配置
        self.sidebar_buttons = [
            ("首页", "home", "assets/icons/pages_icon/home.png"),
            ("账户", "account_page", "assets/icons/pages_icon/account.png"),
            ("拉取", "main_functions", "assets/icons/pages_icon/clone.png"),
            ("提交", "push_mainfunc", "assets/icons/pages_icon/push.png"),
            ("进度", "process_page", "assets/icons/pages_icon/process.png"),
            ("关于", "about", "assets/icons/pages_icon/about.png"),
        ]
        
        # 页面列表，保持顺序与侧边栏按钮一致
        self.page_list = [button[1] for button in self.sidebar_buttons]
        
        # 初始化页面，使用单例模式获取 ProcessPage
        self.pages = {
            "home": HomePage(),
            "account_page": AccountPage(),
            "main_functions": GitClonePage(),
            "push_mainfunc": PushMainFuncPage(),
            "process_page": ProcessPage.get_instance(),
            "about": AboutPage(),
        }
        
        # 将所有页面添加到堆栈，按照page_list的顺序
        for page_name in self.page_list:
            self.stack.addWidget(self.pages[page_name])
            
        PageManager._instance = self
    
    def slide_to_page(self, page_name):
        if self.animation_group and self.animation_group.state() == QPropertyAnimation.Running:
            self.animation_group.stop()
            self.animation_group.finished.emit()  # 确保之前的动画完全结束
            
        new_page = self.pages[page_name]
        current_page = self.stack.currentWidget()
        
        # 如果是同一个页面，不执行动画
        if new_page == current_page:
            return
            
        # 确定滑动方向
        new_index = self.page_list.index(page_name)
        current_index = self.page_list.index([k for k, v in self.pages.items() if v == current_page][0])
        direction = 1 if new_index > current_index else -1
        
        # 创建动画组
        self.animation_group = QParallelAnimationGroup()
        
        # 设置新页面的初始位置
        new_page.show()
        new_page.raise_()
        new_page.move(self.stack.width() * direction, 0)
        
        # 当前页面的动画
        current_anim = QPropertyAnimation(current_page, b"pos")
        current_anim.setDuration(250)  # 缩短动画时间
        current_anim.setEasingCurve(QEasingCurve.OutExpo)  # 使用更流畅的缓动曲线
        current_anim.setStartValue(QPoint(0, 0))
        current_anim.setEndValue(QPoint(-self.stack.width() * direction, 0))
        
        # 新页面的动画
        new_anim = QPropertyAnimation(new_page, b"pos")
        new_anim.setDuration(250)  # 缩短动画时间
        new_anim.setEasingCurve(QEasingCurve.OutExpo)  # 使用更流畅的缓动曲线
        new_anim.setStartValue(QPoint(self.stack.width() * direction, 0))
        new_anim.setEndValue(QPoint(0, 0))
        
        # 添加动画到组
        self.animation_group.addAnimation(current_anim)
        self.animation_group.addAnimation(new_anim)
        
        # 动画完成后更新堆栈
        def on_animation_finished():
            self.stack.setCurrentWidget(new_page)
            self._current_index = new_index
            # 重置所有页面位置
            for page in self.pages.values():
                if page != new_page:
                    page.move(0, 0)
        
        self.animation_group.finished.connect(on_animation_finished)
        self.animation_group.start()
    
    def get_stack(self):
        return self.stack
        
    def get_buttons(self):
        return self.sidebar_buttons
        
    def get_page(self, page_name):
        return self.pages[page_name]