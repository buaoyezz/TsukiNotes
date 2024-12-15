import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

def create_crash_report():
    root = tk.Tk()
    root.title("崩溃报告")
    root.geometry("600x400")
    
    # 使用柔和的渐变背景色
    root.configure(bg='#f0e6ff')
    root.overrideredirect(True)

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

    title_bar = tk.Frame(root, bg='#f0e6ff', relief='flat', bd=0, cursor="fleur")
    title_bar.pack(fill=tk.X, padx=10, pady=5)
    
    title_bar.bind('<Button-1>', start_move)
    title_bar.bind('<B1-Motion>', do_move)
    title_bar.bind('<ButtonRelease-1>', stop_move)
    
    title_label = tk.Label(title_bar, text="出错啦 (｡•́︿•̀｡) | 坐和放宽*", bg='#f0e6ff', fg='#9370db', 
                          font=("微软雅黑", 16, "bold"), cursor="fleur")
    title_label.pack(side=tk.LEFT, padx=10)
    
    title_label.bind('<Button-1>', start_move)
    title_label.bind('<B1-Motion>', do_move)
    title_label.bind('<ButtonRelease-1>', stop_move)

    close_button = tk.Button(title_bar, text="×", bg='#f0e6ff', fg='#9370db',
                            relief='flat', bd=0, font=("Arial", 16),
                            activebackground='#e6d9ff',
                            command=root.destroy,
                            cursor="hand2")  # 添加手型光标
    close_button.pack(side=tk.RIGHT, pady=2)
    
    def on_enter(e):
        close_button['bg'] = '#e6d9ff'
        close_button['fg'] = '#7b52c7'
    
    def on_leave(e):
        close_button['bg'] = '#f0e6ff'
        close_button['fg'] = '#9370db'
    
    close_button.bind('<Enter>', on_enter)
    close_button.bind('<Leave>', on_leave)

    frame = tk.Frame(root, bg='#f0e6ff', padx=30, pady=30)
    frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    title_label = tk.Label(frame, text="哎呀,程序崩溃了喵~", 
                          font=("微软雅黑", 24, "bold"), bg='#f0e6ff', fg='#9370db')
    title_label.pack(fill=tk.X, pady=10)

    version_label = tk.Label(frame, text="Crash Report - Ver0.0.1 ₍˄·͈༝·͈˄₎◞ ̑̑", 
                            font=("微软雅黑", 12), bg='#f0e6ff', fg='#a58bd9')
    version_label.pack(fill=tk.X, pady=5)

    message_label = tk.Label(frame, 
                           text="TsukiNotes遇到了一点小问题呢\n别担心,这不是您的问题呐\n您可以去GitHub提交问题喵\n或者重新打开TsukiNotes试试看！(◕ᴗ◕✿)", 
                           font=("微软雅黑", 12), bg='#f0e6ff', fg='#a58bd9')
    message_label.pack(fill=tk.X, pady=20)

    sad_face_label = tk.Label(frame, text="(｡•́︿•̀｡)", 
                             font=("Arial", 30), bg='#f0e6ff', fg='#9370db')
    sad_face_label.pack(fill=tk.X, pady=10)

    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'+{x}+{y}')

    root.mainloop()

if __name__ == "__main__":
    create_crash_report()