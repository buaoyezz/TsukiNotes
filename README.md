# **TsukiNotes **<br>** Record your inspiration anytime, anywhere**

**Select language before starting: [Chinese Simplified ](README_CN.md) | [English](README.md)**
## About TsukiNotes

TsukiNotes is a powerful note-taking application designed to help users quickly capture and manage every detail of life. The application is developed in Python, which ensures its efficient and stable operation.

## Features

- **Quick Notes**: Simple interface design allows you to quickly record every inspiration

- **Category Management**: Make notes more organized through tags and classification functions

- **Cloud Sync**: Support multi-device synchronization, access your notes anytime, anywhere

- **Data Security**: Encrypted storage to protect your privacy

- **Highlight**: Highlight your code files to enhance your perception

## How to use TsukiNotes

### Start the program

1. Download the TsukiNotes installer and install the wizard installer

2. After completion, open the application and start your record journey

### Get familiar with the operation bar

- **New Note**: Click the plus icon to quickly create a new note

- **Search Note**: Enter keywords to quickly find related notes

- **Category View**: Browse notes by category for efficient management

- **Settings**: Enter the settings menu to personalize your TsukiNotes

### Usage Tips

- **Shortcuts**: Master shortcuts to improve recording efficiency
- **Tag management**: Use tags properly to make your notes more organized

## Feedback and suggestions

We welcome your valuable comments and suggestions to help us continuously improve TsukiNotes. Please open an issue on Github with your feedback

## Contact me

- Email: [ZZBuAoYe@gmail.com](https://mail.google.com/mail/u/0/#inbox?compose=new)

## Update log

- Please see the software

## How to build

1. Install Python 3.12.5

2. Install the dependency library `PyQt5` is the core GUI

4. Build the main program
Build instructions:
```bash
//Abandoned operation
pyinstaller --add-data "tsuki/assets/kernel/cython_utils.cp312-win_amd64.pyd;tsuki/assets/kernel" xxx.py -i xxx.ico -w
```
> New operation | Easier 1.5.8 starts to abandon the external pyd
```bash
pyinstaller TsukiNotes.py -i logo.ico -w
```
>> Compile the installation wizard as above. GUI is also based on `PyQt5`
5. Note that the `-w` parameter can be added optionally. 1. Please change `xxx` to the actual name
6. After the build is completed, `.tsuki` may be modified by you and needs to be reconfigured
7. The code is a bit old, please forgive me

> ## **END**

Thanks for choosing TsukiNotes<br>
If you like it, please click Star, thank you
