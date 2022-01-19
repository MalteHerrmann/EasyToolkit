"""
easytk | Malte Herrmann

Das EasyToolkit (easytk) bietet eine API um mithilfe einfacher Befehle graphische
Nutzeroberflächen basierend auf dem tkinter-Framework zu erstellen.

Es gibt eine Hauptklasse (>>EasyDialogue<<), welche als Basis fungiert.
Objekten dieser Klasse können über Methoden (>>add_...<<) Widgets hinzugefügt
werden. Um eine einheitliche optische Erscheinung und einen einheitlichen
Zugriff auf die Elemente zu erhalten wurden diese tkinter-Widgets in
>>widgets<< in übergeordnete Klassen verpackt.

Die, zusätzlich zur Hauptklasse im Paket definierten, Funktionen ermöglichen
Nutzern die einfache Abfrage von Informationen mittels einzelnen Befehlen.
Beispielsweise kann eine Abfrage eines Dateipfades mithilfe des folgenden
Befehls erfolgen:

   pfad = EasyToolkit.ask_filename("Beispielordner")

"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
# Native python modules
import os
import sys
import tkinter as tk
from tkinter import font
try:
    from PIL import Image
    _PIL_LOADED = True
except:
    _PIL_LOADED = False

# ------------------------------------------------------------------------------
# Own Imports
# ------------------------------------------------------------------------------
from easytk import widgets


root = tk.Tk()
root.withdraw()


class Window():
    """
        Class to create a GUI window using the EasyToolkit package.

        Input arguments:
         + [str] window_type
                 -- possible options: "Selection",
                                      "SelectionFalse",
                                      "YesNo",
                                      "OkCancel" ,
                                      "Message"
         + [bool] testing
                  -- flag for testing purposes                                  
    """

    def __init__(self, window_type="SelectionFalse", testing=False):

        self._TESTING = testing
        self._SHOW_LOGO = True
        self.grouped_output = False
        self.window_type = window_type

        widgets.default_settings(self)

        self.cancel_text = "Cancel"
        self.label_width = None
        self.no_text = "No"
        self.false_text = "Cancel"
        self.ok_text = "OK"
        self.selection_text = "Select"
        self.title = "easytk"
        self.yes_text = "Yes"

        # Lists or bools for return values
        self.dialogue_value = None
        self.cboxVals = []
        self.entryVals = []
        self.checkbutton_values = []
        self.return_values = []

        # Lists for labels, buttons etc.
        self.combos = []
        self.comboSources = {}
        self.comboTargets = {}
        self.comboDicts = {}
        self.custom_buttons = []
        self.entries = []
        self.images = []
        self.labels = []
        self.listboxes = []
        self.select_buttons = []
        self.select_none_buttons = []
        self.yes_no_buttons = []
        self.ok_cancel_buttons = []
        self.message_buttons = []
        self.checkbutton_vars = []
        self.checkbuttons = []
        self.return_objects = []

        # -------------------
        # Initialization of main window
        self.master = tk.Toplevel(root)
        self.master.configure(background=self.background_color)
        self.master.attributes("-topmost", True)
        self.master.title(self.title)
        AllFont = font.Font(family=self.font, size=self.fontsize)
        self.master.option_add("*Font", AllFont)
        self.master.bind("<Return>", self.enter)

        self.main_frame = tk.Frame(self.master, background=self.background_color, bd=0, highlightbackground="grey", highlightcolor="grey", highlightthickness=self.borderthickness)


    def show(self):

        self.main_frame.grid(row=0, column=0, sticky=self.sticky, padx=self.padx, pady=self.pady)
        self.main_frame.grid_propagate(True)

        # Show image if desired
        if self._SHOW_LOGO and _PIL_LOADED and not self._TESTING:
            self.logo_widget = widgets.EasyLogo(self, frame=self.master)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        number_of_cols, number_of_rows = self.main_frame.grid_size()
        if number_of_cols == 0:
            number_of_cols = 1
        if number_of_rows == 0:
            number_of_rows = 1
        for idx_col in range(number_of_cols):
            self.main_frame.columnconfigure(idx_col, weight=1)
        for idx_row in range(number_of_rows+1):
            self.main_frame.rowconfigure(idx_row, weight=1)

        self.selection_button_object = None
        self.selection_buttons_object = None
        self.yes_no_buttons_object = None
        self.ok_cancel_buttons_object = None
        if self.window_type == "Selection":
            self.selection_button_object = widgets.EasySelectionButton(self, columnspan=number_of_cols)
        elif self.window_type == "SelectionFalse":
            self.selection_buttons_object = widgets.EasySelectionFalseButtons(self, columnspan=number_of_cols)
        elif self.window_type == "YesNo":
            self.yes_no_buttons_object = widgets.EasyYesNoButtons(self, columnspan=number_of_cols)
        elif self.window_type == "OkCancel":
            self.ok_cancel_buttons_object = widgets.EasyOkCancelButtons(self, columnspan=number_of_cols)
        elif self.window_type != "Message":
            raise ValueError("Unknown dialogue type: {}".format(self.window_type))
        return_buttons = [self.selection_button_object, self.selection_buttons_object, self.yes_no_buttons_object, self.ok_cancel_buttons_object]
        self.return_buttons = [button for button in return_buttons if button is not None]

        self.win_center()

        def close_application():
            print("Execution aborted by user.")
            root.destroy()
            sys.exit()
        self.master.protocol("WM_DELETE_WINDOW", close_application)

        if not self._TESTING:
            root.mainloop()

        return_value = self.get_gui_return_values()
        return return_value


    def get_gui_return_values(self):
        
        if self.dialogue_value is not None:
            return self.dialogue_value
        elif self.grouped_output:
            if self.cboxVals != [] and self.entryVals != [] and self.checkbutton_values != []:
                return self.cboxVals, self.entryVals, self.checkbutton_values
            elif self.cboxVals != [] and self.entryVals != []:
                return self.cboxVals, self.entryVals
            elif self.cboxVals != [] :
                return self.cboxVals
            elif self.entryVals != []:
                return self.entryVals
            else:
                raise ValueError("Current configuration of return values not known.")
        elif self.grouped_output == False and self.return_values != []:
            return self.return_values
        else:
            return


    def win_center(self):
        # --------------------------------------------------------------------------
        # Update frame to ensure accurate width & height
        # --------------------------------------------------------------------------
        self.main_frame.update_idletasks()

        # --------------------------------------------------------------------------
        # Gets the requested values of the height and width.
        # --------------------------------------------------------------------------
        windowWidth = self.main_frame.winfo_reqwidth()
        windowHeight = self.main_frame.winfo_reqheight()

        # --------------------------------------------------------------------------
        # Gets both half the screen width/height and window width/height
        # --------------------------------------------------------------------------
        positionRight = int(self.master.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.master.winfo_screenheight()/2 - windowHeight/2)

        # --------------------------------------------------------------------------
        # Positions the window in the center of the page.
        # --------------------------------------------------------------------------
        self.master.geometry("+{}+{}".format(positionRight, positionDown))


    def all_states(self):

        if self.grouped_output:
            for cbox in self.combos:
                self.cboxVals.append(cbox.get())

            for entry in self.entries:
                self.entryVals.append(entry.get())

            for cbutton_var in self.checkbutton_vars:
                self.checkbutton_values.append(cbutton_var.get())

        else:

            # Return values
            for obj in self.return_objects:
                try:
                    return_value = obj.get()
                except TypeError as e:
                    if "index1" in e.args[0]:
                        return_value = obj.get(1.0, tk.END)
                    else:
                        raise e
                if isinstance(obj, widgets.EasyFileDialogue):
                    return_value = return_value.strip(os.sep)
                    return_value = return_value.strip(os.altsep)
                self.return_values.append(return_value)

        root.destroy()


    def enter(self, event=None):
        widget = self.master.focus_get()
        if widget != self.master:
            widget.invoke()


    def yes_clicked(self):
        self.dialogue_value = True
        root.destroy()


    def no_clicked(self):
        self.dialogue_value = False
        root.destroy()


    def cancel_clicked(self):
        root.destroy()


    def add_label(self, text, width=None, height=None, row=None, column=0, columnspan=1, frame=None, anchor=None, justify=None, add_to_grid=True):
        """ Adds a label to a window. """

        return widgets.EasyLabel(self, text=text, width=width, height=height, row=row, column=column, columnspan=columnspan, frame=frame, anchor=anchor, justify=justify, add_to_grid=add_to_grid)


    def add_title(self, text, width=None, height=None, row=None, column=0, columnspan=1, frame=None, anchor=None, justify=None, add_to_grid=True):
        """ Adds a title frame to a window. """

        return widgets.EasyTitle(self, text=text, width=width, height=height, row=row, column=column, columnspan=columnspan, frame=frame, anchor=anchor, justify=justify, add_to_grid=add_to_grid)


    def add_table(self, values, headings=None, columnwidths=None, width=None, height=None, row=None, column=0, columnspan=1, frame=None, add_to_grid=True):
        """ Adds a table frame to a window. """

        return widgets.EasyTable(self, values, headings=headings, columnwidths=columnwidths, width=width, height=height, row=row, column=column, columnspan=columnspan, frame=frame, add_to_grid=add_to_grid)


    def add_file_dialogue(self, text, initialdir=os.getcwd(), filetypes=(), default_value=None, width=None, height=None, label_width=None, row=None, column=None, columnspan=1, frame=None, anchor=None, justify=None, add_to_grid=True):
        """ Adds a file selection frame to a window. """

        return widgets.EasyFileDialogue(self, text=text, type="file", initialdir=initialdir, filetypes=filetypes, default_value=default_value, width=width, height=height, label_width=label_width, row=row, column=column, columnspan=columnspan, frame=frame, anchor=anchor, justify=justify, add_to_grid=add_to_grid)


    def add_dir_dialogue(self, text, initialdir=os.getcwd(), filetypes=(), default_value=None, width=None, height=None, label_width=None, row=None, column=None, columnspan=1, frame=None, anchor=None, justify=None, add_to_grid=True):
        """ Adds a directory selection frame to a window. """

        return widgets.EasyFileDialogue(self, text=text, type="dir", initialdir=initialdir, filetypes=filetypes, default_value=default_value, width=width, height=height, label_width=label_width, row=row, column=column, columnspan=columnspan, frame=frame, anchor=anchor, justify=justify, add_to_grid=add_to_grid)


    def add_save_file_dialogue(self, text, initialdir=os.getcwd(), filetypes=(), default_value=None, width=None, height=None, label_width=None, row=None, column=None, columnspan=1, frame=None, anchor=None, justify=None, add_to_grid=True):
        """ Adds a file saving selection frame to a window. """

        return widgets.EasyFileDialogue(self, text=text, type="save", initialdir=initialdir, filetypes=filetypes, default_value=default_value, width=width, height=height, label_width=label_width, row=row, column=column, columnspan=columnspan, frame=frame, anchor=anchor, justify=justify, add_to_grid=add_to_grid)


    def add_checkbutton(self, text=None, on=False, alignment=None, width=None, height=None, row=None, column=None, columnspan=1, frame=None, add_to_grid=True):
        """ Adds a checkbutton to a window. """

        return widgets.EasyCheckbutton(self, text=text, on=on, alignment=alignment, width=width, height=height, row=row, column=column, columnspan=columnspan, frame=frame, add_to_grid=add_to_grid)


    def add_combobox(self, values, default_value=None, title=None, width=None, height=None, label_width=None, row=None, column=None, columnspan=1, frame=None, anchor=None, justify=None, add_to_grid=True):
        """ Adds a combobox to a window. """

        return widgets.EasyCombobox(self, values=values, default_value=default_value, title=title, width=width, height=height, label_width=label_width, row=row, column=column, columnspan=columnspan, frame=frame, anchor=anchor, justify=justify, add_to_grid=add_to_grid)


    def add_listbox(self, entries, text=None, select_mode="single", width=None, height=None, label_width=None, row=None, column=0, columnspan=1, frame=None, add_to_grid=True):
        """ Adds a listbox to a window. """
        
        return widgets.EasyListbox(self, entries, text=text, select_mode=select_mode, width=width, height=height, label_width=label_width, row=row, column=column, columnspan=columnspan, frame=frame, add_to_grid=add_to_grid)


    def add_entry(self, title, default_value=None, label_width=None, width=None, height=None, row=None, column=None, columnspan=1, frame=None, anchor=None, justify=None, add_to_grid=True):
        """ Adds an entry box to a window. """

        return widgets.EasyEntry(self, title=title, default_value=default_value, label_width=label_width, width=width, height=height, row=row, column=column, columnspan=columnspan, frame=frame, anchor=anchor, justify=justify, add_to_grid=add_to_grid)


    def add_image(self, filepath, width=None, height=None, row=None, column=None, columnspan=1, frame=None, add_to_grid=True):
        """ Adds an image to a window. """

        return widgets.EasyImage(self, filepath=filepath, width=width, height=height, row=row, column=column, columnspan=columnspan, frame=frame, add_to_grid=add_to_grid)


    def add_text(self, text, export=False, monospace=False, width=None, height=None, row=None, column=None, columnspan=1, frame=None, add_to_grid=True):
        """ Adds a text to a window. """

        return widgets.EasyText(self, text=text, export=export, monospace=monospace, width=width, height=height, row=row, column=column, columnspan=columnspan, frame=frame, add_to_grid=add_to_grid)


    def add_button(self, text, command, focus=False, width=None, height=None, row=None, column=0, columnspan=1, fill_frame=True, frame=None, add_to_grid=True):
        """ Adds a button to a window. """

        return widgets.EasyButton(self, text=text, command=command, focus=focus, width=width, height=height, row=row, column=column, columnspan=columnspan, fill_frame=fill_frame, frame=frame, add_to_grid=add_to_grid)


    def add_label_frame(self, text, width=None, height=None, row=None, column=0, columnspan=1, frame=None, add_to_grid=True):
        """ Adds a label frame to a window. """

        return widgets.EasyLabelFrame(self, text=text, width=width, height=height, row=row, column=column, columnspan=columnspan, frame=frame, add_to_grid=add_to_grid)
    

    def add_frame(self, width=None, height=None, row=None, column=0, columnspan=1, frame=None, add_to_grid=True):
        """ Adds a frame to a window. """

        return widgets.EasyFrame(self, width=width, height=height, row=row, column=column, columnspan=columnspan, frame=frame, add_to_grid=add_to_grid)


    def config(self, **kwargs):
        r"""
            Method to configure the behaviour of the window object.

            Input arguments:
             + [?]   kwargs
                     -- keywords can be any attribute of Window

                        A full list of attributes and methods can be found with
                        the following command:
                        print("\n".join([entry for entry in dir( >>Window<< ) if entry[0] != "_"]))
            """

        for arg in kwargs:
            if hasattr(self, arg):
                required_argument_type = eval("""type(self.{})""".format(arg))
                if type(kwargs[arg]) != required_argument_type and required_argument_type != type(None):
                    raise ValueError(f"""Incompatible type {type(kwargs[arg])} for setting: {arg}.\n --> Should be {eval('type(self.{})'.format(arg))}""")
                else:
                    if arg == "title":
                        self.master.title(kwargs[arg])
                    else:
                        exec("""self.{} = {}""".format(arg, repr(kwargs[arg])))
            else:
                raise ValueError(f"Unknown setting: {arg}\n --> This cannot be edited at the present moment.")


def ask_yes_no(text, title=None, yes_text=None, no_text=None, show_logo=True):
    """
        =============================
        ask_yes_no
        =============================
        ask_yes_no(text, title=None, yes_text=None, no_text=None, show_logo=True)

        Function to create a simple Yes-No-Dialogue showing the given text.

        Input arguments:
         + [str] text
         + [str] title
         + [str] yes_text
         + [str] no_text
         + [bool] show_logo"""

    yes_no_dialogue = Window(window_type="YesNo")
    yes_no_dialogue.add_label(text)

    if title is not None:
        yes_no_dialogue.config(title=title)

    if yes_text is not None:
        yes_no_dialogue.config(yes_text=yes_text)

    if no_text is not None:
        yes_no_dialogue.config(no_text=no_text)

    yes_no_dialogue._SHOW_LOGO = show_logo

    return yes_no_dialogue.show()


def simple_selection(values, text=None, title=None, selection_text=None, show_logo=True):
    """ Function to create a simple dropdown selection window showing the given text. """

    simple_selection = Window()

    if type(values) != list:
        raise ValueError(f"Please provide a list of values. Current type: {type(values)}")

    if text is not None:
        simple_selection.add_label(text)
    if title is not None:
        simple_selection.config(title=title)
    if selection_text is not None:
        simple_selection.config(selection_text=selection_text)

    simple_selection._SHOW_LOGO = show_logo

    tWidth = 30
    for i in values:
        if round(len(i), -1) > tWidth:
            tWidth = int(round(len(i), -1))

    if not tWidth:
        simple_selection.add_combobox(values)
    else:
        simple_selection.add_combobox(values, width=tWidth)

    return_value = simple_selection.show()

    if return_value is None:
        return None
    else:
        return return_value[0]


def simple_selection_or_false(values, text=None, title=None, selection_text=None, false_text=None, show_logo=True):
    """
        Function to create a simple dropdown selection window showing the given text, where it's possible to not select anything
    """

    simple_selection = Window(window_type="SelectionFalse")

    if type(values) != list:
        raise ValueError(f"Please provide a list of values. Current type: {type(values)}")

    if text is not None:
        simple_selection.add_label(text)
    if title is not None:
        simple_selection.config(title=title)
    if selection_text is not None:
        simple_selection.config(selection_text=selection_text)
    if false_text is not None:
        simple_selection.config(false_text=false_text)

    simple_selection._SHOW_LOGO = show_logo

    tWidth = 30
    for i in values:
        if round(len(i), -1) > tWidth:
            tWidth = int(round(len(i), -1))

    if not tWidth:
        simple_selection.add_combobox(values)
    else:
        simple_selection.add_combobox(values, width=tWidth)

    return_value = simple_selection.show()

    if return_value is None:
        return None
    elif return_value == False:
        return False
    else:
        return return_value[0]


def simple_input(text, title:str=None, selection_text:str=None, default_value:str="", show_logo:bool=True):
    """ Function to create a simple user input with one entry box. """

    simple_input = Window()

    if title is not None:
        simple_input.config(title=title)
    if selection_text is not None:
        simple_input.config(selection_text=selection_text)

    simple_input._SHOW_LOGO = show_logo
    simple_input.add_entry(text, default_value=default_value)
    return_value = simple_input.show()

    if return_value is None:
        return None
    else:
        return return_value[0]


def message(text=None, title=None, type='OK', show_logo=True, scrollable=False, width=None, settings=None):
    """
        =============================
        message
        =============================
        message(text=None, title=None, type='OK', show_logo=True, scrollable=False, width=None, settings=None)

        Function to create a simple message window showing the given text.

        Input arguments:
         + [str] text
         + [str] title
         + [str] type
                 -- possible options: "OK", "OKCXL", "YesNo"
         + [bool] show_logo
         + [bool] scrollable
         + [int] width
         + [dict] settings"""

    if type == "OK":
        message = Window()
        message.config(selection_text="OK")
    elif type == "OKCXL":
        message = Window(window_type="OkCancel")
    elif type == "YesNo":
        message = Window(window_type="YesNo")
    else:
        raise ValueError("\n\nWrong type: {}.\nPossible options: {}".format(type))

    if width is not None:
        message.config(width=width)

    if text is not None:
        if scrollable == True:
            message.add_text(text, settings)
        else:
            message.add_label(text)
    if title is not None:
        message.config(title=title)

    message._SHOW_LOGO = show_logo

    return message.show()


def ask_filename(text, initialdir=os.getcwd(), default_value=None, filetypes=None, width=None, label_width=None):
    """
        =============================
        ask_filename
        =============================
        ask_filename(text, initialdir=os.getcwd(), default_value=None, filetypes=None, width=None, label_width=None)

        Simple GUI which shows a file dialogue.

        Input arguments:
         + [str] text
         + [str] initialdir
         + [str] default_value
         + [tuple] filetypes
         + [int] width
         + [int] label_width"""

    file_dialog = Window()
    file_dialog.config(selection_text="OK")
    if width is not None:
        file_dialog.config(width=width)

    file_dialog.add_label(text)
    file_dialog.add_file_dialogue("", initialdir=initialdir, default_value=default_value, label_width=label_width, filetypes=filetypes)

    return_value = file_dialog.show()
    if return_value is None:
        sys.exit()
    else: return return_value[0]


def ask_dirname(text, initialdir=os.getcwd(), default_value=None, width=None, label_width=None):
    """
        =============================
        ask_dirname
        =============================
        ask_dirname(text, initialdir=os.getcwd(), default_value=None, width=None, label_width=None)

        Simple GUI which shows a directory dialogue.

        Input arguments:
         + [str] text
         + [str] initialdir
         + [str] default_value
         + [int] width
         + [int] label_width"""

    file_dialog = Window()
    file_dialog.config(selection_text="OK")
    if width is not None:
        file_dialog.config(width=width)

    file_dialog.add_label(text)
    file_dialog.add_dir_dialogue("", initialdir=initialdir, default_value=default_value, label_width=label_width)

    return_value = file_dialog.show()
    if return_value is None:
        sys.exit()
    else: return return_value[0]


def ask_savefilename(text, initialdir=os.getcwd(), default_value=None, filetypes=None, width=None, label_width=None):
    """
        =============================
        ask_savefilename
        =============================
        ask_savefilename(text, initialdir=os.getcwd(), default_value=None, filetypes=None, width=None, label_width=None)

        Simple GUI which shows a saving file dialogue.

        Input arguments:
         + [str] text
         + [str] initialdir
         + [str] default_value
         + [tuple] filetypes
         + [int] width
         + [int] label_width"""

    file_dialog = Window()
    file_dialog.config(selection_text="OK")
    if width is not None:
        file_dialog.config(width=width)

    file_dialog.add_label(text)
    file_dialog.add_save_file_dialogue("", initialdir=initialdir, default_value=default_value, label_width=label_width, filetypes=filetypes)

    return_value = file_dialog.show()
    if return_value is None:
        sys.exit()
    else: return return_value[0]
