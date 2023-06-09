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

class InterfaceLanguage:
    """Клас, що підтримуєте мови інтерфейсу."""
    
    menu_about_uk = "Додаток Movar створений для роботи оффлайн\n"\
    "із лінгвістичними словниками,\n"\
    "збереженими в форматі '.txt'.\n"\
    "\n"\
    "Copyright (C) 2023  Teg Miles.\n"\
    "Поширюється за ліцензією GNU GPLv3 або новішої версії.\n"\
    "\n"\
    "Автори:\n"\
    "   -Теґ Майлз (movarocks2@gmail.com)\n"\
    "   -Частина коду взята з книги\n"\
    "'Alan D. Moore. Python GUI Programming with Tkinter."\
    "Second Edition'.\n"\
    "   -Іконку для програми взято звідси "
    
    manual_text_uk = "Щоб користуватися програмою\n"\
    "треба виконати наступні кроки:\n"\
    "   -Відсканувати паперовий словник "\
    "та зберегти його у форматі '.txt'\n"\
    "або знайти вже відсканований txt-файл бажаного словника.\n"\
    "   -Відформатувати перші чотири рядки файла словника "\
    "наступним чином:\n"\
    "       *Перший рядок — #Title:Назва вашого словника\n"\
    "       *Другий рядок — #Pair:Мовна пара, наприклад, Eng-Eng\n"\
    "       *Третій рядок — #Description:Стислий опис вашого словника\n"\
    "       *Четвертий рядок — #Regex filter:Фільтр з "\
    "Regular Expression для слів словника\n"\
    "   -Зайти в налаштування й обрати теку з відповідним файлом.\n"\
    "\n"\
    "Приклад форматування можна знайти у файлі "\
    "Webster dictionary(Gutenberg.org).txt,\n"\
    "який можна знайти в теці Webster dictionary.\n"\
    "УВАГА:\n"\
    "Символ двокрапка «:» має бути лише один у кожному рядку,\n"\
    "інакше буде з'являтися помилка форматування,\n"\
    "оскільки цей символ використовується програмою як розділювач.\n"\
    "\n"\
    "Гарячі клавіші:\n"\
    "F2 - Відкрити налаштування словників.\n"\
    "Ctrl+1 - Гортання груп словників угору.\n"\
    "Ctrl+2 - Гортання груп словників донизу.\n"\
    "Ctrl+Q (Linux) - Вихід із програми.\n"\
    
    menu_about_en = "Movar is an application created for offline working with\n"\
    "linguistic dictionaries saved in '.txt' format.\n"\
    "\n"\
    "Copyright (C) 2023  Teg Miles.\n"\
    "This program distributing under GNU GPLv3 or later version.\n"\
    "\n"\
    "Authors:\n"\
    "   -Teg Miles (movarocks2@gmail.com)\n"\
    "   -A part of the code was taken from this book:\n"\
    "'Alan D. Moore. Python GUI Programming with Tkinter."\
    "Second Edition'.\n"\
    "   -The icon was taken from this website "
    
    manual_text_en = "You need to perform below mentioned steps\n"\
    "to begin using this application:\n"\
    "   -Scan paper dictionary and save it in '.txt' format\n"\
    "or find already scanned and saved in .txt format dictionary.\n"\
    "   -Edit first four rows of the dictionary file as described below:\n"\
    "       *First row — #Title:Title of yours dictionary\n"\
    "       *Second row — #Pair:Language pair, for example Eng-Eng\n"\
    "       *Third row — #Description:Brief description of the dictionary\n"\
    "       *Fourth — #Regex filter:A filter from Regular Expressions "\
    "for words from the dictionary\n"\
    "   -Go to the Settings and choose folder with the file.\n"\
    "\n"\
    "You can find example of the formatting in the file called "\
    "Webster dictionary(Gutenberg.org).txt,\n"\
    "which located in the folder named Webster dictionary.\n"\
    "WARNING:\n"\
    "In each of the rows must be only one colon symbol «:»\n"\
    "or you will get a mistake of internal format of the file\n"\
    "because the application using this symbol as separator.\n"\
    "\n"\
    "Hot keys:\n"\
    "F2 - Open the dictionary settings.\n"\
    "Ctrl+1 - Scrolling dictionaries groups upward.\n"\
    "Ctrl+2 - Scrolling dictionaries groups downward.\n"\
    "Ctrl+Q (Linux) - Exit from the program.\n"\
    
    menu_about_jp = "「Movar」アプリケーションは語彙的な辞書に\n"\
    "オフラインの手がける為にを作りました。\n"\
    "この辞書達は「txt」の形式が必要です。\n"\
    "\n"\
    "Copyright (C) 2023  Teg Miles.\n"\
    "「GNU GPLv3」ライセンスに基ずくを配布しています。\n"\
    "\n"\
    "作者達は:\n"\
    "   -　Teg Miles (movarocks2@gmail.com)\n"\
    "   -「Alan D. Moore. Python GUI Programming with Tkinter.\n"\
    "Second Edition」本のよりはコードの一部を取りました。\n"\
    "         -　アプリのアイコンはこのサイトのよりを取りました "
    
    manual_text_jp = "あのアプリの手がける為に次の策が必要です:\n"\
    "   -紙の辞書をスキャンしなさい。あの辞書は「txt」の形式に保存しなさい。 "\
    "又はすでに「txt」の形式に辞書を得なさい。\n"\
    "   -初めの四列はこの方にフォーマットしなさい :\n"\
    "       *一番目列 — #Title:辞書の名前\n"\
    "       *二番目列 — #Pair:言語の対, Eng-Eng など\n"\
    "       *三番目列 — #Description:辞書の簡潔な記述\n"\
    "       *四番目列 — #Regex filter:「Regular Expression」"\
    "のフィルタは辞書の言葉為に\n"\
    "   -アプリに辞書の設定は開けなさい。あの辞書のフォルダを選びなさい。\n"\
    "\n"\
    "「Webster dictionary」のフォルダに"\
    "「Webster dictionary(Gutenberg.org).txt」のファイルには "\
    "あのフォールマットの例を見てください。\n"\
    "警告:\n"\
    "あの列に重点の印「:」一つだけ必要です。\n"\
    "もしくはフォールマットの失敗を現れます。\n"\
    "あの印はセパレータとしてを用いています。\n"\
    "\n"\
    "ホットキー:\n"\
    "F2 - 辞書の設定を開きます。\n"\
    "Ctrl+1 - 辞書のグループを上向きにスクローリングします。\n"\
    "Ctrl+2 - 辞書のグループを下向きにスクローリングします。\n"\
    "Ctrl+Q (Linux) - アプリを出ます。\n"\
    
    translation_options = {
        'Українська':
                {
                'File': 'Файл',
                'Exit': 'Вихід',
                'Settings': 'Налаштування',
                'Dictionary settings': 'Налаштування словників',
                'Search history': 'Історія пошуку',
                'Clear search history': 'Очистити історію пошуку',
                'Show/hide search history': 
                    'Показати/приховати історію пошуку',
                'Font size': 'Розмір шрифту',
                'Font family': 'Назва шрифту',
                'Select theme': 'Обрати тему',
                'Select style': 'Обрати стиль',
                'Help': 'Допомога',
                'About Movar': 'Про Movar',
                'All dictionaries': 'Усі словники',
                'Word search': 'Пошук слова',
                'Paths to dictionaries': 'Шляхи до словників',
                'Select path to dictionaries':
                    'Обрати шлях до словників',
                'Delete path to dictionaries':
                    'Видалити шлях до словників',
                'Delete all paths to dictionaries':
                    'Видалити всі шляхи до словників',
                'Groups of dictionaries': 'Групи словників',
                'Available dictionaries': 'Наявні словники',
                'Add dictionary': 'Додати\nсловник',
                'Delete dictionary': 'Видалити\nсловник',
                'Create group of dictionaries':
                    'Створити групу словників',
                'Delete group of dictionaries':
                    'Видалити групу словників',
                'Delete all groups of dictionaries':
                    'Видалити всі групи словників',
                'Technical settings': 'Технічні налаштування',
                'Title interface messagebox': 'Зміна мови інтерфейсу',
                'Message interface messagebox':
                'Для зміни мови інтерфейсу\
                    \nнеобхідне перезавантаження!',
                'Copy': 'Копіювати',
                'Paste': 'Вставити',
                'Close menu': 'Закрити меню',
                'No word': 'Словник не містить слова',
                'Processing dictionaries': 'Обробка словників',
                'On/Off playing word':
                    'Увімкнути/Вимкнути вимову слів',
                'Transparency scale': 'Рівень прозорості вікон',
                'Play word': 'Вимовити слово',
                'Enter name dict group':
                    'Введіть назву для групи словників',
                'OK': 'Так',
                'Cancel': 'Скасувати',
                'TTS player name': 'Назва програвача тексту',
                'TTS player voice': 'Голос програвача тексту',
                'Show dictionary description':
                    'Показати\nопис\nсловника\nv\nv',
                'Title show description messagebox': 'Опис словника',
                'Message show description messagebox':
                'Будь ласка, оберіть лише один словник серед наявних.',
                'Font family label': 'Родини шрифтів',
                'Title dict download mistake': \
                    'Помилка завантаження',
                'Dict download mistake': \
                    'Хибне внутрішнє\nформатування словника\n',
                'Choose dict location':
                    'Оберіть розташування словника',
                'Menu About': menu_about_uk,
                'Manual': 'Посібник',
                'Manual text': manual_text_uk,
                'Web site': "Сторінка проєкту(GitHub)",
                'Regex mistake': "Помилка у формулі Regex:\n",
                'Regex mistake title': "Помилка в Regex"
                },
                
        'English':
                {
                'File': 'File',
                'Exit': 'Exit',
                'Settings': 'Settings',
                'Dictionary settings': 'Dictionary settings',
                'Search history': 'Search history',
                'Clear search history': 'Clear search history',
                'Show/hide search history': 
                    'Show/hide search history',
                'Font size': 'Font size',
                'Font family': 'Font name',
                'Select theme': 'Select theme',
                'Select style': 'Select style',
                'Help': 'Help',
                'About Movar': 'About Movar',
                'All dictionaries': 'All dictionaries',
                'Word search': 'Word search',
                'Paths to dictionaries': 'Paths to dictionaries',
                'Select path to dictionaries':
                    'Select path to dictionaries',
                'Delete path to dictionaries':
                    'Delete path to dictionaries',
                'Delete all paths to dictionaries':
                    'Delete all paths to dictionaries',
                'Groups of dictionaries': 'Groups of dictionaries',
                'Available dictionaries': 'Available dictionaries',
                'Add dictionary': 'Add\ndictionary',
                'Delete dictionary': 'Delete\ndictionary',
                'Create group of dictionaries':
                    'Create group of dictionaries',
                'Delete group of dictionaries':
                    'Delete group of dictionaries',
                'Delete all groups of dictionaries':
                    'Delete all groups of dictionaries',
                'Technical settings': 'Technical settings',
                'Title interface messagebox':
                    'Changing interface language',
                'Message interface messagebox':
                'For changing interface language\nrebooting is required!',
                'Copy': 'Copy',
                'Paste': 'Paste',
                'Close menu': 'Close menu',
                'No word': "The dictionary doesn't contain the word",
                'Processing dictionaries': 'Processing dictionaries',
                'On/Off playing word': 'On/Off word pronouncing',
                'Transparency scale': 'Transparency scale of windows',
                'Play word': 'Pronounce the word',
                'Enter name dict group':
                    'Enter a name for the dictionary group',
                'OK': 'OK',
                'Cancel': 'Cancel',
                'TTS player name': 'TTS player name',
                'TTS player voice': 'TTS player voice',
                'Show dictionary description':
                    'Show\ndictionary\ndescription\nv\nv',
                'Title show description messagebox': \
                    'Dictionary description',
                'Message show description messagebox':
                'Choose only one dictionary\namong available, please.',
                'Font family label': 'Font families',
                'Title dict download mistake': \
                    'Download mistake',
                'Dict download mistake': \
                    'Wrong internal\ndictionary format\n',
                'Choose dict location':
                    'Choose dictionary location',
                'Menu About': menu_about_en,
                'Manual': 'Manual',
                'Manual text': manual_text_en,
                'Web site': "Project's website(GitHub)",
                'Regex mistake': "Mistake in Regex formula:\n",
                'Regex mistake title': "Regex mistake"
                },
                
        '日本語':
                {
                'File': 'ファイル(F)',
                'Exit': '終了(Q)',
                'Settings': '環境設定',
                'Dictionary settings': '辞書の設定',
                'Search history': '検索履歴',
                'Clear search history': '検索履歴を削除します',
                'Show/hide search history': 
                    '検索履歴を表示(隠)します',
                'Font size': '字体寸法',
                'Font family': '字体名前',
                'Select theme': 'デザインテーマを選びます',
                'Select style': 'スタイルを選びます',
                'Help': 'ヘルプ(H)',
                'About Movar': 'Movarに関する情報',
                'All dictionaries': '全て辞書',
                'Word search': '言葉検索',
                'Paths to dictionaries': '辞書への道',
                'Select path to dictionaries':
                    '辞書への道を選びます',
                'Delete path to dictionaries':
                    '辞書への道を削除します',
                'Delete all paths to dictionaries':
                    '全て辞書への道を削除します',
                'Groups of dictionaries': '辞書のグループ',
                'Available dictionaries': '利用可能な辞書',
                'Add dictionary': '辞書を\n付け加えります',
                'Delete dictionary': '辞書を\n削除します',
                'Create group of dictionaries':
                    '辞書のグループを追加します',
                'Delete group of dictionaries':
                    '辞書のグループを削除します',
                'Delete all groups of dictionaries':
                    '全て辞書のグループを削除します',
                'Technical settings': '技術的な設定',
                'Title interface messagebox':
                    'インタフェイスの言語を変更している',
                'Message interface messagebox':
                'インタフェイスの言語を変更するには\n再起動が必要です！',
                'Copy': 'コピーします',
                'Paste': 'ペーストします',
                'Close menu': 'メニューを閉めます',
                'No word': "この言葉は辞書にありません - ",
                'Processing dictionaries': '辞書を処理している',
                'On/Off playing word': '言葉を読むことは点けます(消します）',
                'Transparency scale': '透徹のレベル',
                'Play word': '言葉を読みます',
                'Enter name dict group':
                    '辞書のグループの名前を入力してください',
                'OK': 'OK',
                'Cancel': 'キャンセル',
                'TTS player name': 'TTSプレーヤーの名前',
                'TTS player voice': 'TTS声の名前',
                'Show dictionary description':
                    '辞書の記述を表示します\nv\nv',
                'Title show description messagebox': \
                    '辞書の記述',
                'Message show description messagebox':
                    '利用可能な辞書のなかに一つだけを選べください。',
                'Font family label': '字体の家族',
                'Title dict download mistake': \
                    'ダウンロードの誤り',
                'Dict download mistake': \
                    '内部辞書の形式が間違っています\n',
                'Choose dict location':
                    '辞書への道を選んでください',
                'Menu About': menu_about_jp,
                'Manual': '手引き',
                'Manual text': manual_text_jp,
                'Web site': "アプリのウェブサイト(GitHub)",
                'Regex mistake': "「Regex」の式に誤りをしまいました:\n",
                'Regex mistake title': "「Regex」の誤り"
                },
        }
