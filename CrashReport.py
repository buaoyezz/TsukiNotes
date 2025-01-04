import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import random
import time

def create_crash_report():
    root = tk.Tk()
    root.title("崩溃报告Crash Report | TsukiNotes_ReportKernelB2*BugFix")
    # 增加窗口初始大小
    root.geometry("900x600")  # 调整为更大的尺寸
    
    # 使用更可爱的粉色渐变背景
    root.configure(bg='#ffe6f2')
    root.overrideredirect(True)
    root.attributes('-alpha', 0.0)  # 初始透明

    # 渐入动画
    def fade_in():
        alpha = root.attributes('-alpha')
        if alpha < 1.0:
            root.attributes('-alpha', alpha + 0.1)
            root.after(50, fade_in)
    
    fade_in()

    global x, y
    x = None
    y = None

    def start_move(event):
        global x, y
        x = event.x
        y = event.y

    def stop_move(event):
        global x, y
        x = None
        y = None

    def do_move(event):
        global x, y
        if x is not None and y is not None:
            deltax = event.x - x
            deltay = event.y - y
            new_x = root.winfo_x() + deltax
            new_y = root.winfo_y() + deltay
            root.geometry(f"+{new_x}+{new_y}")

    # 可爱的表情列表
    kawaii_faces = ["(◕ᴗ◕✿)", "(｡♥‿♥｡)", "ʕ•ᴥ•ʔ", "(◕‿◕✿)", "(｡◕‿◕｡)", "♡(◡‿◡✿)", 
                    "(✿◠‿◠)", "(◕‿◕)", "ʕ•́ᴥ•̀ʔ", "(｡•́‿•̀｡)", "ʕ·ᴥ·ʔ", "(◕ω◕)", 
                    "(´･ᴗ･`)", "(◍•ᴗ•◍)", "ʕ•ᴥ•ʔ♡", "(´｡• ᵕ •｡`)", "(◕‿◕✿)", 
                    "(｡♥‿♥｡)", "(◡‿◡✿)", "(◕ᴗ◕✿)", "ʕ•ᴥ•ʔ", "(✿ ♥‿♥)", 
                    "(◕‿◕)", "(｡◕‿◕｡)", "ʕ•ᴥ•ʔ", "(◕ω◕✿)", "(｡•́‿•̀｡)", 
                    "(◍•ᴗ•◍)❤", "(◕‿◕✿)", "ʕ•ᴥ•ʔ", "(｡♥‿♥｡)", "(◡‿◡✿)", 
                    "(◕ᴗ◕✿)", "ʕ•ᴥ•ʔ", "(✿ ♥‿♥)", "(◕‿◕)", "(｡◕‿◕｡)", 
                    "ʕ•ᴥ•ʔ", "(◕ω◕✿)", "(｡•́‿•̀｡)", "(◍•ᴗ•◍)❤", "(◕‿◕✿)", 
                    "ʕ•ᴥ•ʔ", "(｡♥‿♥｡)", "(◡‿◡✿)", "(◕ᴗ◕✿)", "ʕ•ᴥ•ʔ", 
                    "(✿ ♥‿♥)", "(◕‿◕)", "(｡◕‿◕｡)", "ʕ•ᴥ•ʔ", "(◕ω◕✿)",
                    "(｡>﹏<｡)", "ಥ_ಥ", "(´;ω;｀)", "(;´д｀)", "(´;ω;｀)", 
                    "(｡•́︿•̀｡)", "( ˃̣̣̥ω˂̣̣̥ )", "(｡ŏ﹏ŏ)", "(｡•́︿•̀｡)", "( ´•̥̥̥ω•̥̥̥` )",
                    "(◕‿◕✿)", "(｡♥‿♥｡)", "ʕ•ᴥ•ʔ", "(✿◠‿◠)", "(｡◕‿◕｡)", 
                    "♡(◡‿◡✿)", "(◕ᴗ◕✿)", "ʕ•́ᴥ•̀ʔ", "(｡•́‿•̀｡)", "ʕ·ᴥ·ʔ",
                    "(◕ω◕)", "(´･ᴗ･`)", "(◍•ᴗ•◍)", "ʕ•ᴥ•ʔ♡", "(´｡• ᵕ •｡`)",
                    "(✿ ♥‿♥)", "(◕‿◕)", "(｡◕‿◕｡)", "ʕ•ᴥ•ʔ", "(◕ω◕✿)",
                    "(｡>﹏<｡)", "ಥ_ಥ", "(´;ω;｀)", "(;´д｀)", "(´;ω;｀)",
                    "(｡•́︿•̀｡)", "( ˃̣̣̥ω˂̣̣̥ )", "(｡ŏ﹏ŏ)", "(｡•́︿•̀｡)", "( ´•̥̥̥ω•̥̥̥` )",
                    "(◕‿◕✿)", "(｡♥‿♥｡)", "ʕ•ᴥ•ʔ", "(✿◠‿◠)", "(｡◕‿◕｡)",
                    "♡(◡‿◡✿)", "(◕ᴗ◕✿)", "ʕ•́ᴥ•̀ʔ", "(｡•́‿•̀｡)", "ʕ·ᴥ·ʔ",
                    "(◕ω◕)", "(´･ᴗ･`)", "(◍•ᴗ•◍)", "ʕ•ᴥ•ʔ♡", "(´｡• ᵕ •｡`)",
                    "(✿ ♥‿♥)", "(◕‿◕)", "(｡◕‿◕｡)", "ʕ•ᴥ•ʔ", "(◕ω◕✿)",
                    "( ˘•ω•˘ )", "(◕‿◕✿)", "(｡♥‿♥｡)", "ʕ•ᴥ•ʔ", "(✿◠‿◠)",
                    "(｡◕‿◕｡)", "♡(◡‿◡✿)", "(◕ᴗ◕✿)", "ʕ•́ᴥ•̀ʔ", "(｡•́‿•̀｡)",
                    "ʕ·ᴥ·ʔ", "(◕ω◕)", "(´･ᴗ･`)", "(◍•ᴗ•◍)", "ʕ•ᴥ•ʔ♡"]

    title_bar = tk.Frame(root, bg='#ffe6f2', relief='flat', bd=0, cursor="fleur")
    title_bar.pack(fill=tk.X, padx=10, pady=5)
    
    title_bar.bind('<Button-1>', start_move)
    title_bar.bind('<B1-Motion>', do_move)
    title_bar.bind('<ButtonRelease-1>', stop_move)
    
    title_label = tk.Label(title_bar, text=f"出错啦 {random.choice(kawaii_faces)} | 让我们一起解决吧~", bg='#ffe6f2', fg='#ff69b4', 
                          font=("微软雅黑", 16, "bold"), cursor="fleur")
    title_label.pack(side=tk.LEFT, padx=10)
    
    title_label.bind('<Button-1>', start_move)
    title_label.bind('<B1-Motion>', do_move)
    title_label.bind('<ButtonRelease-1>', stop_move)

    # 添加呼吸灯效果的关闭按钮
    close_button = tk.Button(title_bar, text="×", bg='#ffe6f2', fg='#ff69b4',
                            relief='flat', bd=0, font=("Arial", 16),
                            activebackground='#ffd1e6',
                            command=lambda: close_with_animation(root),
                            cursor="hand2")
    close_button.pack(side=tk.RIGHT, pady=2)
    
    def on_enter(e):
        close_button['bg'] = '#ffd1e6'
        close_button['fg'] = '#ff1493'
    
    def on_leave(e):
        close_button['bg'] = '#ffe6f2'
        close_button['fg'] = '#ff69b4'
    
    close_button.bind('<Enter>', on_enter)
    close_button.bind('<Leave>', on_leave)

    # 调整frame的内边距
    frame = tk.Frame(root, bg='#ffe6f2', padx=40, pady=40)  # 增加内边距
    frame.pack(expand=True, fill=tk.BOTH, padx=25, pady=25)

    # 调整标题标签
    title_label = tk.Label(frame, text="哎呀,程序遇到了一点小问题~", 
                          font=("微软雅黑", 24, "bold"), 
                          bg='#ffe6f2', 
                          fg='#ff69b4',
                          wraplength=550)  # 添加自动换行
    title_label.pack(fill=tk.X, pady=(0, 20))  # 增加底部间距
    message_text = f"""别担心呢 User~ {random.choice(kawaii_faces)}

这不是您的错哦！现在您可以：

1. 您可以去 GitHub 提交问题~
2. 或者重新打开 TsukiNotes 试试看！{random.choice(kawaii_faces)}
3. 上传 Github Issue 后我们看到后会努力修复这个问题的！{random.choice(kawaii_faces)}
4. 如果给您带来不便，请您谅解！{random.choice(kawaii_faces)}
"""
    
    message_label = tk.Label(frame, text=message_text,
                           font=("微软雅黑", 12), 
                           bg='#ffe6f2', 
                           fg='#ff8dc7',
                           justify=tk.LEFT,
                           wraplength=550,  # 增加文字换行宽度
                           anchor='w')  # 文字左对齐
    message_label.pack(fill=tk.BOTH, expand=True, pady=20, padx=30)

    # 调整版本标签的样式
    version_label = tk.Label(frame, 
                           text=f"Crash Report - Ver0.0.2 {random.choice(kawaii_faces)}", 
                           font=("微软雅黑", 12), 
                           bg='#ffe6f2', 
                           fg='#ff8dc7',
                           pady=10)  # 增加内边距
    version_label.pack(fill=tk.X, pady=5)

    # 添加动画控制标志
    root.animation_running = True

    # 修改breathing_animation函数
    def breathing_animation():
        if not root.animation_running:
            return
        colors = ['#ff69b4', '#ff8dc7', '#ffb6c1', '#ff8dc7']
        i = 0
        def update_color():
            if not root.animation_running:
                return
            nonlocal i
            try:
                sad_face_label.config(fg=colors[i])
                i = (i + 1) % len(colors)
                root.after(800, update_color)
            except tk.TclError:
                return
        update_color()

    # 修改update_face函数
    def update_face():
        if not root.animation_running:
            return
        try:
            new_face = random.choice(kawaii_faces)
            for alpha in range(10, -1, -1):
                if not root.animation_running:
                    return
                sad_face_label.config(fg=f'#{int(alpha/10*255):02x}69b4')
                root.update()
                time.sleep(0.02)  # 稍微加快动画
            sad_face_label.config(text=new_face)
            for alpha in range(0, 11):
                if not root.animation_running:
                    return
                sad_face_label.config(fg=f'#{int(alpha/10*255):02x}69b4')
                root.update()
                time.sleep(0.02)
            root.after(2000, update_face)
        except tk.TclError:
            return

    sad_face_label = tk.Label(frame, text=random.choice(kawaii_faces),
                             font=("Arial", 30), bg='#ffe6f2', fg='#ff69b4')
    sad_face_label.pack(fill=tk.X, pady=10)
    
    breathing_animation()
    update_face()

    # 添加文字悬浮效果
    def add_hover_effect(widget):
        def on_enter(e):
            widget.config(font=("微软雅黑", widget.cget("font").split()[1], "bold"))
            widget['fg'] = '#ff1493'
        def on_leave(e):
            widget.config(font=("微软雅黑", widget.cget("font").split()[1]))
            widget['fg'] = '#ff8dc7'
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)

    # 修改close_with_animation函数
    def close_with_animation(root):
        root.animation_running = False
        def fade_out():
            alpha = root.attributes('-alpha')
            if alpha > 0:
                root.attributes('-alpha', alpha - 0.1)
                root.after(50, fade_out)
            else:
                root.destroy()
        fade_out()

    # 为消息标签添加悬浮效果
    add_hover_effect(message_label)
    add_hover_effect(version_label)

    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'+{x}+{y}')

    root.mainloop()

if __name__ == "__main__":
    create_crash_report()