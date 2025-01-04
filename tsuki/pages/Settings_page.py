from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget, 
                           QStackedWidget, QPushButton, QLabel, QGridLayout, QWidget, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QParallelAnimationGroup,QRect,QTimer
from PyQt5.QtGui import QIcon, QColor
import os
import logging
from tsuki.ui.utils.message_box import ClutMessageBox
from tsuki.ui.utils.clut_card import ClutCard
from tsuki.ui.utils.clut_image_card import ClutImageCard
from tsuki.ui.utils.overlay_notification import OverlayNotification
from tsuki.pages.About_page import AboutPage
from PyQt5.QtWidgets import *
import configparser
import os
import time
import requests
import tempfile
import json
logger = logging.getLogger(__name__)

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        
        # 修改窗口属性
        self.setAttribute(Qt.WA_TranslucentBackground, False)  # 禁用透明背景
        self.setFocusPolicy(Qt.NoFocus) # 取消焦点

        self.setWindowFlags(
            Qt.Dialog | 
            Qt.FramelessWindowHint | 
            Qt.WindowCloseButtonHint | 
            Qt.MSWindowsFixedSizeDialogHint
        )
        
        # 添加拖动相关变量
        self.dragging = False
        self.drag_position = None
        
        # 其他初始化代码保持不变
        self.button_animations = {}
        self.page_animation = None
        self.setWindowTitle('Tsuki全局设置[Settings]')
        self.setWindowIcon(QIcon('./tsuki/assets/resources/settings.png'))
        self.setGeometry(100, 100, 800, 400)
        logger.info('Open Setting')
        
        # 设置布局
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)  # 添加边距
        
        sidebar = QListWidget(self)
        sidebar.setFixedWidth(150)
        sidebar.addItem("界面设置")
        sidebar.addItem("字体设置")
        sidebar.addItem("调试设置")
        sidebar.addItem("关于设置")
        sidebar.addItem("退出Exit")
        sidebar.currentRowChanged.connect(self.display)
        sidebar.itemClicked.connect(self.check_exit)
        sidebar.setFocusPolicy(Qt.NoFocus) # 取消焦点

        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.interfacePage())
        self.stack.addWidget(self.fontPage())
        self.stack.addWidget(self.debugPage())
        # 传入版本信息
        self.stack.addWidget(AboutPage(
            current_version=parent.current_version,
            version_td=parent.version_td,
            version_gj=parent.version_gj,
            update_Date=parent.update_Date
        ))

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)

        # 应用样式
        self.applyStyle()
        
    # 添加鼠标事件处理
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()

    def interfacePage(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(10, 10, 10, 10)

        # 标题
        title_label = QLabel("| 界面设置", self)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px; 
                font-weight: bold;
                color: #333333;
            }
        """)
        layout.addWidget(title_label, alignment=Qt.AlignLeft | Qt.AlignTop)
        
        # 按钮网格布局
        button_layout = QGridLayout()
        button_layout.setSpacing(15)
        self._add_interface_buttons(button_layout)
        layout.addLayout(button_layout)
        
        # 添加弹性空间
        layout.addStretch()
        
        return page

    def _add_interface_buttons(self, layout):
        """添加界面设置按钮"""
        buttons = [
            ("设置背景颜色", self.parent().set_background, 0, 0),
            ("重置文本框背景图片", self.parent().reset_background_color, 0, 1),
            ("设置背景图", self.parent().setBackgroundImage, 1, 0),
            ("重置背景图", self.parent().reset_background, 1, 1),
            ("高亮显示设置", self.parent().total_setting, 2, 0),
            ("彩色设置背景", self.parent().color_bg, 2, 1),
            ("API背景", self.openApiDialog, 3, 0),
            ("主题设置", self.openThemeDialog, 3, 1)
        ]
        
        for button in buttons:
            name, callback, row, col = button
            layout.addWidget(self.createButton(name, callback), row, col)
    def openApiDialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("API背景")
        dialog.setWindowIcon(QIcon('./tsuki/assets/resources/settings.png'))
        # 设置更大的窗口尺寸
        dialog.setFixedSize(700, 600)  # 增加高度
        
        self._setup_api_dialog_ui(dialog)
        dialog.exec_()

    def _setup_api_dialog_ui(self, dialog):
        # 主布局
        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)
        # 增加边距给更多空间
        layout.setContentsMargins(30, 30, 30, 30)

        # 添加状态标签
        self.status_label = QLabel()
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-family: Microsoft YaHei;
                padding: 5px;
            }
        """)

        # API设置卡片
        api_card = ClutCard("API设置", "")
        api_content = QVBoxLayout()
        # 增加内容间距
        api_content.setSpacing(20)
        
        # API输入框组
        api_input_group = QVBoxLayout()
        api_input_group.setSpacing(12)  # 增加控件间距
        
        # API输入框
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("输入API地址")
        self.api_input.setMinimumHeight(40)  # 增加输入框高度
        
        # JSON路径输入框
        self.json_input = QLineEdit()
        self.json_input.setPlaceholderText("输入JSON路径 (如: data.url)")
        self.json_input.setMinimumHeight(40)
        
        # 预设API下拉框
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(["[预设]自定义", "[预设]樱花Random", "[预设]夏沫Random", "[预设]必应Bing每日UHD", "[预设]Bing Random"])
        self.preset_combo.setMinimumHeight(40)
        
        api_input_group.addWidget(self.api_input)
        api_input_group.addWidget(self.json_input)
        api_input_group.addWidget(self.preset_combo)
        
        api_content.addLayout(api_input_group)
        api_card.setContentLayout(api_content)
        layout.addWidget(api_card)

        # 自动化设置卡片
        auto_card = ClutCard("自动化设置[Auto|不可改变]", "")
        auto_content = QVBoxLayout()
        auto_content.setSpacing(20)
        
        # 自动更新设置
        update_group = QHBoxLayout()
        update_group.setSpacing(12)
        self.auto_update_check = QCheckBox("启用自动更新")
        self.update_interval = QSpinBox()
        self.update_interval.setRange(1, 24*60*60)
        self.update_interval.setValue(3600)
        self.update_interval.setSuffix(" 秒")
        self.update_interval.setMinimumHeight(40)
        self.update_interval.setEnabled(False)
        update_group.addWidget(self.auto_update_check)
        update_group.addWidget(self.update_interval)
        auto_content.addLayout(update_group)
        
        # 自动清理设置
        clean_group = QHBoxLayout()
        clean_group.setSpacing(12)
        self.auto_clean_check = QCheckBox("启用自动清理")
        self.clean_interval = QSpinBox()
        self.clean_interval.setRange(1, 7*24*60*60)
        self.clean_interval.setValue(86400)
        self.clean_interval.setSuffix(" 秒")
        self.clean_interval.setMinimumHeight(40)
        self.clean_interval.setEnabled(False)
        clean_group.addWidget(self.auto_clean_check)
        clean_group.addWidget(self.clean_interval)
        auto_content.addLayout(clean_group)
        
        # 清除缓存按钮
        clear_cache_btn = QPushButton("清除缓存")
        clear_cache_btn.setMinimumHeight(35)
        clear_cache_btn.setStyleSheet("""
            QPushButton {
                *outline: none;
                background-color: rgba(139, 92, 246, 0.15);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: rgba(139, 92, 246, 0.25);
            }
            QPushButton:pressed {
                background-color: rgba(139, 92, 246, 0.35);
            }
        """)
        clear_cache_btn.clicked.connect(self._clear_api_cache)
        auto_content.addWidget(clear_cache_btn)
        
        auto_card.setContentLayout(auto_content)
        layout.addWidget(auto_card)

        # 底部按钮组
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        download_btn = QPushButton("下载并设置")
        cancel_btn = QPushButton("取消")
        download_btn.setMinimumHeight(35)
        cancel_btn.setMinimumHeight(35)
        download_btn.setStyleSheet(clear_cache_btn.styleSheet())
        cancel_btn.setStyleSheet(clear_cache_btn.styleSheet())
        button_layout.addWidget(download_btn)
        button_layout.addWidget(cancel_btn)
        
        # 添加状态标签和按钮到布局
        layout.addWidget(self.status_label)
        layout.addLayout(button_layout)

        # 连接信号
        download_btn.clicked.connect(lambda: self._download_image(dialog, self.api_input, self.json_input, download_btn, self.status_label))
        cancel_btn.clicked.connect(dialog.reject)
        self.preset_combo.currentTextChanged.connect(self._on_preset_changed)

        # 设置窗口样式
        dialog.setStyleSheet("""
            QDialog {
                background-color: #e0e5ec;
                border-radius: 15px;
            }
            
            QLineEdit {
                background-color: #e0e5ec;
                border: none;
                border-radius: 8px;
                padding: 10px;
                color: #2d3436;
            }
            
            QComboBox {
                background-color: #e0e5ec;
                border: none;
                border-radius: 8px;
                padding: 10px;
                color: #2d3436;
            }
            
            QCheckBox {
                color: #2d3436;
                spacing: 8px;
            }
            
            QSpinBox {
                background-color: #e0e5ec;
                border: none;
                border-radius: 8px;
                padding: 5px;
                color: #2d3436;
            }
        """)
        
        # Add shadow effects to widgets
        for widget in dialog.findChildren((QLineEdit, QComboBox, QSpinBox)):
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(10)
            shadow.setXOffset(0)
            shadow.setYOffset(0)
            shadow.setColor(QColor(163, 177, 198, 160))
            widget.setGraphicsEffect(shadow)

    def _clear_api_cache(self):
        """手动清理缓存"""
        try:
            cache_dir = './tsuki/assets/app/api_temp'
            if os.path.exists(cache_dir):
                for file in os.listdir(cache_dir):
                    file_path = os.path.join(cache_dir, file)
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        logger.error(f"删除缓存文件失败 {file_path}: {str(e)}")
                ClutMessageBox.show_message(self, "成功", "缓存已清除")
                logger.info("API图片缓存已手动清除")
            else:
                ClutMessageBox.show_message(self, "提示", "缓存目录不存在")
        except Exception as e:
            ClutMessageBox.show_message(self, "错误", f"清除缓存失败: {str(e)}")
            logger.error(f"清除缓存失败: {str(e)}")

    def _load_and_apply_settings(self):
        """加载并应用设置"""
        try:
            config = configparser.ConfigParser()
            config.read('./tsuki/assets/app/cfg/background_api_get.ini')
            
            if 'API' in config:
                # 加载设置
                self.api_input.setText(config['API'].get('url', ''))
                self.json_input.setText(config['API'].get('json_path', ''))
                self.auto_update_check.setChecked(config['API'].getboolean('auto_update', False))
                self.update_interval.setValue(config['API'].getint('update_interval', 3600))
                self.auto_clean_check.setChecked(config['API'].getboolean('auto_clean', False))
                self.clean_interval.setValue(config['API'].getint('clean_interval', 86400))
                
                # 设置最后使用的图片
                last_image = config['API'].get('last_image', '')
                if last_image and os.path.exists(last_image):
                    self.parent().setBackgroundImageFromFile(last_image)
                
                # 启动定时器
                self._setup_timers()
                
                # 如果启用了自动更新，立即更新一次
                if self.auto_update_check.isChecked():
                    self._auto_update_background()
                    
        except Exception as e:
            logger.error(f"加载API设置失败: {str(e)}")

    def _setup_timers(self):
        """设置定时器"""
        # 自动更新定时器
        if self.auto_update_check.isChecked():
            interval = self.update_interval.value() * 1000  # 转换为毫秒
            self.update_timer.start(interval)
        else:
            self.update_timer.stop()
            
        # 自动清理定时器
        if self.auto_clean_check.isChecked():
            interval = self.clean_interval.value() * 1000  # 转换为毫秒
            self.clean_timer.start(interval)
        else:
            self.clean_timer.stop()

    def _auto_update_background(self):
        """自动更新背景"""
        try:
            api_url = self.api_input.text().strip()
            json_path = self.json_input.text().strip()
            if api_url:
                self._download_image(api_url, json_path)
        except Exception as e:
            logger.error(f"自动更新背景失败: {str(e)}")

    def _auto_clean_cache(self):
        """自动清理缓存"""
        try:
            cache_dir = './tsuki/assets/app/api_temp'
            if os.path.exists(cache_dir):
                current_time = time.time()
                for file in os.listdir(cache_dir):
                    file_path = os.path.join(cache_dir, file)
                    # 保留最后使用的图片
                    if file_path != self._get_last_image_path():
                        try:
                            file_time = os.path.getmtime(file_path)
                            if (current_time - file_time) > self.clean_interval.value():
                                os.remove(file_path)
                        except Exception as e:
                            logger.error(f"删除缓存文件失败 {file_path}: {str(e)}")
                logger.info("API图片缓存已自动清理")
        except Exception as e:
            logger.error(f"自动清理缓存失败: {str(e)}")

    def _get_last_image_path(self):
        """获取最后使用的图片路径"""
        try:
            config = configparser.ConfigParser()
            config.read('./tsuki/assets/app/cfg/background_api_get.ini')
            return config['API'].get('last_image', '')
        except:
            return ''

    def _create_api_input_group(self):
        api_group = QGroupBox("API设置")
        api_layout = QVBoxLayout()
        api_layout.setSpacing(15)
        
        api_input = QLineEdit()
        api_input.setPlaceholderText("输入API URL (必填)")
        api_input.setMinimumHeight(35)
        
        json_input = QLineEdit()
        json_input.setPlaceholderText("输入JSON路径 (选填，如: data.url)")
        json_input.setMinimumHeight(35)
        
        api_layout.addWidget(api_input)
        api_layout.addWidget(json_input)
        api_group.setLayout(api_layout)
        
        return api_group, api_input, json_input

    def _create_preset_group(self):
        preset_group = QGroupBox("预设API")
        preset_layout = QHBoxLayout()
        
        preset_combo = QComboBox()
        preset_combo.setMinimumHeight(35)
        preset_combo.addItems([
            "自定义",
            "樱花Random",
            "夏沫Random", 
            "必应Bing每日UHD",
            "Bing Random"
        ])
        
        # 连接信号槽
        preset_combo.currentIndexChanged.connect(self._on_preset_changed)
        
        preset_layout.addWidget(preset_combo)
        preset_group.setLayout(preset_layout)
        return preset_group, preset_combo

    def _create_dialog_buttons(self):
        """创建对话框按钮"""
        download_btn = QPushButton("下载并设置")
        download_btn.setMinimumHeight(35)
        download_btn.setMinimumWidth(120)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.setMinimumHeight(35)
        cancel_btn.setMinimumWidth(120)
        
        return download_btn, cancel_btn

    def _create_status_label(self):
        """创建状态标签"""
        status_label = QLabel()
        status_label.setStyleSheet("color: #666666; font-family: Microsoft YaHei;")
        return status_label

    def _setup_api_dialog_events(self, dialog, preset_combo, api_input, json_input,
                               download_btn, cancel_btn, status_label):
        """设置API对话框事件"""
        # 预设API选择事件
        preset_combo.currentIndexChanged.connect(
            lambda index: self._on_preset_changed(index, api_input, json_input)
        )
        
        # 下载按钮事件
        download_btn.clicked.connect(
            lambda: self._download_image(dialog, api_input, json_input, download_btn, status_label)
        )
        
        # 取消按钮事件
        cancel_btn.clicked.connect(dialog.reject)

    def _on_preset_changed(self, index):
        """处理预设API选择变更"""
        presets = {
            "[预设]樱花Random": {
                "url": "https://www.dmoe.cc/random.php?return=json",
                "path": "imgurl"
            },
            "[预设]夏沫Random": {
                "url": "https://cdn.seovx.com/d/?mom=302", 
                "path": ""
            },
            "[预设]必应Bing每日UHD": {
                "url": "https://bing.img.run/uhd.php",
                "path": ""
            },
            "[预设]Bing Random": {
                "url": "https://bing.img.run/rand.php",
                "path": ""
            }
        }
        
        selected = self.preset_combo.currentText()
        if selected in presets:
            preset = presets[selected]
            self.api_input.setText(preset["url"])
            self.json_input.setText(preset["path"])

    def _download_image(self, dialog, api_input, json_input, download_btn, status_label):
        """下载并设置背景图片"""
        api_url = api_input.text().strip()
        json_path = json_input.text().strip()
        
        if not api_url:
            status_label.setText("请输入API地址")
            return
            
        status_label.setText("正在下载...")
        download_btn.setEnabled(False)
        
        try:
            # 创建api_temp目录
            temp_dir = './tsuki/assets/app/api_temp'
            os.makedirs(temp_dir, exist_ok=True)
            
            # 获取图片
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(api_url, timeout=10, verify=False)
            response.raise_for_status()
            
            if json_path:
                data = response.json()
                image_url = data
                for key in json_path.split('.'):
                    image_url = image_url[key]
                if not image_url.startswith('http'):
                    image_url = 'https://www.bing.com' + image_url
            else:
                image_url = api_url if 'image' in response.headers.get('Content-Type', '') else response.url
            
            # 下载图片
            img_response = requests.get(image_url, timeout=10, verify=False)
            img_response.raise_for_status()
            
            # 获取原始格式并保存
            content_type = img_response.headers.get('Content-Type', '')
            ext = content_type.split('/')[-1] if '/' in content_type else 'jpg'
            save_path = os.path.join(temp_dir, f'api_image_{int(time.time())}.{ext}')
            
            with open(save_path, 'wb') as f:
                f.write(img_response.content)
            
            # 尝试设置背景
            try:
                self.parent().setBackgroundImageFromFile(save_path)
                self.parent().text_edit.setStyleSheet(f"background-image: url({save_path});")
            except Exception:
                # 转换格式重试
                from PIL import Image
                img = Image.open(save_path)
                converted_path = os.path.join(temp_dir, f'api_image_{int(time.time())}.png')
                img.save(converted_path, 'PNG')
                self.parent().setBackgroundImageFromFile(converted_path)
                self.parent().text_edit.setStyleSheet(f"background-image: url({converted_path});")
                save_path = converted_path
            
            # 保存配置
            config = configparser.ConfigParser()
            config['API'] = {
                'url': api_url,
                'json_path': json_path,
                'last_image': save_path,
                'auto_update': 'false',
                'update_interval': '3600',
                'auto_clean': 'false', 
                'clean_interval': '86400'
            }
            
            config_dir = './tsuki/assets/app/cfg'
            os.makedirs(config_dir, exist_ok=True)
            with open(os.path.join(config_dir, 'background_api_get.ini'), 'w') as f:
                config.write(f)
            
            dialog.accept()
            ClutMessageBox.show_message(dialog, "成功", 
                                  f"图片已下载并设置为背景\n保存路径: {save_path}")
            logger.info(f"API image downloaded and set as background: {save_path}")
            
        except Exception as e:
            status_label.setText(f"下载失败: {str(e)}")
            logger.error(f"[Log/ERROR]API image download failed: {str(e)}")
        finally:
            download_btn.setEnabled(True)

    def openThemeDialog(self):
        """打开主题设置对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("主题设置")
        dialog.setWindowIcon(QIcon('./tsuki/assets/resources/settings.png'))
        dialog.setFixedSize(400, 300)
        
        # 主布局
        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 主题选择下拉框
        theme_label = QLabel("选择主题:")
        self.theme_combo = QComboBox()
        self.theme_combo.setMinimumHeight(30)
        self.theme_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        self.load_available_themes()
        
        # 主题信息显示区域
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                color: #333;
            }
        """)
        
        # 更新主题信息显示
        def update_theme_info():
            try:
                current_theme = self.theme_combo.currentText()
                theme_path = f'./tsuki/theme/{current_theme}/theme.json'
                
                if os.path.exists(theme_path):
                    with open(theme_path, 'r', encoding='utf-8') as f:
                        theme_data = json.load(f)
                        info = f"""主题名称: {theme_data.get('name', '默认主题')}
版本: {theme_data.get('version', '1.0')}
作者: {theme_data.get('author', 'TsukiNotes')}
描述: {theme_data.get('description', '无描述')}"""
                        info_text.setText(info)
                else:
                    info_text.setText("无法加载主题信息")
            except Exception as e:
                info_text.setText(f"加载主题信息失败: {str(e)}")
        
        self.theme_combo.currentTextChanged.connect(update_theme_info)
        update_theme_info()
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # 预览和应用按钮
        preview_btn = QPushButton("预览主题")
        apply_btn = QPushButton("应用主题")
        close_btn = QPushButton("关闭")
        
        for btn in [preview_btn, apply_btn, close_btn]:
            btn.setMinimumHeight(30)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a90e2;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 5px 20px;
                }
                QPushButton:hover {
                    background-color: #357abd;
                }
            """)
        
        preview_btn.clicked.connect(lambda: self.preview_theme(self.theme_combo.currentText()))
        apply_btn.clicked.connect(self.apply_selected_theme)
        close_btn.clicked.connect(dialog.close)
        
        button_layout.addWidget(preview_btn)
        button_layout.addWidget(apply_btn)
        button_layout.addWidget(close_btn)
        
        # 添加所有组件到主布局
        layout.addWidget(theme_label)
        layout.addWidget(self.theme_combo)
        layout.addWidget(info_text)
        layout.addLayout(button_layout)
        
        # 设置对话框样式
        dialog.setStyleSheet("""
            QDialog {
                background-color: #666666;
                border-radius: 10px;
            }
            QLabel {
                color: white;
            }
        """)
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 80))
        dialog.setGraphicsEffect(shadow)
        
        dialog.exec_()

    def fontPage(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title_label = QLabel("| 字体设置", self)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px; 
                font-weight: bold;
                color: #333333;
                font-family: "Microsoft YaHei";
            }
        """)
        layout.addWidget(title_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        button_layout = QGridLayout()
        button_layout.setSpacing(15)

        button_layout.addWidget(self.createButton("设置字体大小", self.parent().set_font_size), 0, 0)
        button_layout.addWidget(self.createButton("初始化字体大小", self.parent().initialize_font_size), 0, 1)

        layout.addLayout(button_layout)
        return page

    def debugPage(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title_label = QLabel("| 调试设置", self)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px; 
                font-weight: bold;
                color: #333333;
            }
        """)
        layout.addWidget(title_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        button_layout = QGridLayout()
        button_layout.setSpacing(15)

        button_layout.addWidget(self.createButton("调试模式", self.parent().toggle_debug_mode), 0, 0)
        button_layout.addWidget(self.createButton("加入TsukiNotes预览计划", self.parent().beta_version), 0, 1)
        button_layout.addWidget(self.createButton("快速Crash按钮[测试用警告]",self.parent().crash_app),0, 2)

        layout.addLayout(button_layout)
        return page

    def createButton(self, text, slot):
        """创建按钮"""
        button = QPushButton(text)
        button.clicked.connect(slot)
        button.setMinimumHeight(40)
        
        # 创建按钮容器
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(5, 5, 5, 5)
        container_layout.addWidget(button)
        
        # 按钮阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(163, 177, 198, 160))
        button.setGraphicsEffect(shadow)
        
        # 按钮样式
        button.setStyleSheet("""
            QPushButton {
                background-color: #e0e5ec;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                color: #2d3436;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #eef0f5;
            }
            
            QPushButton:pressed {
                background-color: #d1d9e6;
            }
        """)
        
        # 创建动画组
        anim_group = QParallelAnimationGroup()
        
        # 阴影动画
        shadow_anim = QPropertyAnimation(shadow, b"blurRadius")
        shadow_anim.setDuration(100)
        
        # 缩放动画
        scale_anim = QPropertyAnimation(button, b"geometry")
        scale_anim.setDuration(100)
        scale_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        # 按钮按下效果
        def on_press():
            shadow_anim.setStartValue(15)
            shadow_anim.setEndValue(5)
            
            curr_geo = button.geometry()
            scale_anim.setStartValue(curr_geo)
            scale_anim.setEndValue(QRect(
                int(curr_geo.x() + 2),
                int(curr_geo.y() + 2),
                int(curr_geo.width() * 0.95),
                int(curr_geo.height() * 0.95)
            ))
            
            anim_group.start()
        
        # 按钮释放效果
        def on_release():
            shadow_anim.setStartValue(5)
            shadow_anim.setEndValue(15)
            
            curr_geo = button.geometry()
            scale_anim.setStartValue(curr_geo)
            scale_anim.setEndValue(QRect(
                int(curr_geo.x() - 2),
                int(curr_geo.y() - 2),
                int(curr_geo.width() / 0.95),
                int(curr_geo.height() / 0.95)
            ))
            
            anim_group.start()
        
        anim_group.addAnimation(shadow_anim)
        anim_group.addAnimation(scale_anim)
        
        button.pressed.connect(on_press)
        button.released.connect(on_release)
        
        return container

    def display(self, index):
        """优化页面切换动画为果冻效果"""
        if self.page_animation and self.page_animation.state() == QPropertyAnimation.Running:
            self.page_animation.stop()
            
        anim_group = QParallelAnimationGroup()
        
        # 当前页面动画
        old_widget = self.stack.currentWidget()
        if old_widget:
            old_scale = QPropertyAnimation(old_widget, b"geometry")
            old_scale.setDuration(400)  # 增加动画时长
            old_scale.setStartValue(old_widget.geometry())
            
            old_geo = old_widget.geometry()
            new_rect = QRect(
                int(old_geo.x() - 30),  # 增加位移距离
                old_geo.y(),
                int(old_geo.width() * 0.9),  # 增加缩放比例
                old_geo.height()
            )
            old_scale.setEndValue(new_rect)
            old_scale.setEasingCurve(QEasingCurve.OutElastic)  # 使用弹性曲线
            
            fade_out = QPropertyAnimation(old_widget, b"windowOpacity")
            fade_out.setStartValue(1.0)
            fade_out.setEndValue(0.0)
            fade_out.setDuration(300)
            fade_out.setEasingCurve(QEasingCurve.OutCubic)
            
            anim_group.addAnimation(old_scale)
            anim_group.addAnimation(fade_out)
                
        # 新页面动画
        self.stack.setCurrentIndex(index)
        new_widget = self.stack.currentWidget()
        new_widget.setWindowOpacity(0.0)
        
        curr_geo = new_widget.geometry()
        init_rect = QRect(
            int(curr_geo.x() + 30),  # 增加初始位移
            curr_geo.y(),
            int(curr_geo.width() * 0.9),
            curr_geo.height()
        )
        new_widget.setGeometry(init_rect)
        
        new_scale = QPropertyAnimation(new_widget, b"geometry")
        new_scale.setDuration(500)  # 增加动画时长
        new_scale.setStartValue(new_widget.geometry())
        final_rect = QRect(
            curr_geo.x(),
            curr_geo.y(),
            curr_geo.width(),
            curr_geo.height()
        )
        new_scale.setEndValue(final_rect)
        new_scale.setEasingCurve(QEasingCurve.OutBounce)  # 使用弹跳曲线
        
        fade_in = QPropertyAnimation(new_widget, b"windowOpacity")
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setDuration(300)
        fade_in.setEasingCurve(QEasingCurve.InOutQuad)
        
        anim_group.addAnimation(new_scale)
        anim_group.addAnimation(fade_in)
        
        self.page_animation = anim_group
        anim_group.start()

    def closeEvent(self, event):
        """添加窗口关闭动画"""
        if hasattr(self, 'close_animation'):
            event.ignore()
            return
            
        self.close_animation = QParallelAnimationGroup()
        
        # 缩放动画
        scale_anim = QPropertyAnimation(self, b"geometry")
        scale_anim.setDuration(150)
        scale_anim.setStartValue(self.geometry())
        scale_anim.setEndValue(QRect(
            self.geometry().center().x(),
            self.geometry().center().y(),
            0, 0
        ))
        scale_anim.setEasingCurve(QEasingCurve.InQuad)
        
        # 透明度动画
        fade_anim = QPropertyAnimation(self, b"windowOpacity")
        fade_anim.setDuration(150)
        fade_anim.setStartValue(1.0)
        fade_anim.setEndValue(0.0)
        fade_anim.setEasingCurve(QEasingCurve.InQuad)
        
        self.close_animation.addAnimation(scale_anim)
        self.close_animation.addAnimation(fade_anim)
        
        # 动画结束时真正关闭窗口
        self.close_animation.finished.connect(lambda: super(SettingsWindow, self).closeEvent(event))
        self.close_animation.start()

    def load_available_themes(self):
        """加载可用主题列表"""
        try:
            self.theme_combo.clear()
            theme_dir = './tsuki/theme'
            
            if not os.path.exists(theme_dir):
                os.makedirs(theme_dir, exist_ok=True)
                logger.info(f"Created theme directory: {theme_dir}")
            
            themes = []
            if os.path.exists(theme_dir):
                themes = [d for d in os.listdir(theme_dir) 
                         if os.path.isdir(os.path.join(theme_dir, d)) and 
                         os.path.exists(os.path.join(theme_dir, d, 'theme.json'))]
            
            if not themes:
                logger.warning("No themes found, creating default theme")
                self._create_default_theme()
                themes = ['default']
            
            self.theme_combo.addItems(themes)
            
            # 设置当前主题
            try:
                config = configparser.ConfigParser()
                config_path = './tsuki/assets/app/config/theme/theme.ini'
                if os.path.exists(config_path):
                    config.read(config_path, encoding='utf-8')
                    current_theme = config.get('Theme', 'current_theme', fallback='default')
                    index = self.theme_combo.findText(current_theme)
                    if index >= 0:
                        self.theme_combo.setCurrentIndex(index)
            except Exception as e:
                logger.error(f"加载当前主题设置失败: {e}")
                self.theme_combo.setCurrentText('default')
            
        except Exception as e:
            logger.error(f"加载主题列表失败: {e}")
            self.theme_combo.addItem('default')

    def _create_default_theme(self):
        """创建默认主题"""
        default_theme_dir = './tsuki/theme/default'
        os.makedirs(default_theme_dir, exist_ok=True)
        
        default_theme = {
            "name": "默认主题",
            "version": "1.0",
            "author": "TsukiNotes",
            "window_style": "QMainWindow { background-color: #FFFFFF; }",
            "editor_style": "QTextEdit { background-color: #FFFFFF; color: #000000; }",
            "menu_style": "QMenuBar { background-color: #F0F0F0; }",
            "status_style": "QStatusBar { background-color: #F0F0F0; }"
        }
        
        with open(os.path.join(default_theme_dir, 'theme.json'), 'w', encoding='utf-8') as f:
            json.dump(default_theme, f, ensure_ascii=False, indent=4)

    def apply_selected_theme(self):
        """应用选中的主题"""
        try:
            theme = self.theme_combo.currentText()
            
            # 临时禁用窗口特效
            main_window = self.parent()
            was_translucent = main_window.testAttribute(Qt.WA_TranslucentBackground)
            if was_translucent:
                main_window.setAttribute(Qt.WA_TranslucentBackground, False)
            
            # 第一次应用
            main_window.apply_theme(theme)
            
            # 使用 QTimer 延迟一小段时间后重新应用主题
            QTimer.singleShot(100, lambda: self._reapply_theme(theme, was_translucent))
            
            logger.info(f"Theme applied: {theme}")
            
        except Exception as e:
            logger.error(f"应用主题失败: {e}")
            error_notification = OverlayNotification(parent=self)
            error_notification.show_message(
                title="错误",
                message=f"应用主题失败: {str(e)}",
                duration=5000
            )

    def _reapply_theme(self, theme, was_translucent):
        """重新应用主题"""
        try:
            main_window = self.parent()
            
            # 第二次应用
            main_window.apply_theme(theme)
            
            # 恢复窗口特效
            if was_translucent:
                QTimer.singleShot(50, lambda: main_window.setAttribute(Qt.WA_TranslucentBackground, True))
            
            # 显示成功通知
            notification = OverlayNotification(parent=self)
            notification.show_message(
                title="主题设置",
                message=f"主题 {theme} 已应用喵~",
                duration=3000
            )
            
        except Exception as e:
            logger.error(f"重新应用主题失败: {e}")

    def applyStyle(self):
        # 为主窗口添加拟态效果
        main_shadow = QGraphicsDropShadowEffect()
        main_shadow.setBlurRadius(20)
        main_shadow.setXOffset(0)
        main_shadow.setYOffset(0)
        main_shadow.setColor(QColor(163, 177, 198, 100))
        self.setGraphicsEffect(main_shadow)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #e0e5ec;
                border-radius: 4px;
            }
            
            QListWidget {
                background-color: #e0e5ec;
                border-radius: 10px;
                border: none;
                padding: 10px;
            }
            
            QListWidget::item {
                background-color: #e0e5ec;
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
                color: #2d3436;
            }
            
            QListWidget::item:selected {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffffff,
                    stop:1 #e0e5ec
                );
                color: #2d3436;
            }
            
            QLabel {
                color: #2d3436;
                font-weight: bold;
            }
            
            QStackedWidget {
                background: transparent;
            }
        """)
        
        # 为侧边栏添加内阴影效果
        sidebar_shadow = QGraphicsDropShadowEffect()
        sidebar_shadow.setBlurRadius(15)
        sidebar_shadow.setXOffset(3)
        sidebar_shadow.setYOffset(3)
        sidebar_shadow.setColor(QColor(163, 177, 198, 120))
        self.findChild(QListWidget).setGraphicsEffect(sidebar_shadow)

    def check_exit(self, item):
        if item.text() == "退出Exit":
            self.close()

    def show_theme_info(self):
        """显示主题信息对话框"""
        try:
            current_theme = self.theme_combo.currentText()
            theme_path = f'./tsuki/theme/{current_theme}/theme.json'
            
            if not os.path.exists(theme_path):
                raise FileNotFoundError(f"主题配置文件不存在: {theme_path}")
            
            with open(theme_path, 'r', encoding='utf-8') as f:
                theme_data = json.load(f)
            
            # 创建主题信息对话框
            dialog = QDialog(self)
            dialog.setWindowTitle("主题信息")
            dialog.setFixedSize(400, 500)
            dialog.setStyleSheet("""
                QDialog {
                    background-color: #e0e5ec;
                    border-radius: 15px;
                }
            """)
            
            layout = QVBoxLayout(dialog)
            layout.setSpacing(20)
            layout.setContentsMargins(20, 20, 20, 20)
            
            # 创建主题信息卡片
            info_card = ClutCard("主题详情", "")
            info_content = QVBoxLayout()
            info_content.setSpacing(15)
            
            # 添加主题信息
            info_items = [
                ("主题名称", theme_data.get("name", "未知")),
                ("版本", theme_data.get("version", "未知")),
                ("作者", theme_data.get("author", "未知")),
                ("描述", theme_data.get("description", "无描述"))
            ]
            
            for label, value in info_items:
                item_widget = QWidget()
                item_layout = QHBoxLayout(item_widget)
                item_layout.setContentsMargins(0, 0, 0, 0)
                
                label_widget = QLabel(f"{label}:")
                label_widget.setStyleSheet("font-weight: bold; color: #2d3436;")
                value_widget = QLabel(value)
                value_widget.setWordWrap(True)
                value_widget.setStyleSheet("color: #2d3436;")
                
                item_layout.addWidget(label_widget)
                item_layout.addWidget(value_widget, 1)
                
                info_content.addWidget(item_widget)
            
            info_card.setContentLayout(info_content)
            layout.addWidget(info_card)
            
            # 预览按钮
            preview_btn = QPushButton("预览主题")
            preview_btn.setMinimumHeight(35)
            preview_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a90e2;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #357abd;
                }
                QPushButton:pressed {
                    background-color: #2868b0;
                }
            """)
            preview_btn.clicked.connect(lambda: self.preview_theme(current_theme))
            
            layout.addWidget(preview_btn)
            
            # 添加阴影效果
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setXOffset(0)
            shadow.setYOffset(0)
            shadow.setColor(QColor(163, 177, 198, 100))
            dialog.setGraphicsEffect(shadow)
            
            dialog.exec_()
            
        except Exception as e:
            logger.error(f"显示主题信息失败: {e}")
            error_notification = OverlayNotification(parent=self)
            error_notification.show_message(
                title="错误",
                message=f"无法加载主题信息: {str(e)}",
                duration=3000
            )

    def preview_theme(self, theme_name):
        """预览主题效果"""
        try:
            # 保存当前主题名称
            current_theme = theme_name
            
            # 临时应用主题
            self.parent().apply_theme(current_theme)
            
            # 3秒后恢复原主题
            config = configparser.ConfigParser()
            config_path = './tsuki/assets/app/config/theme/theme.ini'
            
            if os.path.exists(config_path):
                config.read(config_path, encoding='utf-8')
                original_theme = config.get('Theme', 'current_theme', fallback='default')
            else:
                original_theme = 'default'
                
            QTimer.singleShot(3000, lambda: self.parent().apply_theme(original_theme))
            
            # 显示提示
            notification = OverlayNotification(parent=self)
            notification.show_message(
                title="主题预览",
                message="预览将在3秒后自动恢复",
                duration=2000
            )
        except Exception as e:
            logger.error(f"预览主题失败: {e}")
    
