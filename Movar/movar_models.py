"""
Copyright (C) 2023  Teg Miles

This file is part of Movar.

Movar is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License,
or any later version.

Movar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Movar. If not, see <https://www.gnu.org/licenses/>.
"""

import json
from tkinter import messagebox
from .movar_language_support import InterfaceLanguage
from pathlib import Path
import os, mmap, re, platform
from threading import Thread, Lock
from queue import Queue

class TextSearch(Thread):
    """Клас, де завантажуються словники та відбувається пошук по ним."""
    
    def __init__(self, queue=None, *args, **kwargs):
        """Ініціалізація атрибутів."""
        super().__init__(*args, **kwargs)
        self.path_to_dic = SettingsModel.fields['location']['value']
        self.total_dict = {}
        self.queue = queue
        self.dict_download_lock = Lock()
        
    def run(self):
        with self.dict_download_lock:
            self.load_dictionaries()
            self.queue.put('Done!')
            return
            
    def _show_download_mistake(self, filename):
        """Показати помилку при завантаженні."""
        self.queue.put('Done!')
        language = SettingsModel.fields['language']['value']
        language_options = InterfaceLanguage().translation_options
        title = language_options[language]\
        ['Title dict download mistake']
        message = language_options[language]\
        ['Dict download mistake'] + filename + '!'
        messagebox.showwarning(title, message)
                   
    def load_dictionaries(self):
        """Завантаження словників."""
        for path in self.path_to_dic.splitlines():
            if path:
                for filename in os.listdir(path):
                    if filename.endswith(".txt"):
                        with (open(os.path.join(path, filename), 'rb'
                            ) as file):
                            with mmap.mmap(file.fileno(), 0,
                                access=mmap.ACCESS_READ) as mmap_obj:
                                try:
                                    dict_titles = \
                                        dict(mmap_obj.readline().\
                                        decode().strip().split(':')
                                        for i in range(4))
                                    
                                    full_dict_temp = mmap_obj.read().\
                                        decode(encoding='utf-8')
                                    self.total_dict\
                                    [dict_titles['#Title']]=\
                                        {
                                        'Language pair': \
                                        dict_titles['#Pair'],
                                        'Description': \
                                        dict_titles['#Description'],
                                        'Regex filter': \
                                        dict_titles['#Regex filter'],
                                        'Main body': full_dict_temp,
                                        }
                                except:
                                    self._show_download_mistake(
                                        filename)
                                    return
                        
                for key in self.total_dict.keys():
                    index_dict = {}
                    word_filter = self.total_dict[key]\
                        ['Regex filter'].rstrip()
                    for match in re.finditer(word_filter,
                        self.total_dict[key]['Main body'], re.M):
                        word = match.group()
                        word = word.lower()
                        if word in index_dict.keys():
                            new_span = (index_dict[word][0],
                                match.span()[1])
                            index_dict[word] = new_span
                        else:
                            index_dict[word] = match.span()
                    
                    self.total_dict[key]['Indexes'] = index_dict

class SettingsModel:
    """Клас, де встановлюються й запам'ятовуються налаштування."""
    
    fields = {
        'font size': {'type': 'int', 'value': '14'},
        'font family': {'type': 'str', 'value': ''},
        'theme': {'type': 'str', 'value': 'default'},
        'style': {'type': 'int', 'value': '0'},
        'location' : {'type': 'str', 'value': ''},
        'history' : {'type': 'str', 'value': ''},
        'show_history' : {'type': 'bool', 'value': '1'},
        'active dicts' : {'type': 'str', 'value': ''},
        'dict groups' : {'type': 'str', 'value': ''},
        'default dict group': {'type': 'str', 'value': ''},
        'language' : {'type': 'str', 'value': 'Українська'},
        'sound variable' : {'type': 'bool', 'value': '0'},
        'transparency scale' : {'type': 'float', 'value': '1.0'},
        'tts player': {'type': 'str', 'value': 'None'},
        'tts voice': {'type': 'str', 'value': 'None'},
        'initial dir': {'type': 'str', 'value': 'None'},
        }
        
    config_dirs = {
        'Linux': Path(os.environ.get(
            '$XDG_CONFIG_HOME', Path.home()/'.config')
            ),
        'freebsd7': Path(os.environ.get(
            '$XDG_CONFIG_HOME', Path.home()/'.config')
            ),
        'Windows': Path.home()/'AppData'/'Local'
        }
        
    def __init__(self):
        """Ініціалізація атрибутів класу."""
        filename = 'movar_settings.json'
        filedir = self.config_dirs.get(platform.system(), Path.home())
        self.filepath = filedir/filename
        self.load()
        
    def load(self):
        """Завантаження збережених налаштувань."""
        if not self.filepath.exists():
            return
        with open(self.filepath, 'r', encoding='utf-8') as fh:
            raw_values = json.load(fh)
        for key in self.fields:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.fields[key]['value'] = raw_value
                
    def save(self):
        """Збереження налаштувань."""
        with open(self.filepath, 'w', encoding='utf-8') as fh:
            json.dump(self.fields, fh)
            
    def set(self, key, value):
        """Встановлення значень для налаштувань."""
        if (
            key in self.fields and
            type(value).__name__ == self.fields[key]['type']
            ):
            self.fields[key]['value'] = value
        else:
            raise ValueError("Неправильна назва або тип змінної")
