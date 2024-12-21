import os

def load_stylesheet(filename):
    """
    加载QSS样式表文件
    
    Args:
        filename: QSS文件名 (例如: 'sidebar.qss')
        
    Returns:
        str: QSS样式表内容
    """
    # 获取项目根目录路径
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # 构建样式文件的完整路径
    file_path = os.path.join(root_dir, 'assets', 'ui', filename)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"警告: 样式文件 {filename} 未找到")
        return ""
    except Exception as e:
        print(f"加载样式文件 {filename} 时发生错误: {str(e)}")
        return "" 