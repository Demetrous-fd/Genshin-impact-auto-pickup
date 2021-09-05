# Genshin impact auto pickup

A program for automatically collecting items in Genshin impact

### [Link to download the latest version of GIMP](https://github.com/Demetrous-fd/Genshin-impact-auto-pickup/releases/latest)

## Requirements

1. Python 3.8.10
2. [Opencv with CUDA support](https://docs.opencv.org/4.5.2/d3/d52/tutorial_windows_install.html) for working on an NVIDIA video card
3. Running as an administrator

## Requirements installation

`pip install -r requirements.txt`

## Startup arguments

1. `-dont-elevate` - _disables automatic elevation of program rights_
2. `-show-capture` - _displaying a window with recognized objects from the game_
3. `-console` - _running the program without a graphical interface_

## QnA

> ### Q: Can I get banned when using this software ?

>> A: Nothing is excluded, Mihoyo does not approve the use of any third-party software for the game

> ### Q: Why does the program need administrator rights ?

>> A: The program can work without administrator rights, but without them it will not be able to emulate keystrokes


## A model for recognizing objects from the project

YOLOv4-tiny: [Genshin impact actions](https://github.com/Demetrous-fd/Genshin-impact-actions-YOLOv4-tiny)

## Feedback

TG:  @LazyDeus

VK: [LazyDeus](https://vk.com/lazydeus)
