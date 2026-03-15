import os, sys
import tkinter as tk
from tkinter import PhotoImage


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


parent = tk.Tk()

# Использование функции для загрузки изображения
image = PhotoImage(file=resource_path("./img/image.png"))

image_label = tk.Label(parent, image=image)
image_label.pack()

parent.mainloop()