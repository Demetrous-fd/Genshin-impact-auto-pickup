# Genshin impact auto pickup

Программа для автоматического сбора предметов в Genshin impact

### [Ссылка на скачивание последней версии GIAP]()

## Требования для запуска

1. Python 3.8.10 или выше
2. [opencv с поддержкой CUDA](https://docs.opencv.org/4.5.2/d3/d52/tutorial_windows_install.html), для запуска на видеокарте NVIDIA
3. Запуск от имени администратора

## Установка зависимостей

`pip install -r requirements.txt`

## Аргументы запуска

1. `-dont-elevate` - _отключает автоматическое возвышение прав программы_
2. `-show-capture` - _отображение окна с распознанными объектами из игры_
3. `-console` - _запуск программы без графического интерфейса_

## Модель для распознавания объектов из проекта

YOLOv4-tiny: [Genshin impact actions](https://github.com/Demetrous-fd/Genshin-impact-actions-YOLOv4-tiny)

## Обратная связь

TG:  @LazyDeus

VK: [LazyDeus](https://vk.com/lazydeus)
