========================
About Movar application
========================


Description
===========

This program created for offline working with linguistic dictionaries.

Copyright (C) 2023  Teg Miles.
Movar is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License,
or any later version.

Features
========

  * Provides access to properly formatted files of linguistic dictionaries.
  * Can convert separate words into sound.
  * Supports such interface languages as Ukrainian, English, Japanese.

Supported file formats
======================

  -Only .txt format files for now.

How to use
===========

  * Scan paper dictionary and save it as .txt format file or find already scanned dictionary saved as .txt file.
  * Edit first 4 rows as explained below:
	- First row — #Title:Title of yours dictionary
        - Second row — #Pair:Language pair, for example Eng-Eng
        - Third row — #Description:Brief description of the dictionary
        - Fourth — #Regex filter:A filter from Regular Expressions for words from the dictionary
  * Go to the Settings and choose folder with the file.

    You can find example of the formatting in the file called Webster dictionary(Gutenberg.org).txt,
    which located in the folder named Webster dictionary.

    WARNING:
    In each of the rows must be only one colon symbol «:»
    or you will get a mistake of internal format of the file
    because the application using this symbol as separator.

Authors
========

  - Teg Miles (movarocks2@gmail.com)
  - A part of the code was taken from this book: ``Alan D. Moore. Python GUI Programming with Tkinter. Second Edition``
  - The icon was taken from `this place https://www.flaticon.com/free-icon/dictionary_7793703?term=dictionary&page=3&position=77&origin=tag&related_id=7793703`_.

Requirements
============

* Python 3.11, Tkinter, pyttsx3.

One of the following operating systems:

* **Microsoft Windows**: 64-bit Windows 10 or higher
* **Linux**: x86_64 with kernel 5.15.0 or higher.  *Manjaro 23.0.0 (or newer) recommended.*

Installation
============

Windows
-------

Double-click the ``MOVAR-1.0-win64.msi`` file to launch the installation wizard.
Shortcuts will appear on your desktop and in the menu after the wizard completes.

Linux
-----
Extract ``Movar_1.0.tar.gz`` into a directory on your system.
You can then execute the ``Movar`` file from that directory.


Configuration
=============

Configuration for the application is stored in the ``movar_settings.json`` file
in a directory appropriate to your OS.  Refer to this table:

========== ==============================================
System     Directory
========== ==============================================
Linux, BSD ``$XDG_HOME/`` if defined, else ``~/.config/``
Windows    ``%HOME%\AppData\Local``
========== ==============================================

General notes
=============

  - The more dictionaries you will add to the app, the slower it will be downloading at start.
  - For faster searching through dictionaries better to create separate groups of dictionaries.
  - Windows 10 has unstable behavior with the color styles changes.
