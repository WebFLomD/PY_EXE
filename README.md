# Как преобразовать с Python-проект в EXE-файл?
## Описание | Теория
**PyInstaller** — это инструмент для упаковки Python-приложений в автономные исполняемые файлы. Он анализирует код, определяет все зависимости и упаковывает всё необходимое в один файл. Это полезно для распространения приложений на компьютеры, где Python или необходимые библиотеки не установлены.

### Принцип работы PyInstaller:
1. **Анализ кода** — PyInstaller изучает ваш скрипт и определяет все необходимые библиотеки
2. **Сбор зависимостей** — собирает интерпретатор Python, все библиотеки и ваши файлы
3. **Упаковка** — создает один файл или папку с программой

### Установка PyInstaller
```bash
pip install pyinstaller
````
---

### Таблица основных параметров PyInstaller
|Параметр|Описание|Пример|
|--------|--------|------|
|`--onefile`|Создает один exe файл|`--onefile`|
|`--onedir`|Создает папку с исполняемым файлом и зависимостями (по умолчанию)|`--onedir`|
|`--add-data`|Добавляет дополнительные файлы или папки в сборку|`--add-data "img;img"`|
|`--name`|Имя выходного файла|`--name "Имя_Проекта"`|
|`--icon`|Добавляет иконку для exe файла|`--icon "img/icon.ico""`|
|`--windowed`|Скрывает консоль|`--windowed`|
|`--noconsole`|То же что и --windowed|`--noconsole`|
|`--console`|Показывает консольное окно (по умолчанию)|`--console`|
|`--hidden-import`|Добавляет скрытые импорты, которые PyInstaller не видит|`--hidden-import project`|
|`--exclude-module`|Исключает ненужные модули|`--exclude-module test`|
|`--clean`|Очистить кэш|`--clean`|
|`--upx-dir`|Указывает путь к UPX для сжатия|`--upx-dir "C:\upx"`|
|`--version-file`|Добавляет информацию о версии|`--version-file "version.txt"`|
|`--log-level`|Устанавливает уровень детализации логов|`--log-level DEBUG`|
|`--key`|Шифрует файлы с помощью указанного ключа|`--key 123456`|

---

### Пример работы с PyInstaller
**❗Важно❗**

❌ **Неправильно:**
```bash
python -m PyInstallet --onefile main.py
# Ошибка: No module named PyInstallet
# Неправильно написал слово, правильно пишется PyInstaller
```
```bash
python -m pyinstaller --onefile main.py
# Ошибка: если написать с маленькой буквы тоже может не сработать
```
✅ **Правильно:**
```bash
python -m PyInstaller --onefile main.py
# ИЛИ
PyInstaller --onefile main.py
```
**Пример**
```bash
# Простая сборка
PyInstaller project.py

# Один файл с иконкой и данными
PyInstaller --onefile --icon "img/icon.ico" --add-data "img;img" project.py

# Без консоли (для оконных приложений)
PyInstaller --onefile --windowed --name "Имя_Проекта" project.py

# Полная сборка с оптимизацией
PyInstaller --onefile --clean --upx-dir "C:\upx" --add-data "img;img" --name "Имя_Проекта" project.py
```


## Задача
Давайте рассмотрим одну задачку, с которой я столкнулся. Эту задачку дал мне преподаватель в ВУЗе, задачка правда интересная, но были некоторые сложности. <br>
Есть проект, написанный на Python с библиотекой `tkinter`и есть изображение в формате `png`. Суть задачи: нужно, чтобы изображение находилось внутри EXE-файла.

## Решение
Изначально я подумал, что это невозможно, потому что если рассуждать логически, изображения должны храниться в отдельной папке. Но всё-таки я попытался найти решение и покажу 2 способа.
```
# Структура проекта
project/
|
├── main.py          # Основной файл
└── img/             # Папка с изображениями
     └── image.png   # Изображение
```
Написал небольшой код в `main.py` с библиотекой `tkinter`, который показывает только изображение:
```python
import tkinter as tk
from tkinter import PhotoImage

parent = tk.Tk()

image = PhotoImage(file="./img/image.png") # Путь к изображению

image_label = tk.Label(parent, image=image)
image_label.pack()

parent.mainloop()
```

