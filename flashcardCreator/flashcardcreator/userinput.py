#  Copyright (c) 2023 Antonio Robirosa <flashcard.creator@areko.consulting>
#
#  This file is part of the Bulgarian Flashcard Creator.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.
#

import logging
import tkinter as tk
from tkinter import simpledialog

# Collection of methods which ask the user for input like the translation of a word and
# what irregular declinations to import from a word

logger = logging.getLogger(__name__)


class ListDialog(simpledialog.Dialog):
    def __init__(self, parent, title, items):
        self.items = items
        super().__init__(parent, title)


    def body(self, master):
        self.listBox = tk.Listbox(master, selectmode=tk.SINGLE, width=100)
        self.listBox.pack()

        for item in self.items:
            self.listBox.insert(tk.END, item)

        return self.listBox


    def apply(self):
        selected_index = self.listBox.curselection()
        if selected_index:
            self.result = self.items[selected_index[0]]
        else:
            self.result = None


def ask_user_for_translation(word_original, translated_word_original):
    """Prompts the user to correct or complete the automatic translation of the original word

    :param word_original: The word which you want to create flashcard for
    :param translated_word_original: Automatic translation
    :return: Final translation accepted by the user
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    final_translation = simpledialog.askstring("Flash card creator",
                                               f'Please write the final translation for {word_original}',
                                               initialvalue=translated_word_original)
    logger.debug(
        f'The user entered the final translation {final_translation} for {word_original}')
    return final_translation


def ask_user_to_choose_a_row(found_classified_words):
    """
    Asks the user to choose one of the words
    :param found_classified_words: List of words found
    :return: One row or None
    """
    root = tk.Tk()
    dialog = ListDialog(root, "Choose Element", found_classified_words)
    selected_word = dialog.result
    logger.debug(f'The selected word is {selected_word}')
    return selected_word
