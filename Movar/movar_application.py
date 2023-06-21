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


import tkinter as tk
from tkinter import ttk, scrolledtext, font, messagebox
from .movar_widgets import GenericMenu, TopWindow, FrameWindow
from .movar_models import SettingsModel, TextSearch
from .movar_views import ColorStyles
from .movar_widgets import get_main_menu_for_os
from .movar_language_support import InterfaceLanguage
import platform, ast, time, re
from queue import Queue

class Application(tk.Tk):
    """Головне вікно програми Movar."""
    
    def __init__(self, *args, **kwargs):
        """Ініціалізація атрибутів."""
        super().__init__(*args, **kwargs)
        #Конфігурація головного вікна
        self.geometry('800x600')
        self.title("Movar")
        self.resizable(True, True)
        self.configure(bg='black')
        self.queue = Queue()
        self.settings_model = SettingsModel()
        self.language_options = InterfaceLanguage().translation_options
        self._load_settings()
        self.wait_visibility()
        self._set_transparency_value()
        
        #Завантаження кольорових стилів оформлення
        self._download_color_styles()
        
        #Конфігурація стовпця й рядка
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        self.word = tk.StringVar()
        
        #Завантаження словників та префіксного дерева
        self._download_dictionaries_and_index_tree()
        
        #Створення головного меню
        self.menu_class = get_main_menu_for_os(platform.system())
        self.menu = self.menu_class(
            self, self.settings, self.total_dict)
        self.configure(menu=self.menu)
        
        self.tts_player_value = self.menu.tts_player_var
        self.tts_voice_value = self.menu.tts_voice_var
        self.font_family_value = self.menu.font_family_var
        
        self._add_interface_labels()
        
        self._create_interface_main_window_widgets()
        
        self._set_history()
        
        self._show_history()
        
        self._check_if_tts_is_on()
            
        self.event_callbacks = {
            '<<FileQuit>>': lambda _:self.quit(),
            '<<DictSettings>>':
                lambda _:self.menu._dictionaries_settings_window()
            }
            
        self._binding_events()
        
        self.word_entry.focus()
        
        self._creat_right_mouse_button_menu()
        
        self._tracing_variables()
        
    def _download_color_styles(self):
        """Завантаження кольорових схем."""
        self.color_styles = ColorStyles(self, self.settings)
        self.bg_style = self.color_styles.styles[self.color_styles.n]
        self.option_add('*TCombobox*Listbox.background',
            self.bg_style['activebackground'])
        self.option_add('*TCombobox*Listbox.foreground',
            self.bg_style['activeforeground'])
        self.option_add('*TCombobox*Listbox.selectBackground',
            self.bg_style['background'])
        self.option_add('*TCombobox*Listbox.selectForeground',
            self.bg_style['foreground'])
        
    def _create_interface_main_window_widgets(self):
        """Створення віджетів для головного вікна."""
        #Додавання першої рамки для пошуку слова та місця вводу слова
        self.search_frame = FrameWindow(self)
        self.search_frame.columnconfigure(100, weight=100)
        
        #Створення напису для пошуку слова
        self.search_label = ttk.Label(self.search_frame,
            text=self.word_search_label, style='NewLabel.TLabel')
        self.search_label.grid(row=0, column=1, sticky='e')
        
        #Створення місця вводу слова для пошуку
        self.word_entry = ttk.Entry(
            self.search_frame,
            textvariable=self.word,
            style='SearchWord.TEntry'
            )
        self.word_entry.grid(row=0, column=2, sticky='we')
           
        #Створення кнопки програвання слова
        self.play_word_button = ttk.Button(self.search_frame,
            text=self.play_word_button_label,
            style='NewButton.TButton',
            command=self._play_word,
            )
        self.play_word_button.grid(row=0, column=3, sticky='we')
        
        #Створення меню-переліка груп словників для пошуку
        self.dict_main_var = tk.StringVar()
        if self.settings['default dict group'].get() != '':
            default_option = self.settings['default dict group'].get()
        else:
            default_option = self.dict_groups_options[0]
        
        self.dicts_option_menu = ttk.OptionMenu(self.search_frame,
                                    self.dict_main_var,
                                    default_option,
                                    *self.dict_groups_options,
                                    style='Optionmenu.TMenubutton')
        self.dicts_option_menu['menu'].configure(
            background=self.bg_style['background'],
            foreground=self.bg_style['foreground'],
            activebackground=self.bg_style['activebackground'],
            activeforeground=self.bg_style['activeforeground'],
            )
        self.dicts_option_menu.grid(row=0, column=0, sticky='w')
        
        self._choose_dictionaries_groups_for_search()
        
        #Створення горішнього вікна Toplevel для розміщення Listbox
        self.top_window = self._add_toplevel_window()
        self.top_window.transient(self.word_entry)
        
        self.yScroll = ttk.Scrollbar(self.top_window,
            orient=tk.VERTICAL, style="Yscroll.Vertical.TScrollbar")
            
        self.listbox_menu = tk.Listbox(
            self.top_window,
            selectbackground=self.bg_style['activebackground'],
            yscrollcommand=self.yScroll.set)
            
        self.yScroll['command'] = self.listbox_menu.yview
        
        #Додавання другої рамки для виведення результатів
        #та історії пошуку.
        self.result_window = FrameWindow(self)
        
        self.pw = ttk.PanedWindow(
            self.result_window, orient=tk.HORIZONTAL,
            style="SearchResults.TPanedwindow",
            )
        self.pw.grid(row=0, column=0, sticky='nsew')
            
        self.search_results = tk.scrolledtext.ScrolledText(
            self.pw,
            background=self.bg_style['foreground'],
            state='disabled',
            )
        self.search_results.vbar.configure(
            troughcolor=self.bg_style['foreground'], 
            bg=self.bg_style['background'],
            activebackground=self.bg_style['activebackground'],
            borderwidth=5
                )
            
        self.pw.add(self.search_results)
        
        self.search_history = tk.Listbox(
            self.pw,
            selectbackground=self.bg_style['activebackground'],
            )
            
    def _creat_right_mouse_button_menu(self):
        """Створення меню для правої кнопки миші."""
        self.right_mouse_menu = tk.Menu(self,
            tearoff=False, **self.bg_style)
        self.right_mouse_menu.add_command(
            label=self.copy_label, command=self._menu_popup_copy)
        self.right_mouse_menu.add_command(
            label=self.paste_label, command=self._menu_popup_paste)
        self.right_mouse_menu.add_separator()
        self.right_mouse_menu.add_command(label=self.close_menu_label,
            command=self._close_right_mouse_menu)
        
    def _add_interface_labels(self):
        """Додавання мовної підтримки написів інтерфейсу."""
        translations = self.language_options
        selected_language = self.settings['language'].get()
        self.word_search_label = \
            translations[selected_language]['Word search'] + '>>'
        self.copy_label = translations[selected_language]['Copy']
        self.paste_label = translations[selected_language]['Paste']
        self.close_menu_label = \
            translations[selected_language]['Close menu']
        self.play_word_button_label = \
            translations[selected_language]['Play word']
        
    def _show_progress_bar(self):
        """Зображення лінії прогресу під час виконання завантаження."""
        translations = self.language_options
        selected_language = self.settings['language'].get()
        pb_text = \
            translations[selected_language]['Processing dictionaries']
        self.color_styles.configure("LabeledProgressbar", text=pb_text)
        self.top_bar = tk.Toplevel()
        self.top_bar.configure(background =\
            self.bg_style['activebackground'])
        
        self.progr_bar = ttk.Progressbar(self.top_bar,
            mode='indeterminate',
            length=500,
            orient=tk.HORIZONTAL,
            style="LabeledProgressbar"
            )
        self.progr_bar.grid(row=0, sticky='we')
        self.progr_bar.start()
        self.wait_visibility(self.top_bar)
        while self.queue.empty():
            self.progr_bar['value'] += 20
            self.top_bar.update_idletasks()
            time.sleep(0.25)
            
    def _download_dictionaries_and_index_tree(self, *_):
        """Завантаження словників."""
        #Завантаження словників
        self._save_settings()
        searcher = TextSearch(self.queue)
        searcher.start()
        self._show_progress_bar()
        self.total_dict = searcher.total_dict
        
        #Завантаження префіксного дерева
        self.index_search = dict()
        self.selected_index = dict()
        for key in self.total_dict.keys():
            if self.total_dict[key].get('Indexes'):
                self.index_search[key] = self.total_dict[key]['Indexes']

        if self.total_dict:
            total_list = ""
            for key in self.total_dict.keys():
                lang_pair = self.total_dict[key]['Language pair']
                total_list += key + f'({lang_pair})\n'
            self.settings['active dicts'].set(total_list)
        else:
            self.settings['active dicts'].set('')
        
        self.selected_index = self.index_search
        
        self.queue.get()
        self.progr_bar.stop()
        self.top_bar.withdraw()
            
    def _choose_dictionaries_groups_for_search(self, *_):
        """Встановлення поточної групи словників."""
        self.menu.total_dict = self.total_dict
        if self.dict_main_var.get() not in self.dict_groups_options:
            self.dict_main_var.set(self.dict_groups_options[0])
        dict_group_name = self.dict_main_var.get()
        dict_list = self.dict_groups_options
        if self.settings['dict groups'].get():
            dict_groups = ast.literal_eval(
                self.settings['dict groups'].get())
            self.selected_index = dict()
            if dict_group_name == dict_list[0]:
                self.selected_index = self.index_search
            else:
                for dic in dict_groups[dict_group_name]:
                    dic = dic.split("(")[0]
                    self.selected_index[dic] = self.index_search[dic]
            self.settings['default dict group'].set(dict_group_name)

    def _on_style_change(self, *_):
        """Зміна кольорового стилю оформлення."""
        self._download_color_styles()
        self.menu_class = get_main_menu_for_os(platform.system())
        self.menu = self.menu_class(
            self, self.settings, self.total_dict)
        self.configure(menu=self.menu)
        
        self.dicts_option_menu['menu'].configure(
            background=self.bg_style['background'],
            foreground=self.bg_style['foreground'],
            activebackground=self.bg_style['activebackground'],
            activeforeground=self.bg_style['activeforeground'],
            )
        self.listbox_menu.config(
            selectbackground=self.bg_style['activebackground']
            )
        self.search_results.configure(
            background=self.bg_style['foreground'])
        self.search_results.vbar.configure(
            troughcolor = self.bg_style['activeforeground'], 
            bg = self.bg_style['activebackground'],
                )
            
    def _on_theme_change(self, *_):
        """Попередження про те, коли змінюється тема."""
        theme = self.settings['theme'].get()
        self._download_color_styles()
        
        self.color_styles.theme_use(theme)
        
        self.menu_class = get_main_menu_for_os(platform.system())
        self.menu = self.menu_class(
            self, self.settings, self.total_dict)
        self.configure(menu=self.menu)
    
    def _on_language_change(self, *_):
        """Попередження щодо необхідності перезавантаження
        при зміни мови інтерфейсу."""
        self._download_dictionary_groups_for_choosing_from()
        
        language = self.settings['language'].get()
        title = self.language_options[language]\
        ['Title interface messagebox']
        message = self.language_options[language]\
        ['Message interface messagebox']
        messagebox.showwarning(title, message)
        
    def _display_popup_menu(self, event):
        """Показує контекстне меню при натисканні правої кнопки миші."""
        self.right_mouse_menu.post(event.x_root, event.y_root)

    def _menu_popup_copy(self):
        """Копіювання виділеного тексту."""
        self.focus_get().event_generate("<<Copy>>")

    def _menu_popup_paste(self):
        """Вставка скопійованого тексту."""
        self.word_entry.event_generate("<<Paste>>")
        
    def _close_right_mouse_menu(self):
        """Закриття контекстного меню."""
        self.right_mouse_menu.unpost()
        
    def _add_toplevel_window(self):
        """Створення додаткового вікна Toplevel."""
        top = TopWindow()
        top.transient(self.word_entry)
        top.withdraw()
        return top
        
    def _binding_events(self, *_):
        """Функція зі зв'язаними подіями."""
        self.word_entry.bind('<KeyRelease>', self._key_press)
        self.word_entry.bind('<Down>', self._listbox_focus)
        self.word_entry.bind('<Return>', self._text_widget_insert)
        
        self.listbox_menu.bind('<KeyPress>', self._entry_focus)
        self.listbox_menu.bind('<ButtonRelease-1>', self._listbox_focus)
        self.listbox_menu.bind('<Return>', self._listbox_focus)
        
        self.search_history.bind("<ButtonRelease-1>",
            self._history_listbox_selection)
        
        for sequence, callback in self.event_callbacks.items():
            self.bind(sequence, callback)
            
        self.bind_all("<ButtonPress-3>", self._display_popup_menu)
        self.bind_all("<Control-KeyPress-1>",
            self._change_dict_group_key_up)
        self.bind_all("<Control-KeyPress-2>",
            self._change_dict_group_key_down)
        
        self.search_results.bind('<KeyPress>', self._entry_focus)
        
        self.bind("<Configure>", self._hide_toplevel_window)
        
        self.bind("<FocusOut>", self._hide_toplevel_window)
        
        self.pw.bind("<Configure>", self._set_resized_window_config)
        
    def _change_dict_group_key_up(self, *_):
        """Гортання груп словників угору."""
        options = self.dict_groups_options
        opt_length = len(self.dict_groups_options)
        if opt_length > 1:
            cur_pos = options.index(self.dict_main_var.get())
            cur_neg_ind = cur_pos - opt_length
            cur_neg_ind -= 1
            if cur_neg_ind >= -opt_length:
                self.dict_main_var.set(options[cur_neg_ind])
            else:
                self.dict_main_var.set(options[-1])
                
    def _change_dict_group_key_down(self, *_):
        """Гортання груп словників угору."""
        options = self.dict_groups_options
        opt_length = len(self.dict_groups_options)
        if opt_length > 1:
            cur_pos = options.index(self.dict_main_var.get())
            cur_pos += 1
            if cur_pos < opt_length:
                self.dict_main_var.set(options[cur_pos])
            else:
                self.dict_main_var.set(options[0])
    
    def _tracing_variables(self, *_):
        """Відстежувані змінні в налаштуваннях."""
        self.settings['theme'].trace_add(
            'write', self._on_theme_change)
        self.settings['style'].trace_add(
            'write', self._on_style_change)
        self.settings['history'].trace_add(
            'write', self._delete_history)
        self.settings['show_history'].trace_add(
            'write', self._show_history)
        self.settings['location'].trace_add(
            'write', self._download_dictionaries_and_index_tree)
        self.settings['dict groups'].trace_add(
            'write', self._download_dictionary_groups_for_choosing_from)
        self.settings['language'].trace_add(
            'write', self._on_language_change)
        self.settings['transparency scale'].trace_add(
            'write', self._set_transparency_value)
        self.settings['sound variable'].trace_add(
            'write', self._check_if_tts_is_on)
        self.tts_player_value.trace_add(
            'write', self._set_default_tts_player)
        self.tts_voice_value.trace_add(
            'write', self._set_default_tts_voice)
        self.dict_main_var.trace_add(
            'write', self._choose_dictionaries_groups_for_search)
        self.font_family_value.trace_add(
            'write', self._set_default_font_family)
        
    def _hide_toplevel_window(self, event):
        """Приховування горішнього вікна Toplevel."""
        if not self.listbox_menu.curselection():
            self.top_window.withdraw()
            self._close_right_mouse_menu()
        else:
            self._listbox_focus(event)
        
    def _load_settings(self):
        """Завантаження налаштувань до словника self.settings."""
        vartypes = {
            'bool': tk.BooleanVar,
            'str': tk.StringVar,
            'int': tk.IntVar,
            'float': tk.DoubleVar
            }
        self.settings = dict()
        for key, data in self.settings_model.fields.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.settings[key] = vartype(value=data['value'])
        
        for var in self.settings.values():
            var.trace_add('write', self._save_settings)
            
        self._set_font()
        self.settings['font size'].trace_add('write', self._set_font)
        self.settings['font family'].trace_add('write', self._set_font)
        
        self._set_style()
        self.settings['style'].trace_add('write', self._set_style)
        
        style = ttk.Style()
        theme = self.settings.get('theme').get()
        if theme in style.theme_names():
            style.theme_use(theme)
        
        translations = self.language_options
        selected_language = self.settings['language'].get()
        all_dict_label = \
            translations[selected_language]['All dictionaries']
        
        self.dict_groups_options = [all_dict_label]
        
        if self.settings['dict groups'].get() != "":    
            dict_groups = ast.literal_eval(
                self.settings['dict groups'].get())  
            for dict_group in dict_groups.keys():
                self.dict_groups_options.append(dict_group)
        
    def _download_dictionary_groups_for_choosing_from(self, *_):
        """Завантаження переліку групи словників для віджета."""
        translations = self.language_options
        selected_language = self.settings['language'].get()
        all_dict_label = \
            translations[selected_language]['All dictionaries']
            
        self.dict_groups_options = [all_dict_label]
        if self.settings['dict groups'].get() != '':
            dict_groups = ast.literal_eval(
                self.settings['dict groups'].get())  
        
            for dict_group in dict_groups.keys():
                self.dict_groups_options.append(dict_group)
        
        self.dicts_option_menu["menu"].delete(0, tk.END)
        for choice in self.dict_groups_options:
            self.dicts_option_menu["menu"].add_command(
                label=choice, command=tk._setit(
                    self.dict_main_var, choice))
                    
        self._choose_dictionaries_groups_for_search()
        
    def _save_settings(self, *_):
        """Збереження налаштувань."""
        for key, variable in self.settings.items():
            self.settings_model.set(key, variable.get())
        self.settings_model.save()
            
    def _set_font(self, *_):
        """Установлення шрифту додатка."""
        font_size = self.settings['font size'].get()
        font_family = self.settings['font family'].get()
        font_names = (
            'TkDefaultFont', 'TkMenuFont', 'TkTextFont', 'TkFixedFont'
            )
        for font_name in font_names:
            tk_font = font.nametofont(font_name)
            tk_font.config(size=font_size, family=font_family)
            
    def _set_default_font_family(self, *_):
        """Встановлення поточної родини шрифтів."""
        self.settings['font family'].set(self.font_family_value.get())
            
    def _set_style(self, *_):
        """Установлення стилю інтерфейса."""
        ColorStyles.n = self.settings['style'].get()
        
    def _set_history(self, *_):
        """Установлення історії пошуку слів."""
        history = self.settings['history'].get().strip('\n')
        history_list = list(history.split('\n'))
        if history_list != '':
            for line in history_list:
                self.search_history.insert(0, line)
                
    def _set_resized_window_config(self, *_):
        """Налаштування вікон при зміни розміру головного вікна."""
        if self.settings['show_history'].get() == 1:
            self.update_idletasks()
            sash_position = int(self.winfo_width() - 
                self.winfo_width() * 1/4)
            self.pw.sashpos(0, sash_position)
        if self.word.get():
            self.update_idletasks()
            self._text_widget_insert()
                
    def _delete_history(self, *_):
        """Видалення історії пошуку слів."""
        history = self.settings['history'].get()
        if len(history) == 0:
            self.search_history.delete(0, 'end')
            
    def _show_history(self, *_):
        """Показати чи сховати історію пошуку слів."""
        if self.settings['show_history'].get() == 1:
            self.pw.add(self.search_history)
            self.update_idletasks()
            sash_position = int(self.winfo_width() - 
                self.winfo_width() * 1/4)
            self.pw.sashpos(0, sash_position)
        else:
            if len(self.pw.panes()) == 2:
                self.pw.remove(self.search_history)
            
    def _set_transparency_value(self, *_):
        """Встановлення значення прозорості вікон."""
        trans_value = self.settings['transparency scale'].get()
        self.wm_attributes('-alpha', trans_value)
        
    def _set_default_tts_player(self, *_):
        """Встановлення поточного програвача текста."""
        self.settings['tts player'].set(self.tts_player_value.get())
        
    def _set_default_tts_voice(self, *_):
        """Встановлення поточного голосу програвача тексту."""
        self.settings['tts voice'].set(self.tts_voice_value.get())
        
    def _check_if_tts_is_on(self, *_):
        """Перевірка стану програвання звуків."""
        if self.settings['sound variable'].get() == 1:
            self.play_word_button['state'] = tk.NORMAL
        else:
           self.play_word_button['state'] = tk.DISABLED
           
    def _play_word(self, *_):
        """Програвання слова."""
        current_player = self.settings['tts player'].get()
        current_voice = self.settings['tts voice'].get()
        if current_player != "None" or current_voice != "None":
            if current_player == 'pyttsx3':
                import pyttsx3
                engine = pyttsx3.init()
                current_voice = self.settings['tts voice'].get()
                engine.setProperty('voice', current_voice)
                word = self.word.get()
                if word:
                    engine.say(word)
                engine.runAndWait()
            
    def _key_press(self, event):
        """Стеження за натиснутою кнопкою клавіатури."""
        key = event.widget.get()
        self.search_history.selection_clear(0, tk.END)
        if key == "":
            data = []
            self.top_window.withdraw()
        elif key != '' and event.keysym != 'Return':
            data = []
            self._listbox_search_menu_appears()
            for dic in self.selected_index.keys():
                for item in self.selected_index[dic]:
                    clean_item = re.sub(r'\W', '', item)
                    if (clean_item.lower().startswith(key.lower()) \
                    or item.lower().startswith(key.lower())) \
                    and item not in data:
                        self.yScroll.grid(row=1, column=1,
                            sticky='ns')
                        self.listbox_menu.grid(row=1, column=0,
                            sticky="we")
                        data.append(item)
            self._listbox_search_words_update(data)
    
    def _listbox_search_words_update(self, data):
        """Оновлення слів у Listbox_menu"""
        self.listbox_menu.delete(0, 'end')
        data = sorted(data, key=lambda x: re.sub(r'\W', '', x))
        for item in data:
            self.listbox_menu.insert('end', item)
        
    def _listbox_focus(self, event):
        """Вибір слова у випадному меню під пошуком слова"""
        self.listbox_menu.focus_set()
        if (event.keysym == 'Down') or (event.keysym == 'Up'):
            self.listbox_menu.select_set(0)
            self.listbox_menu.event_generate('<<ListboxSelect>>')
        elif (event.num == 1) or (event.keysym == 'Return'):
            if self.listbox_menu.curselection():
                found_word = self.listbox_menu.get(
                    self.listbox_menu.curselection())
                self._entry_insert_text(found_word)
                self._text_widget_insert()
                
    def _listbox_search_menu_appears(self, *_):
        """Створення вікна для випадного меню пошуку."""
        z = self.word_entry.winfo_width()
        x = self.word_entry.winfo_rootx()
        y = self.pw.winfo_rooty() - 30
            
        self.top_window.overrideredirect(True)
        self.top_window.geometry("%dx240+%d+%d"%(z,x,y))
        self.top_window.deiconify()
        
    def _entry_focus(self, event):
        """Керування введенням і редагуванням слів у пошуку."""
        if event.keysym != 'Down' and event.keysym != 'Up':
            if len(event.keysym) == 1 :
                text = self.word.get() + event.keysym
                self._entry_insert_text(text)
                
    def _entry_insert_text(self, text):
        """Вставка тексту в поле пошуку слова."""
        self.word_entry.delete(0, 'end')
        self.word_entry.insert(0, text)
        self.word_entry.focus_set()
        
    def _history_listbox_selection(self, *_):
        """Вибір слова з історії пошуку."""
        if self.search_history.curselection():
            found_word = (self.search_history.get(
                self.search_history.curselection()))
            self._entry_insert_text(found_word) 
            self._text_widget_insert()
        
    def _text_widget_insert(self, *_):
        """Вивід результатів пошуку слова."""
        translations = self.language_options
        selected_language = self.settings['language'].get()
        no_word_label = translations[selected_language]['No word']
        all_dictionaries = \
            translations[selected_language]['All dictionaries']
        
        self.search_results.configure(state='normal')
        self.search_results.delete('1.0', 'end')
        self.search_results.configure(state='disabled')
        
        sel_dict_set = dict()
        dict_group_name = self.dict_main_var.get()
        
        if self.settings['dict groups'].get():
            dict_groups = ast.literal_eval(
                self.settings['dict groups'].get())
            if dict_group_name != all_dictionaries:
                total_list = {}
                selected_dicts = dict_groups[dict_group_name]
                for key in self.total_dict.keys():
                    lang_pair = self.total_dict[key]['Language pair']
                    total_list[key]= key + f'({lang_pair})'
                for key, dict_name in total_list.items():
                    if dict_name in selected_dicts:
                        sel_dict_set[key] = self.total_dict[key]
            else:
                sel_dict_set = self.total_dict
        else:
            sel_dict_set = self.total_dict
                    
        count = len(sel_dict_set)
        word = self.word.get().lower()
        for key in sel_dict_set.keys():
            if word in sel_dict_set[key]['Indexes']:
                start_article = sel_dict_set[key]['Indexes'][word][0]
                found_word_index = list(
                    sel_dict_set[key]['Indexes']).index(word)
                if found_word_index < \
                    (len(sel_dict_set[key]['Indexes']) - 1):
                    next_word_index = found_word_index + 1
                    end_article = sel_dict_set[key]['Indexes']\
                        [list(sel_dict_set[key]['Indexes'])\
                        [next_word_index]][0]
                else:
                    end_article = None
                
                article = sel_dict_set[key]\
                    ['Main body'][start_article:end_article]
                self._search_results_internal_frame(article, key)    
            else:
                count -= 1
                if count == 0:
                    self.search_results.configure(state='normal')
                    self.search_results.delete('1.0', 'end')
                    self.search_results.insert('1.0',
                        f"{no_word_label} «{self.word.get()}».")
                    self.search_results.configure(state='disabled')
            
        history = self.settings['history'].get().strip('\n')
        history_list = list(history.split('\n'))
        if len(history_list) < 300:
            if word not in history_list:
                self.settings['history'].set(
                        history + '\n' + word)
                self.search_history.insert(0, word)
                    
        self.top_window.withdraw()
        
    def _search_results_internal_frame(self, article, key):
        """Додавання результатів пошуку до внутрішньої рамки."""
        self.search_results.configure(state='normal')
                
        label = ttk.Label(self.search_results, text=key,
                    style="NewLabel.TLabel")
        label_frame = ttk.LabelFrame(
                    self.search_results, 
                    style='NewLabelFrame.TLabelframe',
                    labelwidget=label,
                    )
                
        self.search_results.window_create("1.0",
                    window=label_frame, pady=5, stretch=1)
        self.sep_text = tk.Text(label_frame,
                    selectbackground=self.bg_style['activebackground'],
                    selectforeground=self.bg_style['activeforeground'],
                    wrap=tk.WORD
                    )
        self.sep_text.insert("1.0", article)
        self.sep_text.configure(state='disabled')
                
        height, width = self._internal_frame_sizes(article, self.sep_text)
        self.sep_text.configure(width=width, height=height)
        self.sep_text.grid()
        
        self.search_results.configure(state='disabled')
        
    def _internal_frame_sizes(self, article, sep_text):
        """Розрахунок розмірів внутрішньої рамки."""
        current_font = self.settings['font family'].get()
        current_font_size = self.settings['font size'].get()
                
        font = tk.font.Font(family=current_font,
            size=current_font_size, weight='normal')
        char_width = font.measure("0")
               
        width = int((self.search_results.winfo_width()-50)/char_width)
        height = int(len(article)/width)
        
        text_lines = int(sep_text.index('end').split('.')[0])-1
        line_list = article.split('\n')
        line_length = [len(line) for line in line_list]
        max_line_length = max(line_length)
        
        if max_line_length > width:
            height = int(len(article)/width) + 2
        else:
            height = text_lines + 2
        
        return height, width
        
if __name__ == "__main__":
    app = Application()
    app.mainloop()
