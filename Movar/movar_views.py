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
from tkinter import ttk

class ColorStyles(ttk.Style):
    """Клас, що керує налаштуванням кольорів програми."""

    styles = [{
            'background': 'aquamarine4',
            'foreground': 'aqua',
            'activebackground': 'coral',
            'activeforeground': 'azure',
            'relief': tk.RAISED},
                        {
            'background': 'RoyalBlue',
            'foreground': 'white',
            'activebackground': 'yellow2',
            'activeforeground': 'black',
            'relief': tk.SUNKEN},
            {
            'background': 'dark violet',
            'foreground': 'aqua',
            'activebackground': 'coral',
            'activeforeground': 'azure',
            'relief': tk.GROOVE},
            {
            'background': 'dark turquoise',
            'foreground': 'maroon',
            'activebackground': 'plum',
            'activeforeground': 'dark blue',
            'relief': tk.RIDGE},
            {
            'background': 'peru',
            'foreground': 'maroon',
            'activebackground': 'plum',
            'activeforeground': 'dark blue',
            'relief': tk.RIDGE},
            {
            'background': 'blanched almond',
            'foreground': 'purple4',
            'activebackground': 'SteelBlue4',
            'activeforeground': 'ghost white',
            'relief': tk.RAISED},
            {
            'background': 'dark blue',
            'foreground': 'plum',
            'activebackground': 'SteelBlue4',
            'activeforeground': 'ghost white',
            'relief': tk.GROOVE},
            {
            'background': 'black',
            'foreground': 'white',
            'activebackground': 'white',
            'activeforeground': 'black',
            'relief': tk.GROOVE},
            {
            'background': 'white',
            'foreground': 'black',
            'activebackground': 'antique white',
            'activeforeground': 'black',
            'relief': tk.GROOVE},
            {
            'background': 'blue violet',
            'foreground': 'blanched almond',
            'activebackground': 'burlywood',
            'activeforeground': 'black',
            'relief': tk.RIDGE},
            ]
        
    def __init__(self, parent, settings, *args, **kwargs):
        """Ініціалізація атрибутів."""
        super().__init__(*args, **kwargs)
        self.settings = settings
        self.n = self.settings['style'].get()
        
        self._TEnry_config()
        self._Hor_TScrollbar_config()
        self._Optionmenu_config()
        self._Progressbar_config()
        self._TButton_config()
        self._TCheckbutton_config()
        self._TCombobox_config()
        self._TFrame_config()
        self._TLabel_config()
        self._TLabelframe_config()
        self._TNotebook_config()
        self._TPaned_window_config()
        self._TScale_config()
        self._Vert_TScrollbar_config()
        
    def _TEnry_config(self):
        """Стиль для віджета ttk.Entry."""
        
        self.configure("SearchWord.TEntry",
            selectbackground=self.styles[self.n]['background'],
            selectforeground=self.styles[self.n]['activeforeground'],
            borderwidth=5,
            padding=5,
            )
        self.map('SearchWord.TEntry', 
            fieldbackground=[('focus',
                self.styles[self.n]['activebackground']),
                ('!focus', self.styles[self.n]['background'])]
                )
            
    def _TFrame_config(self):
        """Стиль для ttk.Frame."""
        self.configure(
            "Description.TFrame",
            background=self.styles[self.n]['background'],
            relief=self.styles[self.n]['relief'],
            )
        
    def _Vert_TScrollbar_config(self):
        """Стиль для вертикального ttk.Scrollbar."""
        self.configure("Yscroll.Vertical.TScrollbar",
                    background=self.styles[self.n]['background'],
                    troughcolor=self.styles[self.n]['foreground'],
                    arrowcolor=self.styles[self.n]['activebackground'],
                    borderwidth=5,
                        )
                        
        self.map("Yscroll.Vertical.TScrollbar", 
            background=[('focus',
                self.styles[self.n]['foreground']),
                ('active', self.styles[self.n]['activebackground'])],
                )
                
    def _Hor_TScrollbar_config(self):
        """Стиль для горизонтального ttk.Scrollbar."""
        self.configure("Xscroll.Horizontal.TScrollbar",
                    background=self.styles[self.n]['background'],
                    troughcolor=self.styles[self.n]['foreground'],
                    arrowcolor=self.styles[self.n]['activebackground'],
                    borderwidth=5,
                        )
        self.map("Xscroll.Horizontal.TScrollbar", 
            background=[('focus',
                self.styles[self.n]['foreground']),
                ('active', self.styles[self.n]['activebackground'])],
                )
    
    def _TLabel_config(self):
        """Стиль для віджета ttk.Label."""
        self.configure("NewLabel.TLabel",
            background=self.styles[self.n]['background'],
            foreground=self.styles[self.n]['foreground'],
            borderwidth=10,
            )
                       
    def _TLabelframe_config(self):
        """Стиль для віджета ttk.LabelFrame."""
        self.configure('NewLabelFrame.TLabelframe', 
            background=self.styles[self.n]['activebackground'],
            foreground=self.styles[self.n]['foreground'],
            borderwidth=5,
            )
                        
    def _TButton_config(self):
        """Стиль для віджета ttk.Button."""
        self.configure("NewButton.TButton",
                        background=self.styles[self.n]['background'],
                        foreground=self.styles[self.n]['foreground'],
                        borderwidth=5,
                        )
        self.map("NewButton.TButton",
                foreground=[('pressed', 'red'),
                    ('active', self.styles[self.n]['activeforeground']),
                    ],
                background=[
                    ('active', self.styles[self.n]['activebackground']),
                    ]
                )
                
        
    def _TPaned_window_config(self):
        """Стиль для віджета ttk.Panedwindow."""                    
        self.configure("SearchResults.TPanedwindow",
                background=self.styles[self.n]['background'],
            )
        self.configure("Sash",
            background=self.styles[self.n]['foreground'],
            bordercolor=self.styles[self.n]['foreground'],
            sashrelief=self.styles[self.n]['relief'],
            handlepad=150,
            handlesize=25,
            borderwidth=5,
            sashthickness=15
            )
    
    def _TNotebook_config(self):
        """Стиль для віджета ttk.Notebook."""
        self.configure(
            "Settings.TNotebook",
            background=self.styles[self.n]['background'],
            foreground=self.styles[self.n]['foreground'],
            activebackground=self.styles[self.n]['activebackground'],
            activeforeground=self.styles[self.n]['activeforeground'],
            relief=self.styles[self.n]['relief'],
            borderwidth=5,
            )
        self.map('Settings.TNotebook.Tab', 
            background=[('selected',
                self.styles[self.n]['activebackground'])],
            foreground=[('selected',
                self.styles[self.n]['activeforeground'])],
                )
        self.configure("Settings.TNotebook.Tab",
            background=self.styles[self.n]['background'])
    
    def _Optionmenu_config(self):
        """Стиль для віджета ttk.Optionmenu."""
        self.configure("Optionmenu.TMenubutton",
            background=self.styles[self.n]['background'],
            foreground=self.styles[self.n]['foreground'],
            relief=self.styles[self.n]['relief'],
            borderwidth=5,
            )
        self.map("Optionmenu.TMenubutton",
            background=[('active',
                self.styles[self.n]['activebackground'])],
            foreground=[('active',
                self.styles[self.n]['activeforeground'])],
                )
     
    def _Progressbar_config(self):
        """Стиль для віджета ttk.Progressbar."""           
        self.layout("LabeledProgressbar",
         [('LabeledProgressbar.trough',
           {'children': [('LabeledProgressbar.pbar',
                          {'side': 'left', 'sticky': 'ns'}),
                         ("LabeledProgressbar.label",
                          {"sticky": ""})],
           'sticky': 'nswe'})])
        
        self.configure("LabeledProgressbar",
            background=self.styles[self.n]['background'],
            foreground=self.styles[self.n]['foreground'],
            troughcolor=self.styles[self.n]['activebackground'],
            borderwidth=5,
            )
        
    def _TCheckbutton_config(self):
        """Стиль для віджета ttk.Checkbutton."""
        self.configure("NewCheckbutton.TCheckbutton",
            background=self.styles[self.n]['background'],
            foreground=self.styles[self.n]['foreground'],
            )
        self.map('NewCheckbutton.TCheckbutton',
            foreground=[
                ('selected', self.styles[self.n]['foreground']),
                ],
            background=[
                ('active', self.styles[self.n]['activebackground']),
                ],
                )
                
    def _TScale_config(self):
        """Стиль для віджета ttk.Scale."""
        self.configure("NewScale.Horizontal.TScale",
            background=self.styles[self.n]['background'],
            troughcolor=self.styles[self.n]['activebackground'],
            throughrelief=self.styles[self.n]['relief'],
            borderwidth=10,
            lightcolor=self.styles[self.n]['activebackground']
            )
                              
    def _TCombobox_config(self):
        """Стиль для віджета ttk.Combobox."""
        self.configure("NewCombobox.TCombobox",
            background=self.styles[self.n]['background'],
            foreground=self.styles[self.n]['foreground'],
            arrowcolor=self.styles[self.n]['activebackground'],
            relief=self.styles[self.n]['relief'],
            borderwidth=5,
            selectbackground=self.styles[self.n]['activebackground'],
            )
            
        self.configure('Vertical.TScrollbar',
            background=self.styles[self.n]['background'],
            troughcolor=self.styles[self.n]['activebackground'],
            arrowcolor=self.styles[self.n]['activebackground'],
            borderwidth=5,
            )
        
        self.map('NewCombobox.TCombobox',
            fieldbackground=[('readonly',
                self.styles[self.n]['background'])],
            selectbackground=[('active',
                self.styles[self.n]['activebackground'])],
            )