### Способ 1. Изображение не входит в EXE.
Самый простой способ преобразования *.py* в *.exe*. Можете найти в разделе `Пример работы с PyInstaller > Пример`.
```bash
PyInstaller --onefile --add-data "img;img" --name Test main.py
```
После того как вы выполнили эту команду, начнется процесс преобразования из .py в .exe. В папке появятся 2 папки (build, dist) и 1 файл (Test.spec). EXE-файл находится в папке dist.<br>
**Важно!** При таком способе изображения **НЕ попадают** внутрь EXE-файла. После сборки нужно вручную скопировать папку с изображениями в папку `dist`.

### Способ 2. Изображение внутри EXE
Второй способ похож на первый, но мы будем работать с `.spec` файлом и добавим специальную функцию в `main.py` <br>
Для начала добавим функцию в `main.py`
```python
import os, sys

# Функция для доступа к файлам (картинки, звуки, базы данных)
# Когда программа скомпилирована в .exe через PyInstaller,
# все файлы распаковываются во временную папку (sys._MEIPASS)
# Эта функция автоматически выбирает правильный путь:
# - При разработке (.py) -> файлы в папке с программой
# - В готовом .exe -> файлы во временной папке PyInstaller
# ВАЖНО: Для работы этой функции нужно в .spec файле указать:
# datas=[('папка_с_файлами', 'папка_назначения')]
# Пример: datas=[('images', 'images'), ('data', 'data')]

def resource_path(relative_path):
  if hasattr(sys, '_MEIPASS'):
      return os.path.join(sys._MEIPASS, relative_path)
  return os.path.join(os.path.abspath('.'), relative_path)

# Использование функции для загрузки изображения
image = PhotoImage(resource_path("img/image.png"))
```
Далее в консоле пишем:
```bash
PyInstaller --onefile main.py
```
Или можете использовать дополнительные параметры:
```bash
PyInstaller --onefile --icon "img/icon.ico" --name "Test" project.py
```

Затем открываем `main.spec` (если вы указали `--name "Test"`, то файл будет называться `Test.spec`) и добавляем в него путь к изображению:
```spec
a = Analysis(
    ['main.py'],
    pathex=['C:\\Users\\Admin\\Desktop\\project\\test_exe'], # Указываем путь к проекту
    ...
)


a.datas += [('./img/image.png', './img/image.png', 'DATA')] # Указываем путь к изображению
...
```

После этого удалите папки `build` и `dist` (если они есть) и выполните в терминале
```bash
PyInstaller main.spec
```
После сборки снова появятся папки `build` и `dist`, а в папке `dist` будет готовый EXE-файл, внутри которого уже находятся все изображения!

## Заключение
Второй способ - это то, что просил преподаватель. Ты получаешь один аккуратный EXE-файл, который можно запустить на любом компьютере, и все изображения будут на месте!

## Источники
- [CyberForum.ru - Как "положить" изображения в EXE файл созданный с PyInstaller?](https://www.cyberforum.ru/python/thread2468049-page2.html)
- [Stack Overflow - Add image to .spec file in Pyinstaller](https://stackoverflow.com/questions/9946760/add-image-to-spec-file-in-pyinstaller)
- [Stack Overflow - Bundling data files with PyInstaller (--onefile)](https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741)

### Может быть будет полезно
- [Aaron Tan's Blog - Creating an executable with PyQt5, PyInstaller, and more](https://blog.aaronhktan.com/posts/2018/05/14/pyqt5-pyinstaller-executable)
- [SkillFactory - 6 способов конвертировать код на Python в exe-файл](https://blog.skillfactory.ru/kak-konvertirovat-kod-na-python-v-exe-fayl/)
- [SkillFactory - Как превратить Python-скрипт в EXE: обзор инструментов и советы по выбору](https://skillbox.ru/media/code/kak-sdelat-exe-fajl-python/)
- [YouTube - Конвертируем .py в .exe | PyInstaller](https://www.youtube.com/live/gmHIcqiCJ7Q)
