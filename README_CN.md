# **TsukiNotes - 随时随地记录您的灵感**

**开始之前选择语言：[简体中文](README_CN.md) | [English](README.md)**
## 关于 TsukiNotes

TsukiNotes 是一款功能强大的笔记记录应用程序，旨在帮助用户快速捕捉和管理生活中的点点滴滴。应用采用 Python 语言开发，保证了其高效稳定的运行。

## 功能特点

- **快速笔记**：简洁的界面设计，让您能够迅速记录每一个灵感
- **分类管理**：通过标签和分类功能，让笔记更有条理
- **云端同步**：支持多设备同步，随时随地访问您的笔记
- **数据安全**：加密存储，保障您的隐私安全
- **高亮显示**：高亮显示您代码文件，增进您的观感

## 如何使用 TsukiNotes

### 启动程序

1. 下载并安装 TsukiNotes。
2. 打开应用程序，开始您的记录之旅。

### 熟悉操作栏

- **新建笔记**：点击加号图标，快速创建新笔记。
- **搜索笔记**：输入关键词，快速找到相关笔记。
- **分类查看**：按照分类浏览笔记，高效管理。
- **设置**：进入设置菜单，个性化您的 TsukiNotes。

### 使用技巧

- **快捷键**：掌握快捷键操作，提高记录效率。
- **标签管理**：合理使用标签，让笔记更有序。

## 反馈与建议

我们非常欢迎您提供宝贵的意见和建议，以帮助我们不断改进 TsukiNotes。请将您的反馈在Github开一个issue

## 联系我

- 邮箱：[ZZBuAoYe@gmail.com](https://mail.google.com/mail/u/0/#inbox?compose=new)

## 更新日志

- 请看软件内

## 如何构建
1. 安装 Python 3.12
2. 安装依赖库'''pyqt5'''是核心
3. 使用set_up.py构建.pyx为pyd，放入预设文件夹 
```bash
python setup.py build_ext --inplace
```
4. 构建主程序
构建所需的指令: 
```bash
pyinstaller --add-data "tsuki/assets/kernel/cython_utils.cp312-win_amd64.pyd;tsuki/assets/kernel" xxx.py -i xxx.ico -w
```
5. 值得注意的 `-w` 参数可以选择性添加1，`xxx`请改为实际名称
6. 构建完成后将`.tsuki`可能被您改动，需要重新配置
7. 代码写的有点史，见谅

> ## **END**

感谢您选择 TsukiNotes，我们将竭诚为您服务，为您提供优质的笔记记录体验。
