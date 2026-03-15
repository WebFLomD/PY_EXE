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
# Не правильно написал слово, правильно пишется PyInstaller
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
#Простая сборка
PyInstaller project.py

# Один файл с иконкой и данными
PyInstaller --onefile --icon "img/icon.ico" --add-data "img;img" project.py

# Без консоли (для оконных приложений)
PyInstaller --onefile --windowed --name "Имя_Проекта" project.py

# Полная сборка с оптимизацией
PyInstaller --onefile --clean --upx-dir "C:\upx" --add-data "img;img" --name "Имя_Проекта" project.py
```


## Задача
Давайте рассмотрим одну задачку, с которыми я решал. Эту задачку дал мне преподаватель с ВУЗа, задачка правда интересная, но были некоторые сложности. <br>
Есть проект, написанный на Python с библеотекой `tkinter` и есть изображение с форматом `png`. Суть задачи, нужно чтобы изображение находилось в EXE.

## Решение
Изначально я подумал, что это невозможно, потому что если подумать по логике, изображение должны храниться в папке с изображениями. Но все такий попытался найти решение, я покажу 2 решения.
```
project/
|
├── main.py          # Основной файл
└── img/             # Папка с изображениями
     └── image.png   # Изображение
```
Написал небольшой код в `main.py` с библеотекой `tkinter`, который показывает только изображение
```python
import tkinter as tk
from tkinter import PhotoImage

parent = tk.Tk()

image = PhotoImage(file="./img/image.png") # Путь к изображению

image_label = tk.Label(parent, image=image)
image_label.pack()

parent.mainloop()
```

### Способ 1. Изображение не хводит в EXE.
Самый простой способ преобразование  *.py* в *.exe*. Можете найти в пунке `Пример работы с PyInstaller > Пример`.
```bash
PyInstaller --onefile --add-data "img;img" --name Test main.py
```
После того как вы прописали эту команду, пойдет процесс преобразование с *.py* в *.exe*. В папке появится 2 папки (build, dist) и 1 файл(Test.spec). Для того
чтобы найти EXE-файл, находится в папке *dist*, там вы найдет тот самый проект, который вы преобразовали. <br>
**Важно!** При таком способе изображения **НЕ попадают** внутрь EXE-файла. После сборки нужно вручную скопировать папку с изображениями в папку `dist`.

### Способо 2
2 способ, тоже самое, что и с 1. Только, будем работать с `.spec` и добавим функцию|скрипт. Для начала, добавим функцию|скрипт в `main.py`
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
```

Далее в консоле пишем
```bash
PyInstaller --onefile main.py
```

Или можете написать
```bash
PyInstaller --onefile --icon "img/icon.ico" --name "Test" project.py
```

Затем в `main.spec`, если вы в консоле писали `--name "Test"`, то будет `Test.spec`
```spec
a = Analysis(
    ['main.py'],
    pathex=['C:\\Users\\Admin\\Desktop\\project\\test_exe'], # Указываем путь к проекту
    ...
)

a.datas += [('./img/image.png', './img/image.png', 'DATA')] # Указываем путь к изображению
...
```

После этого надо удалить 2 папки (build, dist). И написать в терменале
```bash
PyInstaller main.spec
```
После этого, также появится 2 папки (build, dist), EXE-файл тамже находится

## Источники
- [CyberForum.ru - Как "положить" изображения в EXE файл созданный с PyInstaller?](https://www.cyberforum.ru/python/thread2468049-page2.html)
- [Stack Overflow - Add image to .spec file in Pyinstaller](https://stackoverflow.com/questions/9946760/add-image-to-spec-file-in-pyinstaller)
- [Stack Overflow - Bundling data files with PyInstaller (--onefile)](https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741)
