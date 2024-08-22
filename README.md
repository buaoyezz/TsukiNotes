# **TsukiNotes - Capture Your Ideas Anytime, Anywhere**

**Before starting, select a language: [简体中文](README_CN.md) | [English](README.md)**

## About TsukiNotes

TsukiNotes is a powerful note-taking application designed to help you quickly capture and manage all the details of your life. Developed in Python, TsukiNotes ensures efficient and stable performance.

## Features

- **Quick Notes**: A simple interface design allows you to swiftly jot down every idea.
- **Organized Management**: Use tags and categories to keep your notes well-organized.
- **Cloud Sync**: Support for multi-device synchronization, allowing you to access your notes anytime, anywhere.
- **Data Security**: Encrypted storage ensures the privacy and security of your data.
- **Syntax Highlighting**: Enhances your experience by highlighting code in your notes.

## How to Use TsukiNotes

### Launch the Program

1. Download and install TsukiNotes.
2. Open the application and start your note-taking journey.

### Get to Know the Toolbar

- **New Note**: Click the plus icon to quickly create a new note.
- **Search Notes**: Enter keywords to quickly find related notes.
- **Browse by Category**: Manage your notes efficiently by browsing through categories.
- **Settings**: Access the settings menu to personalize your TsukiNotes experience.

### Tips for Effective Use

- **Keyboard Shortcuts**: Learn and use shortcuts to enhance your note-taking efficiency.
- **Tag Management**: Use tags wisely to keep your notes well-ordered.

## Feedback and Suggestions

We greatly appreciate your feedback and suggestions to help us continuously improve TsukiNotes. Please submit your feedback by opening an issue on GitHub.

## Contact Me

- Email: [ZZBuAoYe@gmail.com](https://mail.google.com/mail/u/0/#inbox?compose=new)

## Changelog

- Please refer to the in-app changelog.

## How to Build

1. Install Python 3.12.
2. Install the necessary libraries; `pyqt5` is the core dependency.
3. Use `setup.py` to compile `.pyx` files into `.pyd`, and place them in the preset folder:
    ```bash
    python setup.py build_ext --inplace
    ```
4. Build the main program:
    ```bash
    pyinstaller --add-data "tsuki/assets/kernel/cython_utils.cp312-win_amd64.pyd;tsuki/assets/kernel" your_script.py -i your_icon.ico -w
    ```
5. Note: The `-w` parameter is optional. Replace `your_script.py` and `your_icon.ico` with the actual file names.
6. After building, you may need to reconfigure `.tsuki` files if they were modified.
7. Apologies if the code quality isn't up to your expectations.

> ## **END**

Thank you for choosing TsukiNotes. We are committed to providing you with an exceptional note-taking experience.
