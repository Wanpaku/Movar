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

import ast, webbrowser
import tkinter as tk
from tkinter import ttk, font, messagebox, Toplevel, filedialog
from .movar_views import ColorStyles
from .movar_models import SettingsModel, TextSearch
from .movar_language_support import InterfaceLanguage

class TopWindow(tk.Toplevel):
    """Клас, що відповідає за горішні вікна."""
    
    def __init__(self, *args, **kwargs):
        """Ініціалізація атрибутів."""
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.resizable(True, True)
        
class FrameWindow(ttk.Frame):
    """Клас, що відповідає за рамки(frame)."""
    
    def __init__(self, parent, *args, **kwargs):
        """Ініціалізація атрибутів."""
        super().__init__(parent, *args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.configure(
        borderwidth=5,
        padding=5, 
        style="Description.TFrame",
        )
        
        self.grid(sticky='nsew')
        
class NotebookWindow(ttk.Notebook):
    """Клас, що відповідає за записники(notebook)."""
    
    def __init__(self, parent, *args, **kwargs):
        """Ініціалізація атрибутів."""
        super().__init__(parent, *args, **kwargs)
        self.configure(style='Settings.TNotebook')
        
        self.grid(sticky='nsew')
        
class GenericMenu(tk.Menu):
    """Клас, що відповідає за загальні налаштування віджетів-меню."""
    accelerators = {
        'Вихід': 'Ctrl+Q',
        'Налаштування словників': 'F2'
        }
    
    keybinds = {
        '<Control-q>': '<<FileQuit>>',
        '<F2>': '<<DictSettings>>',
        }

    def __init__(self, parent, settings, total_dict, *args, **kwargs):
        """Ініціалізація атрибутів."""
        super().__init__(*args, **kwargs)
        self.settings = settings
        self.settings_model = SettingsModel()
        self.total_dict = total_dict
        self.configure(tearoff=False)
        self._menus = dict()
        self.dict_lists = dict()
        self.color_styles = ColorStyles(self, self.settings)
        self.bg_style = self.color_styles.styles[self.color_styles.n]
        self.configure(**self.bg_style)
        self.language_options = \
            InterfaceLanguage().translation_options
        self._dictionary_interface_labels()
        self._add_variables_for_widgets()
        
        self._build_main_menu()
        self._bind_accelerators()
        self._set_tracing_variables()
        
    def _add_variables_for_widgets(self):
        """Додавання відстежуваних змінних для віджетів."""
        #Змінна для показу історії пошуку
        self.on_off = tk.IntVar()
        self.on_off.set(self.settings['show_history'].get())
        #Змінна для ввімкнення програвання слів
        self.sound_checkbutton_variable = tk.IntVar()
        self.sound_checkbutton_variable.set(
            self.settings['sound variable'].get())
        #Змінна для шкали прозорості
        self.transparency_scale_variable = tk.DoubleVar()
        self.transparency_scale_variable.set(
            self.settings['transparency scale'].get())
        #Змінна для програвача тексту
        self.tts_player_var = tk.StringVar()
        #Змінна для голосу програвача тексту
        self.tts_voice_var = tk.StringVar()
        #Змінна для меню вибору родини шрифтів
        self.font_family_var = tk.StringVar()
        #Перелік доступних голосів для програвачів тексту
        self.tts_voice_options = ["None"]
        
    def _add_quit_menu(self, menu):
        """Додавання функції 'Вихід' до головного меню."""
        menu.add_command(
            label=self.add_quit_menu_label,
            command=self._event('<<FileQuit>>'),
            accelerator=self.accelerators.get('Вихід')
            )
            
    def _add_language_menu(self, menu):
        """Додавання меню вибору мови інтерфейсу."""
        language_menu = tk.Menu(self, tearoff=False, **self.bg_style)
        for i in self.language_options.keys():
            language_menu.add_radiobutton(
            label=i, value=i,
            variable=self.settings['language'])
            
        menu.add_cascade(
            label="Interface language", menu=language_menu)
            
    def _add_dictionaries_settings_menu(self, menu):
        """Додавання меню 'Налаштування словників'."""
        menu.add_command(
            label=self.dict_settings_menu_label,
            command=self._dictionaries_settings_window,
            accelerator=self.accelerators.get('Налаштування словників')
            )
    
    def _add_search_history_menu(self, menu):
        """Додавання меню "Історія пошуку"."""
        history_menu = tk.Menu(self, tearoff=False, **self.bg_style)
        menu.add_cascade(
            label=self.search_history_label, menu=history_menu)
        history_menu.add_command(label=self.clear_history_label,
            command=self._cleaning_search_history)
        history_menu.add_checkbutton(
            label=self.show_history_label,
            command=self._show_history, variable=self.on_off)
            
    def _add_font_size_menu(self, menu):
        """Додавання меню вибору розміру шрифту."""
       
        size_menu = tk.Menu(self, tearoff=False, **self.bg_style)
        menu.add_cascade(
            label=self.add_font_size_menu_label, menu=size_menu)
        for size in range(6, 27, 1):
            size_menu.add_radiobutton(
                label=size, value=size,
                variable=self.settings['font size']
                )
        
    def _set_current_font_family(self):
        """Встановлення поточного фону."""
        default_font_family = self.settings['font family'].get()
        for index, font_family in enumerate(self.font_family_options):
            if font_family == default_font_family:
                self.font_family_menu.current(index)
                
    def _add_themes_menu(self, menu):
        """Додавання меню вибору тем."""
        theme_menu = tk.Menu(self, tearoff=False, **self.bg_style)
        for theme in self.color_styles.theme_names():
            theme_menu.add_radiobutton(
            label=theme, value=theme,
            variable=self.settings['theme']
            )
        menu.add_cascade(
            label=self.add_themes_menu_label, menu=theme_menu)
        
    def _add_styles_menu(self, menu):
        """Додавання меню вибору кольорових стилів."""
        style_menu = tk.Menu(self, tearoff=False, **self.bg_style)
        for i in range(len(self.color_styles.styles)):
            style_menu.add_radiobutton(
            label=i, value=i,
            variable=self.settings['style'])
            
        menu.add_cascade(
            label=self.add_style_menu_label, menu=style_menu)
        
    def _add_about_menu(self, menu):
        """Додавання меню "Про Мовар"."""
        about_menu = tk.Menu(self, tearoff=False, **self.bg_style)
        menu.add_command(label=self.about_menu_label,
                        command=self._show_about)
        menu.add_command(label=self.manual_label,
                        command=self._show_manual_text
                        )
            
    def _event(self, sequence):
        """Проста функція-обгортка."""
        def callback(*_):
            """Функція виклику."""
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)
        return callback
        
    def _build_main_menu(self):
        """Побудова головного меню програми."""
        #Файлове меню
        self._menus[self.file_label] = tk.Menu(self,
            tearoff=False, **self.bg_style)
        self._menus[self.file_label].add_separator()
        self._add_quit_menu(self._menus[self.file_label])
        
        #Меню налаштувань
        self._menus[self.settings_label] = tk.Menu(self,
            tearoff=False, **self.bg_style)
        self._add_language_menu(self._menus[self.settings_label])
        self._add_dictionaries_settings_menu(
            self._menus[self.settings_label])
        self._add_search_history_menu(self._menus[self.settings_label])
        self._add_font_size_menu(self._menus[self.settings_label])
        self._add_themes_menu(self._menus[self.settings_label])
        self._add_styles_menu(self._menus[self.settings_label])
        
        #Меню "Про програму"
        self._menus[self.help_label] = tk.Menu(self,
            tearoff=False, **self.bg_style)
        self._add_about_menu(self._menus[self.help_label])
        
        #Завантаження всіх меню
        for label, menu in self._menus.items():
            self.add_cascade(label=label, menu=menu)
        
    def _bind_accelerators(self):
        """Прив'язка скорочень до комбінацій клавіш."""
        for key, sequence in self.keybinds.items():
            self.bind_all(key, self._event(sequence))
            
    def _dictionary_interface_labels(self):
        """Завантаження значень мовної підтримки програми."""
        translations = self.language_options
        selected_language = self.settings['language'].get()
        self.path_to_dict_label = \
            translations[selected_language]['Paths to dictionaries']
        self.dict_groups_label = \
            translations[selected_language]['Groups of dictionaries']
        self.technical_settings_label = \
            translations[selected_language]['Technical settings']
        self.select_path_to_dict_label = \
            translations[selected_language]\
            ['Select path to dictionaries']
        self.del_path_to_dict_label = \
            translations[selected_language]\
            ['Delete path to dictionaries']
        self.del_all_paths_to_dict_label = \
            translations[selected_language]\
            ['Delete all paths to dictionaries']
        self.avail_dict_label = \
            translations[selected_language]['Available dictionaries']
        self.add_dict_to_group_label = \
            translations[selected_language]['Add dictionary'] + '>>'
        self.del_dict_from_group_label = \
            translations[selected_language]['Delete dictionary'] + '<<'
        self.create_dict_group_label = \
            translations[selected_language]\
            ['Create group of dictionaries']
        self.del_dict_group_label = \
            translations[selected_language]\
            ['Delete group of dictionaries']
        self.del_all_dict_groups_label = \
            translations[selected_language]\
            ['Delete all groups of dictionaries']
        self.file_label = translations[selected_language]['File']
        self.settings_label = \
            translations[selected_language]['Settings']
        self.help_label = translations[selected_language]['Help']
        self.about_menu_label = \
            translations[selected_language]['About Movar']
        self.add_style_menu_label = \
            translations[selected_language]['Select style']
        self.add_themes_menu_label = \
            translations[selected_language]['Select theme']
        self.add_font_family_menu_label = \
            translations[selected_language]['Font family']
        self.add_font_size_menu_label = \
            translations[selected_language]['Font size']
        self.search_history_label = \
            translations[selected_language]['Search history']
        self.clear_history_label = \
            translations[selected_language]['Clear search history']
        self.show_history_label = \
            translations[selected_language]['Show/hide search history']
        self.dict_settings_menu_label = \
            translations[selected_language]['Dictionary settings']
        self.add_quit_menu_label = \
            translations[selected_language]['Exit']
        self.on_off_playing_word = \
            translations[selected_language]['On/Off playing word']
        self.transparency_scale_label = \
            translations[selected_language]['Transparency scale']
        self.enter_dict_group_name_label = \
            translations[selected_language]['Enter name dict group']
        self.OK_label = translations[selected_language]['OK']
        self.cancel_label = translations[selected_language]['Cancel']
        self.tts_player_name_label = \
            translations[selected_language]['TTS player name']
        self.tts_player_voice_label = \
            translations[selected_language]['TTS player voice']
        self.show_dict_descr_button_label = \
            translations[selected_language]\
            ['Show dictionary description']
        self.descr_dict_title = translations[selected_language]\
            ['Title show description messagebox']
        self.descr_dict_message = translations[selected_language]\
            ['Message show description messagebox']
        self.font_family_label = \
            translations[selected_language]['Font family label']
        self.choose_dict_loc_label = \
            translations[selected_language]['Choose dict location']
        self.menu_about_text = \
            translations[selected_language]['Menu About']
        self.manual_label = \
            translations[selected_language]['Manual']
        self.manual_text = \
            translations[selected_language]['Manual text']
            
    def _dictionaries_settings_window(self, *_):
        """Відкриття вікна налаштування розташування словників."""
        #Створення нового вікна
        self.top = TopWindow()
        self.top.title(self.dict_settings_menu_label)
        
        self.global_frame = FrameWindow(self.top)
        
        notebook_frame = FrameWindow(self.global_frame)
        notebook_frame.configure(borderwidth=0, padding=0)
        notebook_frame.grid(columnspan=2, sticky='nsew')
        
        notebook = NotebookWindow(notebook_frame)
        
        self.frame_1 = FrameWindow(notebook)
        self.frame_1_buttons = FrameWindow(self.frame_1)
        self.frame_1_buttons.rowconfigure(100, weight=100)
        self.frame_1_buttons.grid(column=1, rowspan=2)
        
        self.frame_2 = FrameWindow(notebook)
        self.frame_2_dict_buttons = FrameWindow(self.frame_2)
        self.frame_2_dict_buttons.rowconfigure(12, weight=3)
        self.frame_2_dict_buttons.grid(row=1, column=2)
        self.frame_2_groups = FrameWindow(self.frame_2)
        self.frame_2_groups.grid(row=1, column=3)
        
        self.frame_3 = FrameWindow(notebook)
        
        notebook.add(self.frame_1, text=self.path_to_dict_label)
        notebook.add(self.frame_2, text=self.dict_groups_label)
        notebook.add(self.frame_3, text=self.technical_settings_label)
        
        self._add_ok_cancel_to_global_frame()
        self._add_dictionary_paths_window()
        self._add_dictionary_groups_window()
        self._add_technical_settings_window()
        
    def _add_ok_cancel_to_global_frame(self):
        """Додавання кнопок закриття меню налаштувань."""
        ok_button = ttk.Button(self.global_frame,
            text=self.OK_label,
            style='NewButton.TButton',
            command=self._closing_settings_window
            )
        ok_button.grid(row=2, column=0, sticky='e')
        
        cancel_button = ttk.Button(self.global_frame,
            text=self.cancel_label,
            style='NewButton.TButton',
            command=self._closing_settings_window
            )
        cancel_button.grid(row=2, column=1, sticky='w')
        
    def _add_dictionary_paths_window(self):
        """Текстове поле з місцями розташування словників"""
        xScroll = ttk.Scrollbar(self.frame_1,
            orient=tk.HORIZONTAL, style="Xscroll.Horizontal.TScrollbar")
        
        self.locations = tk.Listbox(self.frame_1, 
            exportselection=0,
            selectbackground=self.bg_style['activebackground'],
            width=50,
            xscrollcommand=xScroll.set
            )
        xScroll['command'] = self.locations.xview
        xScroll.grid(row=1, column=0, sticky='we')
        self.locations.grid(row=0, column=0, sticky="nsew")
        self._set_dictionary_location()
        self.locations.bind('<Button-1>', self._select_location)
        
        open_directory_button = ttk.Button(self.frame_1_buttons,
            text=self.select_path_to_dict_label,
            command=self._open_dictionary_directory,
            style="NewButton.TButton")
        open_directory_button.grid(row=0, column=0, sticky='nwe')
        
        delete_directory_button = ttk.Button(self.frame_1_buttons,
            text=self.del_path_to_dict_label,
            command=self._delete_dictionary_directory,
            style="NewButton.TButton")
        delete_directory_button.grid(row=1, column=0, sticky='nwe')
        
        delete_all_directories_button = ttk.Button(self.frame_1_buttons,
            text=self.del_all_paths_to_dict_label,
            command=self._delete_all_dictionary_directories,
            style="NewButton.TButton")
        delete_all_directories_button.grid(row=2,
            column=0, sticky='nwe')
            
    def _closing_settings_window(self, *_):
        """Закриття вікна налаштувань."""
        self.top.withdraw()
        
    def _add_dictionary_groups_window(self):
        """Додавання вікна з групами словників."""
        self._create_list_of_available_dictionaries()
        
        self._add_frame_for_description_of_dictionary()
        
        self._add_buttons_for_dictionary_groups_and_description()
        
        self._add_buttons_for_creating_and_deleting_dict_groups()
        
        self.dict_group_list = NotebookWindow(self.frame_2_groups)
        self.dict_group_list.grid(row=0, column=0)
        self._set_dictionary_groups()
    
    def _add_buttons_for_creating_and_deleting_dict_groups(self, *_):
        """Додавання кнопок створення/видалення груп словників."""
        #Кнопки створення та видалення груп словників
        create_dict_group_button = ttk.Button(self.frame_2_groups,
            style='NewButton.TButton',
            text=self.create_dict_group_label,
            command=self._ask_name_of_dict_group)
        create_dict_group_button.grid(row=1, column=0, sticky='nsew')
        
        delete_dict_group_button = ttk.Button(self.frame_2_groups,
            style='NewButton.TButton',
            text=self.del_dict_group_label,
            command=self._delete_selected_dictionary_group)
        delete_dict_group_button.grid(row=2, column=0, sticky='nsew')
        
        delete_all_dict_group_button = ttk.Button(self.frame_2_groups,
            style='NewButton.TButton',
            text=self.del_all_dict_groups_label,
            command=self._delete_all_dictionary_groups)
        delete_all_dict_group_button.grid(row=3,
            column=0, sticky='nsew')
        
    def _add_buttons_for_dictionary_groups_and_description(self, *_):
        """Додавання кнопок для груп та опису словників."""
        #Кнопки додавання, вилучення словників
        add_dict_button = ttk.Button(self.frame_2_dict_buttons,
            style='NewButton.TButton',
            text=self.add_dict_to_group_label,
            command=self._add_dict_to_a_group)
        add_dict_button.grid(row=9, column=0, sticky='swe')
        
        del_dict_button = ttk.Button(self.frame_2_dict_buttons,
            style='NewButton.TButton',
            text=self.del_dict_from_group_label,
            command=self._delete_dict_from_a_group)
        del_dict_button.grid(row=10, column=0, sticky='nwe')
        
        #Кнопка перегляду опису словника
        show_dict_descr_button = ttk.Button(
            self.frame_2_dict_buttons,
            style='NewButton.TButton',
            text=self.show_dict_descr_button_label,
            command=self._show_dictionary_description)
        show_dict_descr_button.grid(row=11, column=0, sticky='nwe')
        
    def _add_frame_for_description_of_dictionary(self, *_):
        """Додавання рамки для опису словників."""
        self.dict_description = tk.scrolledtext.ScrolledText(
            self.frame_2, bg='white',
            state='disabled',
            wrap=tk.WORD,
            height=4
            )
        self.dict_description.vbar.configure(
            troughcolor=self.bg_style['foreground'], 
            bg=self.bg_style['background'],
            activebackground=self.bg_style['activebackground'],
            borderwidth=5
                )
        self.dict_description.grid(
            row=3, column=0, columnspan=4, sticky='nsew')
        
    def _create_list_of_available_dictionaries(self, *_):
        """Створення переліку наявних словників."""
        #Напис-позначка для наявних словників
        total_dict_label = ttk.Label(self.frame_2,
            text=self.avail_dict_label, style="NewLabel.TLabel")
        total_dict_label.grid(row=0, column=0, sticky='w')
        
        yScroll_f2 = ttk.Scrollbar(self.frame_2,
            orient=tk.VERTICAL, style="Yscroll.Vertical.TScrollbar")
            
        xScroll_f2 = ttk.Scrollbar(self.frame_2,
            orient=tk.HORIZONTAL, style="Xscroll.Horizontal.TScrollbar")
        
        #Listbox із активними словниками
        self.total_dict_list = tk.Listbox(self.frame_2,
            selectbackground=self.bg_style['activebackground'],
            yscrollcommand=yScroll_f2.set,
            xscrollcommand=xScroll_f2.set,
            selectmode=tk.MULTIPLE,
            )
        yScroll_f2['command'] = self.total_dict_list.yview
        xScroll_f2['command'] = self.total_dict_list.xview
        yScroll_f2.grid(row=1, column=1, sticky='ns')
        xScroll_f2.grid(row=2, column=0, sticky='we')
        self.total_dict_list.grid(row=1, column=0,
            sticky="nsew")
        
        #Завантаження переліка активних словників
        self._set_active_dictionary_list()
        
    def _show_dictionary_description(self, *_):
        """Додавання опису словника при його виділенні
        у віджеті "Наявні словники"."""
        if len(self.total_dict_list.curselection()) == 1:
            selected_dict_index = self.total_dict_list.curselection()
            selected_dict = \
                self.total_dict_list.get(selected_dict_index)
            dict_name = selected_dict.split('(')[0]
            description = self.total_dict[dict_name]['Description']
            self.dict_description.configure(state='normal')
            self.dict_description.delete('1.0', 'end')
            self.dict_description.insert('1.0', description)
            self.dict_description.configure(state='disabled')
        else:
            messagebox.showwarning(
                self.descr_dict_title,
                self.descr_dict_message,
                parent=self.top)
        
    def _add_technical_settings_window(self):
        """Додавання вікна з технічними налаштуваннями."""
        self.frame_3.columnconfigure(100, weight=100)
        self.frame_3.rowconfigure(100, weight=100)
        
        self._add_button_on_off_spelling_words()
        
        self._add_transparency_scale()
            
        self._add_engines_for_tts()
        
        self._add_voices_for_tts_engine()
        
        self._add_font_family_choices()
        
        
    def _add_font_family_choices(self, *_):
        """Додавання меню вибору родини шрифтів."""
        #Напис-позначка для меню вибору родини шрифтів
        self.font_family_sign = ttk.Label(self.frame_3,
            text=self.font_family_label,
            style="NewLabel.TLabel")
        self.font_family_sign.grid(row=5, column=0, sticky='w')
        
        #Створення меню родини шрифтів
        self.font_family_options = sorted(list(set(font.families())))
        
        self.font_family_menu = ttk.Combobox(self.frame_3,
                                    textvariable=self.font_family_var,
                                    #default_voice_option,
                                    values = self.font_family_options,
                                    state='readonly',
                                    style='NewCombobox.TCombobox',
                                    )
        
        self.font_family_menu.grid(row=6, column=0, sticky='nsew')
        self._set_current_font_family()
        
    def _add_voices_for_tts_engine(self, *_):
        """Додавання голосів для рушія вимови тексту."""
        #Напис-позначка для голосу програвача тексту
        self.tts_player_voice = ttk.Label(self.frame_3,
            text=self.tts_player_voice_label,
            style="NewLabel.TLabel")
        self.tts_player_voice.grid(row=3, column=0, sticky='w')
        
        #Створення меню голосів програвача тексту
        self.tts_voice_option_menu = ttk.Combobox(self.frame_3,
                                    textvariable=self.tts_voice_var,
                                    state='readonly',
                                    style='NewCombobox.TCombobox',
                                    )
        
        self.tts_voice_option_menu.grid(row=4, column=0, sticky='nsew')
        self._set_voices_options()
        self._choose_default_tts_voice()
        
    def _add_engines_for_tts(self, *_):
        """Додавання рушіїв для вимови слів."""
        #Напис-позначка для рушіїв програвачів тексту
        self.tts_player_name = ttk.Label(self.frame_3,
            text=self.tts_player_name_label,
            style="NewLabel.TLabel")
        self.tts_player_name.grid(row=1, column=0, sticky='w')
        
        #Створення меню програвачів тексту
        self.tts_player_options = ['None', 'pyttsx3']
        default_player_option = self.settings['tts player'].get()
        self.tts_player_option_menu = ttk.OptionMenu(self.frame_3,
                                    self.tts_player_var,
                                    default_player_option,
                                    *self.tts_player_options,
                                    style='Optionmenu.TMenubutton')
        self.tts_player_option_menu['menu'].configure(
            background=self.bg_style['background'],
            foreground=self.bg_style['foreground'],
            activebackground=self.bg_style['activebackground'],
            activeforeground=self.bg_style['activeforeground'],
            )
        self.tts_player_option_menu.grid(row=2, column=0, sticky='nsew')
    
    def _add_transparency_scale(self, *_):
        """Додавання шкали прозорості вікон."""
        #Шкала прозорості вікон інтерфейсу
        self.transparency_scale_button_label = ttk.Label(self.frame_3,
            text=self.transparency_scale_label,
            style="NewLabel.TLabel")
        self.transparency_scale_button_label.grid(
            row=0, column=1, sticky='n')
            
        self.show_transparency_variable = ttk.Label(self.frame_3,
            textvariable=self.transparency_scale_variable,
            style="NewLabel.TLabel")
        self.show_transparency_variable.grid(
            row=1, column=1, sticky='n')
            
        self.transparency_scale_button = ttk.Scale(self.frame_3,
            from_=0.2, to=1, orient=tk.HORIZONTAL, length=300,
            variable=self.transparency_scale_variable,
            command=self._set_transparency_scale_variable,
            style="NewScale.Horizontal.TScale")
        self.transparency_scale_button.grid(
            row=2, column=1, sticky='n')
        
    def _add_button_on_off_spelling_words(self, *_):
        """Додавання кнопки ввімкнення/вимкнення вимови слів."""
        #Кнопка ввімкнення/вимкнення вимови слів
        self.sound_checkbutton = ttk.Checkbutton(self.frame_3,
            style="NewCheckbutton.TCheckbutton",
            text=self.on_off_playing_word,
            command=self._on_off_playing_word,
            variable=self.sound_checkbutton_variable)
        self.sound_checkbutton.grid(row=0, column=0, sticky='sw')
        
        
    def _ask_name_of_dict_group(self):
        """Вікно введення назви групи словників."""
        self.top_window = TopWindow()
        self.dict_group_name = tk.StringVar()
        top_frame = FrameWindow(self.top_window)
        
        entry_label = ttk.Label(top_frame,
            text=self.enter_dict_group_name_label,
            style='NewLabel.TLabel')
        entry_label.grid(row=0, column=0, sticky='we')
        
        name_entry = ttk.Entry(top_frame,
            textvariable=self.dict_group_name,
            style='SearchWord.TEntry')
        name_entry.grid(row=1, column=0, sticky='we')
        name_entry.focus_set()
        
        ok_button = ttk.Button(top_frame, text=self.OK_label,
         style='NewButton.TButton',
         command=self._add_dictionary_group)
        ok_button.grid(row=2, column=0, sticky='w')
        
        name_entry.bind('<Return>', self._add_dictionary_group)
        
        cancel_button = ttk.Button(top_frame, text=self.cancel_label,
         style='NewButton.TButton', command=self.top_window.withdraw)
        cancel_button.grid(row=2, column=0, sticky='e')
        
        
    def _add_dictionary_group(self, *_):
        """Додавання нової групи словників."""
        dict_group_name = self.dict_group_name.get()
        new_dict_group = dict()
        if self.settings['dict groups'].get() != '':
            old_dict_groups = ast.literal_eval(
                self.settings['dict groups'].get()
                )
        else:
            old_dict_groups = dict()
            
        if dict_group_name != '' and (
            dict_group_name not in old_dict_groups.keys()):
            self._draw_dictionary_group_window(dict_group_name)
            self.top_window.withdraw()
            old_dict_groups[dict_group_name] = []
            self.settings['dict groups'].set(old_dict_groups)
            
    def _draw_dictionary_group_window(self, dict_group_name):
        """Малювання віджета для відображення групи словників."""
        #Малювання загальної рамки для групи словників.
        group_frame_1 = FrameWindow(self.dict_group_list)
        
        self.dict_group_list.add(group_frame_1,
                text=dict_group_name)
        
        yScroll_f1 = ttk.Scrollbar(group_frame_1,
            orient=tk.VERTICAL, style="Yscroll.Vertical.TScrollbar")
        xScroll_f1 = ttk.Scrollbar(group_frame_1,
            orient=tk.HORIZONTAL, style="Xscroll.Horizontal.TScrollbar")
        
        self.dict_lists[dict_group_name] = tk.Listbox(group_frame_1,
                selectbackground=self.bg_style['activebackground'],
                yscrollcommand=yScroll_f1.set,
                xscrollcommand=xScroll_f1.set,
                selectmode=tk.MULTIPLE,
                width=25
                )
        yScroll_f1['command'] = \
                self.dict_lists[dict_group_name].yview
        xScroll_f1['command'] = \
                self.dict_lists[dict_group_name].xview
        yScroll_f1.grid(row=0, column=1, sticky='ns')
        xScroll_f1.grid(row=1, column=0, sticky='we')
        self.dict_lists[dict_group_name].grid(
                row=0, column=0, sticky="nsew")
                
        #Заповнення словниками окремої групи словників.
        all_active_dicts = self.total_dict_list.get(0, tk.END)
        if self.settings['dict groups'].get() != '':
            dict_groups = ast.literal_eval(
                self.settings['dict groups'].get())
            if dict_group_name not in dict_groups.keys():
                dict_groups[dict_group_name] = ''
        else:
            dict_groups = dict()
            dict_groups[dict_group_name] = ''
        
        if dict_groups[dict_group_name] != '':
            for dic in dict_groups[dict_group_name]:
                if dic in all_active_dicts:
                    self.dict_lists[dict_group_name].insert(tk.END, dic)
                
    def _add_dict_to_a_group(self):
        """Додавання словника до певної групи словників."""
        if self.dict_group_list.tabs():
            dict_groups = ast.literal_eval(
                self.settings['dict groups'].get())
            selected_dicts = self.total_dict_list.curselection()
            if selected_dicts:
                for i in selected_dicts:
                    current_tab = self.dict_group_list.tab(
                        self.dict_group_list.select(), "text")
                    selected_dict = self.total_dict_list.get(i)
                    if selected_dict not in \
                        self.dict_lists[current_tab].get(0, tk.END):
                        self.dict_lists[current_tab].insert(0,
                                                        selected_dict)
                        dict_groups[current_tab].append(selected_dict)
                        self.settings['dict groups'].set(dict_groups)
                        
    def _delete_dict_from_a_group(self):
        """Видалення словника з певної групи словників."""
        if self.dict_group_list.tabs():
            current_tab = self.dict_group_list.tab(
                        self.dict_group_list.select(), "text")
            selected_dicts = self.dict_lists[current_tab].curselection()
        if self.dict_lists and selected_dicts:
            self.dict_lists[current_tab].delete(selected_dicts)
            
            dict_groups = ast.literal_eval(
            self.settings['dict groups'].get())
            dict_groups[current_tab] = list(
                self.dict_lists[current_tab].get(0, tk.END))
            self.settings['dict groups'].set(dict_groups)
            
    def _delete_dict_from_all_groups(self):
        """Видалення словника з усіх груп словників."""
        all_active_dicts = self.total_dict_list.get(0, tk.END)
        locations = self.settings['location'].get()
        
        if self.dict_lists:
            if locations == '':
                dict_groups = ast.literal_eval(
                                self.settings['dict groups'].get())
                for key in self.dict_lists.keys():
                    self.dict_lists[key].delete(0, tk.END)
                    dict_groups[key] = []
                self.settings['dict groups'].set(dict_groups)
            else:
                for key in self.dict_lists.keys():
                    for index, value in enumerate(
                        self.dict_lists[key].get(0, tk.END)):
                        if value not in all_active_dicts:
                            self.dict_lists[key].delete(index)
                            dict_groups = ast.literal_eval(
                                self.settings['dict groups'].get())
                            dict_groups[key] = list(
                                self.dict_lists[key].get(0, tk.END))
                            self.settings['dict groups'].set(
                                dict_groups)
            
    def _delete_selected_dictionary_group(self):
        """Видалення обраної групи словників."""
        if self.dict_group_list.tabs():
            current_tab = self.dict_group_list.tab(
                        self.dict_group_list.select(), "text")
            self.dict_group_list.forget(self.dict_group_list.select())
            dict_groups = ast.literal_eval(
                self.settings['dict groups'].get())
            del dict_groups[current_tab]
            self.settings['dict groups'].set(dict_groups)
            
    def _delete_all_dictionary_groups(self):
        """Видалення всіх груп словників."""
        while self.dict_group_list.tabs():
            current_tab = self.dict_group_list.tab(
                        self.dict_group_list.select(), "text")
            self.dict_group_list.forget(self.dict_group_list.select())
            dict_groups = ast.literal_eval(
                self.settings['dict groups'].get())
            del dict_groups[current_tab]
        self.settings['dict groups'].set(dict())
        
    def _open_dictionary_directory(self, *_):
        """Відкрити місце розташування на диску."""
        initdir = self.settings['initial dir'].get()
        filepath = filedialog.askdirectory(
            parent=self.top,
            initialdir=initdir,
            title=self.choose_dict_loc_label
            )
        if filepath and filepath not in self.locations.get(0, 'end'):
            self.settings['initial dir'].set(filepath)
            self.locations.insert(0, filepath)
            dirpaths = ''
            dicpaths = self.locations.get(0, tk.END)
            for dicpath in dicpaths:
                dirpaths += dicpath + '\n'
               
            self.settings['location'].set(dirpaths)
            self._set_active_dictionary_list()
            dict_groups = self.settings['dict groups'].get()
            self.settings['dict groups'].set(dict_groups)
        
    def _delete_dictionary_directory(self, *_):
        """Видалення непотрібного місця розташування словників."""
        index = self.locations.curselection()
        if index:
            self.locations.delete(index)
            self.total_dict_list.delete(index)
            dirpaths = ''
            dicpaths = self.locations.get(0, tk.END)
            for dicpath in dicpaths:
                dirpaths += dicpath + '\n'
            self.settings['location'].set(dirpaths)
            self._set_active_dictionary_list()
            self._delete_dict_from_all_groups()
            dict_groups = self.settings['dict groups'].get()
            self.settings['dict groups'].set(dict_groups)
        
    def _delete_all_dictionary_directories(self, *_):
        """Видалення всіх шляхів до словників."""
        if self.locations.get(0) != '':
            self.locations.delete(0, tk.END)
            self.settings['location'].set('')
            self._set_active_dictionary_list()
            self._delete_dict_from_all_groups()
            dict_groups = self.settings['dict groups'].get()
            self.settings['dict groups'].set(dict_groups)
                    
    def _select_location(self, event):
        """Вибір шляху до словника."""
        self.locations.focus_set()
        if (event.keysym == 'Down') or (event.keysym == 'Up'):
            self.locations.select_set(0)
            self.locations.event_generate('<<ListboxSelect>>')
                
    def _set_dictionary_location(self, *_):
        """Установлення місць розміщення словників."""
        dictionaries = self.settings['location'].get()
        for dictionary in dictionaries.splitlines():
            self.locations.insert(0, dictionary)
            
    def _set_active_dictionary_list(self, *_):
        """Завантаження переліку наявних словників."""
        active_dicts = self.settings['active dicts'].get()
        all_active_dicts = self.total_dict_list.get(0, tk.END)
        if active_dicts == '':
            self.total_dict_list.delete(0, tk.END)
        else:
            for active_dict in active_dicts.splitlines():
                if active_dict not in all_active_dicts:
                    self.total_dict_list.insert(0, active_dict)
                    
    def _set_dictionary_groups(self):
        """Завантаження збережених груп словників."""
        if self.settings['dict groups'].get() != '':
            dict_groups = ast.literal_eval(
                self.settings['dict groups'].get()
                )
            for i in dict_groups.keys():
                self._draw_dictionary_group_window(i)
            
    def _cleaning_search_history(self, *_):
        """Очищення історії пошуку слів."""
        self.settings['history'].set('')
        
    def _show_history(self, *_):
        """Показати чи приховати історію пошуку слів."""
        self.settings['show_history'].set(self.on_off.get())
        
    def _on_off_playing_word(self):
        """Вмикання/вимикання програвання слів."""
        self.settings['sound variable'].set(
            self.sound_checkbutton_variable.get())
    
    def _set_transparency_scale_variable(self, *_):
        """Встановлення значення прозорості вікон."""
        trans_var = f"{self.transparency_scale_variable.get():0.2f}"
        self.transparency_scale_variable.set(trans_var)
        self.top.wm_attributes('-alpha', trans_var)
        self.settings['transparency scale'].set(trans_var)
        
    def _set_voices_options(self, *_):
        """Встановлення переліку доступних голосів
        для читання тексту."""
        self.tts_voice_option_menu = ttk.Combobox(self.frame_3,
                                textvariable=self.tts_voice_var,
                                state='readonly',
                                style='NewCombobox.TCombobox',
                                )
        self.tts_voice_option_menu.grid(row=4, column=0, sticky='nsew')
        
        if self.settings['tts player'].get() != "None":
            if self.settings['tts player'].get() == 'pyttsx3':
                import pyttsx3
                engine = pyttsx3.init()
                voices = engine.getProperty('voices')
                for voice in voices:
                    engine.setProperty('voice', voice.id)
                    if voice.id not in self.tts_voice_options:
                        self.tts_voice_options.append(voice.id.lower())
                engine.runAndWait()
                self.tts_voice_options.sort()
        else:
            self.tts_voice_options = ["None"]
            self.tts_voice_option_menu.set(self.tts_voice_options[0])
                
        self.tts_voice_option_menu.configure(
                    values=self.tts_voice_options)
        
    def _choose_default_tts_voice(self):
        """Встановлення поточного голосу для програвача тексту."""
        default_voice_option = self.settings['tts voice'].get()
        if default_voice_option != "None":
            for index, voice in enumerate(self.tts_voice_options):
                if voice == default_voice_option:
                    self.tts_voice_option_menu.current(index)
        else:
            self.tts_voice_option_menu.set(default_voice_option)
            
    def _set_tracing_variables(self, *_):
        """Встановлення відстежуваних змінних."""
        self.tts_player_var.trace_add(
            'write', self._set_voices_options)
            
    def _show_about(self):
        """Показати інформацію про програму."""
        self.top_about = TopWindow()
        
        label = ttk.Label(self.top_about, text="Movar",
                    style="NewLabel.TLabel")
        frame_about = ttk.LabelFrame(self.top_about,
            labelwidget=label, labelanchor='n',
            style='NewLabelFrame.TLabelframe',
            )
        frame_about.grid(sticky='nsew')
        
        tk.Grid.rowconfigure(frame_about, 0, weight=1)
        tk.Grid.columnconfigure(frame_about, 0, weight=1)
        
        self.text_about = tk.Text(frame_about, 
            selectbackground=self.bg_style['activebackground'],
            selectforeground=self.bg_style['activeforeground'],
            wrap=tk.WORD,
            )
        self.text_about.tag_configure("center", justify="center")
         
        self.text_about.tag_configure("hlink",
            foreground='blue', underline=1,)
        self.text_about.tag_bind("hlink",
            "<ButtonRelease-1>", self._text_about_hyperlink)
        self.text_about.tag_bind("hlink",
            "<Enter>", self._show_cursor_hand)
        self.text_about.tag_bind("hlink",
            "<Leave>", self._hide_cursor_hand)
        
        flaticon = "Flaticon."   
         
        self.text_about.insert('end', self.menu_about_text)
        self.text_about.insert('end', flaticon, "hlink")
        self.text_about.tag_add("center", 1.0, 'end')
        self.text_about.configure(state='disabled')
        self.text_about.grid(row=0, column=0, sticky='nsew')
        
        ok_button = ttk.Button(frame_about,
            text=self.OK_label,
            style='NewButton.TButton',
            command=self._close_show_about,
            
            )
        ok_button.grid(row=1, column=0, sticky='n')
        
    def _close_show_about(self):
        """Закрити вікно "Про програму"."""
        self.top_about.withdraw()
    
    def _text_about_hyperlink(self, event):
        """Обробка гіперпосилання з меню "Про програму"."""
        word_hlink = {"Flaticon.": "https://www.flaticon.com/"\
        "free-icon/dictionary_7793703?term="\
        "dictionary&page=3&position=77&origin=tag&related_id=7793703"}
        tags = dict()
        for tag in self.text_about.tag_names():
            if tag[0:5] == 'hlink':
                tag_start = self.text_about.index(tag + '.first')
                tag_end = self.text_about.index(tag + '.last')
                tags[tag] = (tag_start, tag_end)
        cursor_pos = self.text_about.index(tk.INSERT)
        for key in tags.keys():
            if float(cursor_pos) >= float(tags[key][0]) and \
            float(cursor_pos) <= float(tags[key][1]) :
                linked_word = self.text_about.get(tags[key][0],
                    tags[key][1])
            if linked_word in word_hlink.keys():
               webbrowser.open_new(word_hlink[linked_word]) 
        
    def _show_cursor_hand(self, *_):
        """Показати курсор "Рука1"."""
        self.text_about.configure(cursor="hand1")
        
    def _hide_cursor_hand(self, *_):
        """Приховати курсор "Рука1"."""
        self.text_about.configure(cursor="")
        
    def _show_manual_text(self):
        """Показати текст посібника з Допомоги."""
        self.top_manual = TopWindow()
        
        label = ttk.Label(self.top_manual, text=self.manual_label,
                    style="NewLabel.TLabel")
        frame_manual = ttk.LabelFrame(self.top_manual,
            labelwidget=label, labelanchor='n',
            style='NewLabelFrame.TLabelframe',
            )
        frame_manual.grid(sticky='nsew')
        
        tk.Grid.rowconfigure(frame_manual, 0, weight=1)
        tk.Grid.columnconfigure(frame_manual, 0, weight=1)
        
        self.text_about = tk.Text(frame_manual, 
            selectbackground=self.bg_style['activebackground'],
            selectforeground=self.bg_style['activeforeground'],
            wrap=tk.WORD,
            )
        self.text_about.tag_configure("center", justify="center")
         
        self.text_about.insert('end', self.manual_text)
        self.text_about.tag_add("center", 1.0, 'end')
        self.text_about.configure(state='disabled')
        self.text_about.grid(row=0, column=0, sticky='nsew')
        
        ok_button = ttk.Button(frame_manual,
            text=self.OK_label,
            style='NewButton.TButton',
            command=self._close_show_manual_text,
            
            )
        ok_button.grid(row=1, column=0, sticky='n')
        
    def _close_show_manual_text(self):
        """Закрити вікно з посібником."""
        self.top_manual.withdraw()
        
        
                
class WindowsMainMenu(GenericMenu):
    """Клас для головного меню Windows."""
    
    def __init__(self, *args, **kwargs):
        """Attributes initialization."""
        try:
            del(self.keybinds['<Control-q>'])
        except:
            pass
        super().__init__(*args, **kwargs)
        
    def _add_quit_menu(self, menu):
        """Додавання функції 'Вихід' до головного меню."""
        menu.add_command(
            label=self.add_quit_menu_label,
            command=self._event('<<FileQuit>>'),
            )
            
class LinuxMainMenu(GenericMenu):
    """Клас для головного меню Linux."""
    
            
def get_main_menu_for_os(os_name):
    """Getting main menu for certain OS."""
    menus = {
        'Linux': LinuxMainMenu,
        'freebsd7': LinuxMainMenu,
        'Windows': WindowsMainMenu
        }
    return menus.get(os_name, GenericMenu)
        
        
            
        

        
