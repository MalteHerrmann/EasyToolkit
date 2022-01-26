"""widgets | Malte Herrmann

Hier sind die einzelnen >>widgets<< definiert, welche im Rahmen von
>>easytk<< in die erstellten GUIs eingefügt werden.

Das Hinzufügen der Widgets zur GUI sollte nicht mithilfe dieser Objekte
geschehen, sondern mit den dafür vorgesehen Methoden in der >>Window<<-
Klasse.
"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import os
import re
import sys
import tkinter
import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter import filedialog
from typing import Union
from PIL import Image, ImageTk

module_path = os.path.dirname(os.path.dirname(__file__))


def default_settings(object):

    object.background_color = "white"
    object.background_color = "lightgrey"
    object.background_color = "#E6E6E6"
    object.borderthickness = 1
    object.font = "Arial"
    object.fontcolor = "black"
    object.fontsize = 10
    object.height = 30
    object.width = 600
    object.padx = 5
    object.pady = 5
    object.relief = "solid"
    object.on = False
    object.state = "readonly"
    object.sticky = tk.W+tk.E+tk.N

    # ------------------
    # Check if script executed from linux
    if re.search("\/(home|mnt)\/", os.getcwd()):
        object.on_linux = True
    else:
        object.on_linux = False


class EasyWidget:

    def __init__(self):

        default_settings(self)
        self.focus=True


    def assign_values(self, EasyDialogue, locals_dict):
        """
            Assigns default values to an EasyWidget.
            
            Arguments:
            - [EasyDialogue] EasyDialogue
            - [dict] locals_dict
        """
        
        self.EasyDialogue = EasyDialogue

        self.row = locals_dict["row"]
        self.column = locals_dict["column"]
        self.columnspan = locals_dict["columnspan"]

        if "frame" not in locals_dict or locals_dict["frame"] is None:
            self.frame = EasyDialogue.main_frame
        else:
            frame = locals_dict["frame"]
            if isinstance(frame, EasyLabelFrame) or isinstance(frame, EasyFrame):
                frame = frame.object
                self.frame = frame
            else:
                self.frame = frame

        if "width" not in locals_dict or locals_dict["width"] is None:
            if not ".!frame" in self.frame.winfo_parent():
                self.width = EasyDialogue.width * self.columnspan
            else:
                self.width = self.frame.winfo_reqwidth()

        else:
            self.width = locals_dict["width"]

        if "height" in locals_dict and locals_dict["height"] is not None:
            self.height = locals_dict["height"]
            
        if "anchor" not in locals_dict or locals_dict["anchor"] is None:
            self.anchor = "w"
        else:
            self.anchor = locals_dict["anchor"]

        if "justify" not in locals_dict or locals_dict["justify"] is None:
            self.justify = "left"
        else:
            self.justify = locals_dict["justify"]

        if "label_width" in locals_dict:
            if locals_dict["label_width"] is None:
                self.label_width = EasyDialogue.label_width
            else:
                self.label_width = locals_dict["label_width"]

        if "focus" not in locals_dict or locals_dict["focus"] is None:
            self.focus = False
        else:
            self.focus = locals_dict["focus"]

        if "select_mode" in locals_dict and locals_dict["select_mode"] is not None:
            self.select_mode = locals_dict["select_mode"]

        if "type" in locals_dict and locals_dict["type"] is not None:
            self.type = locals_dict["type"]


    def file_chosen(self, entry_box, type, initialdir, filetypes, string_var=None):

        entry = entry_box.get()
        if entry != "":
            if os.path.isfile(entry):
                initialdir = os.path.split(entry)[0]
            elif os.path.isdir(entry):
                initialdir = entry

        if filetypes is None:
            filetypes = ()

        if len(filetypes) > 0:
            if not isinstance(filetypes[0], tuple):
                filetypes_list = [filetypes]
            else:
                filetypes_list = list(filetypes)
            if ("Alle Dateien (*.*)","*.*") not in filetypes_list:
                filetypes_list.append(("Alle Dateien (*.*)","*.*"))
            filetypes = tuple(filetypes_list)

        if type == "file":
            path = filedialog.askopenfilename(title="Choose file", initialdir=initialdir, filetypes=filetypes)
        elif type == "dir":
            path = filedialog.askdirectory(title="Choose directory", initialdir=initialdir)
        elif type == "save":
            if initialdir is None:
                path = filedialog.asksaveasfilename(title="Save As", filetypes=filetypes)
            else:
                # path = filedialog.asksaveasfilename(title="Save As", initialdir=initialdir, filetypes=filetypes)
                path = filedialog.asksaveasfilename(title="Save As", initialdir=initialdir, filetypes=filetypes)
        else:
            path = ""

        if path is not [] and path != "":
            if string_var is not None:
                string_var.set(path)
                if hasattr(self, "check_path") and callable(self.check_path):
                    self.check_path()
            else:
                entry_box.delete(0, tk.END)
                entry_box.insert(0, path)

        entry_box.xview_moveto(1)


    def insert_into_grid(self, object, frame, row, column, columnspan, sticky=None):

        if sticky is None:
            sticky=self.sticky

        if hasattr(self, "EasyDialogue"):
            if hasattr(self.EasyDialogue, "return_buttons"):
                if len(self.EasyDialogue.return_buttons) > 0:
                    _RETURN_BUTTONS_EXIST = True
                    for idx, button in enumerate(self.EasyDialogue.return_buttons):
                        button.grid_object.grid_forget()
                else:
                    _RETURN_BUTTONS_EXIST = False
            else:
                _RETURN_BUTTONS_EXIST = False
        else:
            _RETURN_BUTTONS_EXIST = False

         

        if row is None:
            object.grid(row=frame.grid_size()[1], column=column, columnspan=columnspan, sticky=self.sticky, padx=self.padx, pady=self.pady)
        elif isinstance(row, int):
            object.grid(row=row, column=column, columnspan=columnspan, sticky=self.sticky, padx=self.padx, pady=self.pady)
        else:
            raise ValueError("Row must be integer or None!")

        if _RETURN_BUTTONS_EXIST:
            for button in self.EasyDialogue.return_buttons:
                button.grid_object.grid()


    def remove_from_grid(self):
        self.grid_object.grid_remove()


class EasyButton(EasyWidget):

    def __init__(self, EasyDialogue, text=None, command=None, focus=False, width=None, height=None, row=None, column=0, columnspan=1, fill_frame=True, frame=None, add_to_grid=True):

        EasyWidget.__init__(self)
        self.assign_values(EasyDialogue, locals())

        if text is None:
            raise ValueError("\n\nKeyword argument 'text' has to be set.\n")

        self.grid_object = tkinter.Frame(self.frame, width=self.width, height=self.height, background=EasyDialogue.background_color)
        self.object = tkinter.Button(self.grid_object, text=text, command=command, background=EasyDialogue.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize))
        self.object.pack(fill="both" if fill_frame==True else None, expand=True if fill_frame==True else False)
        self.grid_object.pack_propagate(False)

        EasyDialogue.custom_buttons.append(self.object)
        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)
        if add_to_grid == False:
            self.remove_from_grid()

        if focus == True:
            self.grid_object.focus_set()


class EasyFrame(EasyWidget):

    def __init__(self, EasyDialogue, width=None, height=None, row=None, column=0, columnspan=1, frame=None, add_to_grid=True):

        EasyWidget.__init__(self)
        self.assign_values(EasyDialogue, locals())

        self.grid_object = tkinter.Frame(self.frame, background=EasyDialogue.background_color)
        self.object = tkinter.Frame(self.grid_object, width=self.width, height=self.height, background=EasyDialogue.background_color)
        self.object.pack(side="left", fill="both", expand=True, padx=0)
        self.grid_object.pack_propagate(True)
        self.object.grid_propagate(True)

        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)
        if add_to_grid == False:
            self.remove_from_grid()


class EasyLabelFrame(EasyWidget):

    def __init__(self, EasyDialogue, text, width=None, height=None, row=None, column=0, columnspan=1, frame=None, add_to_grid=True):

        EasyWidget.__init__(self)
        self.assign_values(EasyDialogue, locals())

        self.grid_object = tkinter.Frame(self.frame, background=EasyDialogue.background_color)
        self.object = tkinter.LabelFrame(self.grid_object, text=text, width=self.width, height=self.height, font=(EasyDialogue.font, EasyDialogue.fontsize-2), background=EasyDialogue.background_color)
        self.object.pack(side="left", fill="both", expand=True, padx=0)
        self.grid_object.pack_propagate(True)
        self.object.grid_propagate(True)

        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)
        if add_to_grid == False:
            self.remove_from_grid()


class EasyTitle(EasyWidget):

    def __init__(self, EasyDialogue, text:str, width=None, height=None, row=None, column=0, columnspan=1, frame=None, anchor=None, justify=None, add_to_grid=True):

        EasyWidget.__init__(self)
        self.assign_values(EasyDialogue, locals())

        self.number_of_lines = len(text.split("\n"))

        self.grid_object = tkinter.Frame(self.frame, width=self.width, height=self.height*self.number_of_lines, background=EasyDialogue.background_color)
        self.object = tkinter.Label(self.grid_object, height=self.number_of_lines, text=text, font=(EasyDialogue.font, EasyDialogue.fontsize), background=self.background_color, anchor=self.anchor, justify=self.justify, width=self.width, padx=0)
        self.object.pack(side="left", fill="both", expand=True, padx=0)
        self.grid_object.pack_propagate(False)

        EasyDialogue.labels.append(self.object)
        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)
        if add_to_grid == False:
            self.remove_from_grid()


class EasyListbox(EasyWidget):

    def __init__(self, EasyDialogue, entries, text=None, select_mode="single", width=None, height=None, label_width=None, row=None, column=0, columnspan=1, frame=None, add_to_grid=True):
        
        EasyWidget.__init__(self)
        self.assign_values(EasyDialogue, locals())

        if not isinstance(entries, list):
            raise TypeError("Entries must be list. Current type: '{}'".format(type(entries)))

        if select_mode not in ["single", "extended", "multiple"]:
            raise ValueError(f"Forbidden selection mode: '{select_mode}'.")
        
        self.entries = entries.copy()
        self.grid_object = tkinter.Frame(self.frame, width=self.width, height=len(entries)*self.height, background=EasyDialogue.background_color)
        
        if text is not None:
            if self.label_width is None:
                label = self.label = tk.Label(self.grid_object, text=text, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize), anchor="w", justify="left", padx=0)
            else:
                label = self.label = tk.Label(self.grid_object, text=text, width=self.label_width, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize), anchor=self.anchor, justify=self.justify, padx=0)
            label.pack(side="left", anchor="nw", padx=(0, self.padx))
        
        self.string_var = tk.StringVar()
        self.string_var.set(self.entries)
        self.object = tkinter.Listbox(self.grid_object, listvariable=self.string_var, selectmode=select_mode, width=self.width, height=self.height, font=(EasyDialogue.font, EasyDialogue.fontsize), background="white", exportselection=False)
        self.set(entries[0])
        self.object.pack(side="left", fill="both", expand=True, padx=0)
        self.grid_object.pack_propagate(False)

        EasyDialogue.listboxes.append(self.object)
        EasyDialogue.return_objects.append(self)
        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)
        if not add_to_grid:
            self.remove_from_grid()

    
    def set(self, new_value:str) -> None:
        for idx, entry in enumerate(self.entries):
            if entry == new_value:
                self.object.selection_clear(0, 'end')
                self.object.activate(idx)
                self.object.index(idx)
                self.object.selection_set(idx)
                break
        else:
            self.insert_value(new_value)
            self.set(new_value)

    
    def insert_value(self, new_value:str) -> None:
            self.entries.append(new_value)
            self.string_var.set(self.entries)

    
    def get(self) -> Union[list, str]:
        """ 
            Returns a list of selected values if multiple selection is allowed. Otherwise, the 
            selected value is returned as a string.
        """

        selected_values = [self.object.get(idx) for idx in self.object.curselection()]
        if self.select_mode in ["multiple", "extended"]:
            return_value = selected_values
        else:
            if len(selected_values) > 0:
                return_value = selected_values[0]
            else:
                return ""
        return return_value


class EasyTable(EasyWidget):

    def __init__(self, EasyDialogue, values, headings=None, columnwidths=None, width=None, height=None, row=None, column=0, columnspan=1, frame=None, add_to_grid=True):

        EasyWidget.__init__(self)
        self.assign_values(EasyDialogue, locals())

        if not isinstance(values, dict):
            raise ValueError("\n\nValues must be given as a dictionary. Current type: {}".format(type(values)))

        len_list = []
        for key in values:
            if not isinstance(values[key], str):
                len_list.append(len(values[key]))
            else:
                len_list.append(1)
        number_of_columns = max(len_list)

        self.grid_object = tk.Frame(self.frame, width=width, height=height, background=EasyDialogue.background_color)
        table_frame = tk.Frame(self.grid_object, width=width, height=height, background=EasyDialogue.background_color)
        # self.object = ttk.Treeview(self.grid_object, selectmode="browse")
        self.object = ttk.Treeview(table_frame, selectmode="browse")
        if number_of_columns == 1 and headings is None:
            self.object["columns"] = ("",)
        elif headings is None:
            self.object["columns"] = tuple(["" for _ in range(number_of_columns)])
        else:
            self.object["columns"] = headings

        if headings is None:
            self.object["show"] = "tree"

        # Create scrollbars and assign functionality
        hsb = ttk.Scrollbar(self.grid_object, orient="horizontal", command=self.object.xview)
        vsb = ttk.Scrollbar(self.grid_object, orient="vertical", command=self.object.yview)
        self.object.configure(xscrollcommand=hsb.set)
        self.object.configure(yscrollcommand=vsb.set)

        # Assign column widths
        if columnwidths is not None:
            if len(columnwidths) != number_of_columns:
                print("Unequal number of widths ({}) and columns ({})!".format(len(columnwidths), number_of_columns))
            else:
                for idx, columnwidth in enumerate(columnwidths):
                    self.object.column(idx, width=columnwidth)

        # Insert contents
        first_value = values[[key for key in values.keys()][0]]
        if isinstance(first_value, dict):
            for idx, key in enumerate(values):
                contained_values = [values[key][key_inner] for idx_inner, key_inner in enumerate(values[key]) if idx_inner > 0]

                if number_of_columns == 1:
                    self.object.insert("", "end", text=key, values=(str(contained_values),))
                else:
                    self.object.insert("", "end", text=key, values=tuple(contained_values))
        else:
            for idx, key in enumerate(values):
                if number_of_columns == 1:
                    self.object.insert("", "end", text=key, values=(str(values[key]),))
                else:
                    self.object.insert("", "end", text=key, values=tuple(values[key]))

        # self.object.pack(side="left", fill="both", expand=True, padx=0)
        # hsb.pack(side="bottom", fill="x", padx=0, pady=0)
        # vsb.pack(side="right", fill="y", padx=0)
        # self.grid_object.pack_propagate(False)

        self.object.pack(side="left", fill="both", expand=True, padx=0)
        table_frame.pack_propagate(False)

        # self.object.grid(row=0, column=0, padx=0, sticky=self.sticky)
        table_frame.grid(row=0, column=0, padx=0, sticky=tk.S+tk.N+tk.W+tk.E)
        vsb.grid(row=0, column=1, padx=0, sticky=tk.N+tk.S)
        hsb.grid(row=1, column=0, columnspan=1, padx=0, sticky=self.sticky)
        self.grid_object.grid_propagate(True)

        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)
        if not add_to_grid:
            self.remove_from_grid()


class EasyLabel(EasyWidget):

    def __init__(self, EasyDialogue, text=None, width=None, height=None, row=None, column=0, columnspan=1, frame=None, anchor=None, justify=None, add_to_grid=True):

        EasyWidget.__init__(self)
        self.assign_values(EasyDialogue, locals())

        if text is None:
            raise ValueError("Keyword argument 'text' must be set!")

        self.string_var = tk.StringVar()
        self.string_var.set(text if text is not None else "")
        self.grid_object = tkinter.Frame(self.frame, width=self.width, height=self.height, background=EasyDialogue.background_color)
        self.object = tkinter.Message(self.grid_object, textvariable=self.string_var, font=(EasyDialogue.font, EasyDialogue.fontsize), background=self.background_color, anchor=self.anchor, justify=self.justify, width=self.width, padx=0)
        self.object.pack(side="left", fill="both", expand=True, padx=0)
        self.grid_object.pack_propagate(True)

        EasyDialogue.labels.append(self.object)
        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)
        if add_to_grid == False:
            self.remove_from_grid()

    def add_to_grid(self, *obsolete): # *obsolete argument can be deleted in the future
        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)

    def remove_from_grid(self, *obsolete): # *obsolete argument can be deleted in the future
        self.grid_object.grid_remove()


class EasyFileDialogue(EasyWidget):

    def __init__(self, EasyDialogue, type="file", text=None, initialdir=os.getcwd(), filetypes=(), default_value=None, width=None, height=None, label_width=None, row=None, column=None, columnspan=1, frame=None, anchor=None, justify=None, add_to_grid=True):

        EasyWidget.__init__(self)
        self.assign_values(EasyDialogue, locals())

        if text is None:
            raise ValueError("Keyword argument 'text' must be set!")

        self.grid_object = tkinter.Frame(self.frame, width=self.width, height=self.height, background=self.background_color)
        # label = tk.Message(self.grid_object, text=text, background=self.background_color, font=(self.font, self.fontsize))
        self.string_var = tk.StringVar()
        self.string_var.set(text)
        
        if self.label_width is None:
            label = self.label = tk.Label(self.grid_object, textvariable=self.string_var, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize), anchor="w", justify="left", padx=0)
        else:
            label = self.label = tk.Label(self.grid_object, textvariable=self.string_var, width=self.label_width, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize), anchor=self.anchor, justify=self.justify, padx=0)
        label.pack(side="left", padx=(0, self.padx))
        self.object_string_var = tk.StringVar()
        self.object = tkinter.Entry(self.grid_object, relief=self.relief, textvariable=self.object_string_var, font=(EasyDialogue.font, EasyDialogue.fontsize))
        self.object.bind("<Return>", self.check_path())
        if default_value is not None:
            self.object_string_var.set(default_value)
            self.object.xview_moveto(1)
        self.object.pack(side="left", fill="both", expand=True, padx=self.padx)
        if type in ["file", "dir", "save"]:
            button = tk.Button(self.grid_object, text="...", width=5, command=lambda:self.file_chosen(self.object, type, initialdir, filetypes, string_var=self.object_string_var), background=self.background_color, foreground=self.fontcolor, font=(EasyDialogue.font, EasyDialogue.fontsize))
        else:
            raise ValueError("\n\nUnsupported file dialogue type: {}\n\nIt has to be 'file', 'dir' or 'save'.".format(type))
        button.pack(side="left")

        # Remove label from pack if text is ""
        if text == "":
            label.pack_forget()
        
        self.grid_object.pack_propagate(False)
        
        # bind string var
        self.object_string_var.trace_add("write", self.check_path)
        self.check_path()

        EasyDialogue.entries.append(self.object)
        EasyDialogue.return_objects.append(self)
        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)
        if add_to_grid == False:
            self.remove_from_grid()

    def check_path(self, *args):
        value = self.object_string_var.get()
        if value.strip() == "":
            return

        if self.type == "dir":
            if os.path.isdir(value):
                background_color="#d3ffce"
            else:
                background_color="#ffe4e1"
        elif self.type == "file":
            if os.path.isfile(value):
                background_color="#d3ffce"
            else:
                background_color="#ffe4e1"
        elif self.type == "save":
            dirname = os.path.dirname(value)
            if os.path.isfile(value) and os.path.exists(value):
                background_color="#ffff70"
            elif dirname == "" or os.path.isdir(dirname):
                background_color="#d3ffce"
            else:
                background_color="#ffe4e1"

        self.object.config(background=background_color)


    def set(self, new_value: str) -> None:
        if isinstance(new_value, str):
            # self.object.delete(0, tk.END)
            # self.object.insert(0, new_value)
            self.object_string_var.set(new_value)
            self.check_path()
            self.object.xview_moveto(1)
        else:
            raise TypeError(f"\n\nNeuer Wert muss ein String sein!\nAktueller Typ: {type(new_value)}\n\n")


    def get(self) -> str:
        return self.object_string_var.get()


class EasyImage(EasyWidget):

    def __init__(self, EasyDialogue, filepath=None, width=None, height=None, row=None, column=None, columnspan=1, frame=None, add_to_grid=True):

        EasyWidget.__init__(self)
        self.assign_values(EasyDialogue, locals())
        
        if not os.path.exists(filepath):
            raise ValueError("\n\nFile not found: {}".format(filepath))

        current_image = Image.open(filepath)
        resized = current_image.resize((self.width, self.height))
        self.current_image_resized = ImageTk.PhotoImage(resized)

        self.grid_object = tkinter.Frame(self.frame, width=self.width, height=self.height, background=self.background_color)
        self.object = tkinter.Label(self.grid_object, image=self.current_image_resized, width=self.width, height=self.height, background=self.background_color)
        self.object.pack()
        self.grid_object.pack_propagate(False)

        EasyDialogue.images.append(self.current_image_resized)
        EasyDialogue.labels.append(self.object)
        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)
        if add_to_grid == False:
            self.remove_from_grid()


class EasyEntry(EasyWidget):

    def __init__(self, EasyDialogue, default_value=None, title=None, label_width=None, width=None, height=None, row=None, column=None, columnspan=1, frame=None, anchor=None, justify=None, add_to_grid=True):

        EasyWidget.__init__(self)
        self.assign_values(EasyDialogue, locals())

        self.grid_object = tkinter.Frame(self.frame, width=self.width, height=self.height, background=self.background_color)
        self.string_var = tk.StringVar()
        #TODO: hier Konsistenz bzgl. Labelstring-Var einbauen etc.
        if title is not None:
            self.string_var.set(title)
            if self.label_width is None:
                self.title_label = self.label = tkinter.Label(self.grid_object, textvariable=self.string_var, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize), anchor=self.anchor, justify=self.justify, padx=0)
            else:
                # print("Used label width: {}".format(label_width))
                self.title_label = self.label = tkinter.Label(self.grid_object, textvariable=self.string_var, width=self.label_width, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize), anchor=self.anchor, justify=self.justify, padx=0)
            self.title_label.pack(side="left", padx=(0, 2*self.padx))
        self.object = tkinter.Entry(self.grid_object, relief=self.relief, font=(EasyDialogue.font, EasyDialogue.fontsize))
        if default_value is not None:
            self.object.insert(0, default_value)
            self.object.xview_moveto(1)
        self.object.pack(side="left", fill="both", expand=True)
        self.grid_object.pack_propagate(False)

        EasyDialogue.entries.append(self.object)
        EasyDialogue.return_objects.append(self.object)
        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)
        if add_to_grid == False:
            self.remove_from_grid()
        

    def set(self, new_value) -> None:
        if isinstance(new_value, str):
            self.object.delete(0, tk.END)
            self.object.insert(0, new_value)
            self.object.xview_moveto(1)
            

    def get(self) -> str:
        return self.object.get()


class EasyCombobox(EasyWidget):

    def __init__(self, EasyDialogue, values=None, default_value=None, title=None, width=None, height=None, label_width=None, row=None, column=None, columnspan=1, frame=None, anchor=None, justify=None, add_to_grid=True):

        EasyWidget.__init__(self)
        self.assign_values(EasyDialogue, locals())

        if values is None:
            raise ValueError("\n\nKeyword argument 'values' has to be set.")

        if default_value is None:
            default_value = values[0]

        self.grid_object = tkinter.Frame(self.frame, width=self.width, height=self.height, background=self.background_color)
        if title is not None:
            self.string_var = tk.StringVar()
            self.string_var.set(title)
            if self.label_width is None:
                self.combobox_label = self.label = tkinter.Label(self.grid_object, textvariable=self.string_var, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize), anchor=self.anchor, justify=self.justify, padx=0)
            else:
                # print("Used label width: {}".format(label_width))
                self.combobox_label = self.label = tkinter.Label(self.grid_object, textvariable=self.string_var, width=self.label_width, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize), anchor=self.anchor, justify=self.justify, padx=0)
            self.combobox_label.pack(side="left", padx=(0, 2*self.padx))
        self.object = ttk.Combobox(self.grid_object, values=values, state=self.state, font=(EasyDialogue.font, EasyDialogue.fontsize))
        self.object.set(default_value)
        self.object.pack(side="left", fill="both", expand=True)
        self.grid_object.pack_propagate(False)

        EasyDialogue.combos.append(self.object)
        EasyDialogue.return_objects.append(self.object)
        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)
        if not add_to_grid:
            self.remove_from_grid()


    def set(self, new_value) -> None:
        self.object.set(new_value)


    def get(self) -> str:
        return self.object.get()


class EasyCheckbutton(EasyWidget):

    def __init__(self, EasyDialogue, text=None, on=False, alignment=None, width=None, height=None, row=None, column=None, columnspan=1, frame=None, add_to_grid=True):

        EasyWidget.__init__(self)
        self.assign_values(EasyDialogue, locals())

        if text is None:
            raise ValueError("\n\nKeyword argument 'text' has to be set.")

        self.grid_object = tkinter.Frame(self.frame, width=self.width, height=self.height, background=self.background_color)
        self.object_var = tkinter.IntVar()
        if on == True:
            self.object_var.set(1)
        else:
            self.object_var.set(0)
        self.string_var = tk.StringVar()
        self.string_var.set(text)
        self.object = tkinter.Checkbutton(self.grid_object, textvariable=self.string_var, variable=self.object_var, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize), anchor="w")
        self.object.pack(side="left", fill="both", expand=True)
        self.grid_object.pack_propagate(False)

        EasyDialogue.checkbutton_vars.append(self.object_var)
        EasyDialogue.checkbuttons.append(self.object)
        EasyDialogue.return_objects.append(self.object_var)
        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)
        if add_to_grid == False:
            self.remove_from_grid()
        

    def get(self):
        return self.object_var.get()
        

    def set(self, new_value):
        if new_value == True:
            new_value = 1
        elif new_value == False:
            new_value = 0
        elif new_value not in (0, 1):
            raise ValueError("Only valid values are: True, False, 1 ,0! Current value: {}".format(new_value))
        self.object_var.set(new_value)


class EasyText(EasyWidget):

    def __init__(self, EasyDialogue, text=None, export=False, monospace=False, width=None, height=None, row=None, column=None, columnspan=1, frame=None, add_to_grid=True):

        EasyWidget.__init__(self)
        self.assign_values(EasyDialogue, locals())

        if text is None:
            raise ValueError("\n\nKeyword argument 'text' has to be set.")

        self.grid_object = tkinter.Frame(self.frame, width=self.width, height=self.height, background=self.background_color)
        self.object = tkinter.Text(self.grid_object, font=(self.font if not monospace else "Courier", self.fontsize), foreground=self.fontcolor, background=self.background_color)
        self.object.insert(tkinter.END, text)
        self.object.pack(fill="both", expand=True)
        self.grid_object.pack_propagate(False)

        EasyDialogue.labels.append(self.object)
        if export == True:
            EasyDialogue.return_objects.append(self.object)
        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)
        if add_to_grid == False:
            self.remove_from_grid()


    def set(self, new_value) -> None:
        if isinstance(new_value, str):
            self.object.delete(1.0, tk.END)
            self.object.insert(1.0, new_value)
            self.object.xview_moveto(1)
            

    def get(self) -> str:
        return self.object.get("1.0", "end-1c")


class EasySelectionButton(EasyWidget):

    def __init__(self, EasyDialogue, row=None, column=0, columnspan=1, focus=True, frame=None, fill_frame=False):

        EasyWidget.__init__(self)
        self.assign_values(EasyDialogue, locals())
            
        if len(EasyDialogue.selection_text) < 13:
            self.grid_object = tkinter.Frame(self.frame, width=EasyDialogue.width*self.columnspan, height=EasyDialogue.height, background=EasyDialogue.background_color)
            self.object = tkinter.Button(self.grid_object, text=EasyDialogue.selection_text, width=10, command=EasyDialogue.all_states, background=EasyDialogue.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize))
        else:
            self.grid_object = tkinter.Frame(self.frame, width=EasyDialogue.width*self.columnspan, height=EasyDialogue.height, background=EasyDialogue.background_color)
            self.object = tkinter.Button(self.grid_object, text=EasyDialogue.selection_text, command=EasyDialogue.all_states, background=EasyDialogue.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize))
        if fill_frame == True:
            self.object.pack(fill="both")
        else:
            self.object.pack()
        self.grid_object.pack_propagate(False)
        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)

        EasyDialogue.select_buttons.append(self.grid_object)

        if self.focus:
            self.grid_object.focus_set()


class EasySelectionFalseButtons(EasyWidget):

    def __init__(self, EasyDialogue, row=None, column=0, columnspan=1, focus=True, frame=None, fill_frame=False):

        EasyWidget.__init__(self)
        self.assign_values(EasyDialogue, locals())

        self.grid_object = tkinter.Frame(self.frame, width=self.width, height=self.height, background=self.background_color)
        self.select_frame = tkinter.Frame(self.grid_object, width=self.width/2, height=self.height, background=self.background_color)
        if len(EasyDialogue.selection_text) < 13:
            self.select_button = tk.Button(self.select_frame, text=EasyDialogue.selection_text, width=10, command=EasyDialogue.all_states, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize))
        else:
            self.select_button = tk.Button(self.select_frame, text=EasyDialogue.selection_text, command=EasyDialogue.all_states, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize))
        # self.yes_button.grid(row=0, column=0, padx=self.padx, pady=self.pady)
        self.select_button.pack(side="right", fill="both")
        EasyDialogue.select_none_buttons.append(self.select_button)
        # self.yes_frame.pack(side="left", fill="both", expand=fill_frame)
        self.select_frame.grid(row=0, column=0, padx=self.padx, pady=self.pady)
        self.select_frame.pack_propagate(False)

        self.none_frame = tkinter.Frame(self.grid_object, width=self.width/2, height=self.height, background=self.background_color)
        if len(EasyDialogue.false_text) < 13:
            self.none_button = tk.Button(self.none_frame, text=EasyDialogue.false_text, width=10, height=self.height, command=EasyDialogue.no_clicked, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize))
        else:
            self.none_button = tk.Button(self.none_frame, text=EasyDialogue.false_text, height=self.height, command=EasyDialogue.no_clicked, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize))
        # self.no_button.grid(row=0, column=1, padx=self.padx, pady=self.pady)
        self.none_button.pack(side="left", fill="both")
        EasyDialogue.select_none_buttons.append(self.none_button)
        # self.no_frame.pack(side="left", fill="both", expand=fill_frame)
        self.none_frame.grid(row=0, column=1, padx=self.padx, pady=self.pady)
        self.none_frame.pack_propagate(False)

        self.grid_object.grid_propagate(True)
        self.grid_object.grid_propagate(False)
        self.grid_object.rowconfigure(0, weight=1)
        self.grid_object.columnconfigure(0, weight=1)
        self.grid_object.columnconfigure(1, weight=1)

        if self.focus:
            self.select_button.focus_set()

        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)


class EasyYesNoButtons(EasyWidget):

    def __init__(self, EasyDialogue, row=None, column=0, columnspan=1, focus=True, frame=None, fill_frame=False):

        EasyWidget.__init__(self)
        self.assign_values(EasyDialogue, locals())

        self.grid_object = tkinter.Frame(self.frame, width=self.width, height=self.height, background=self.background_color)
        self.yes_frame = tkinter.Frame(self.grid_object, width=self.width/2, height=self.height, background=self.background_color)
        if len(EasyDialogue.yes_text) < 13:
            self.yes_button = tk.Button(self.yes_frame, text=EasyDialogue.yes_text, width=10, command=EasyDialogue.yes_clicked, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize))
        else:
            self.yes_button = tk.Button(self.yes_frame, text=EasyDialogue.yes_text, command=EasyDialogue.yes_clicked, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize))
        # self.yes_button.grid(row=0, column=0, padx=self.padx, pady=self.pady)
        self.yes_button.pack(side="right", fill="both")
        EasyDialogue.yes_no_buttons.append(self.yes_button)
        # self.yes_frame.pack(side="left", fill="both", expand=fill_frame)
        self.yes_frame.grid(row=0, column=0, padx=self.padx, pady=self.pady)
        self.yes_frame.pack_propagate(False)

        self.no_frame = tkinter.Frame(self.grid_object, width=self.width/2, height=self.height, background=self.background_color)
        if len(EasyDialogue.no_text) < 13:
            self.no_button = tk.Button(self.no_frame, text=EasyDialogue.no_text, width=10, command=EasyDialogue.no_clicked, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize))
        else:
            self.no_button = tk.Button(self.no_frame, text=EasyDialogue.no_text, command=EasyDialogue.no_clicked, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize))
        # self.no_button.grid(row=0, column=1, padx=self.padx, pady=self.pady)
        self.no_button.pack(side="left", fill="both")
        EasyDialogue.yes_no_buttons.append(self.no_button)
        # self.no_frame.pack(side="left", fill="both", expand=fill_frame)
        self.no_frame.grid(row=0, column=1, padx=self.padx, pady=self.pady)
        self.no_frame.pack_propagate(False)

        self.grid_object.grid_propagate(True)
        self.grid_object.rowconfigure(0, weight=1)
        self.grid_object.columnconfigure(0, weight=1)
        self.grid_object.columnconfigure(1, weight=1)

        if self.focus:
            self.yes_button.focus_set()

        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)


class EasyOkCancelButtons(EasyWidget):

    def __init__(self, EasyDialogue, row=None, column=0, columnspan=1, focus=True, frame=None, fill_frame=False):

        EasyWidget.__init__(self)
        self.assign_values(EasyDialogue, locals())

        self.grid_object = tkinter.Frame(self.frame, width=self.width, height=self.height, background=self.background_color)
        self.ok_frame = tkinter.Frame(self.grid_object, width=self.width/2, height=self.height, background=self.background_color)
        if len(EasyDialogue.ok_text) < 13:
            self.ok_button = tk.Button(self.ok_frame, text=EasyDialogue.ok_text, width=10, command=EasyDialogue.yes_clicked, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize))
        else:
            self.ok_button = tk.Button(self.ok_frame, text=EasyDialogue.ok_text, command=EasyDialogue.yes_clicked, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize))
        # self.yes_button.grid(row=0, column=0, padx=self.padx, pady=self.pady)
        self.ok_button.pack(side="right", fill="both")
        EasyDialogue.ok_cancel_buttons.append(self.ok_button)
        # self.ok_frame.pack(side="left", fill="both", expand=fill_frame)
        self.ok_frame.grid(row=0, column=0, padx=self.padx, pady=self.pady)
        self.ok_frame.pack_propagate(False)

        self.cancel_frame = tkinter.Frame(self.grid_object, width=self.width/2, height=self.height, background=self.background_color)
        if len(EasyDialogue.cancel_text) < 13:
            self.cancel_button = tk.Button(self.cancel_frame, text=EasyDialogue.cancel_text, width=10, command=EasyDialogue.cancel_clicked, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize))
        else:
            self.cancel_button = tk.Button(self.cancel_frame, text=EasyDialogue.cancel_text, command=EasyDialogue.cancel_clicked, background=self.background_color, font=(EasyDialogue.font, EasyDialogue.fontsize))
        # self.cancel_button.grid(row=0, column=1, padx=self.padx, pady=self.pady)
        self.cancel_button.pack(side="left", fill="both")
        EasyDialogue.ok_cancel_buttons.append(self.cancel_button)
        # self.cancel_frame.pack(side="left", fill="both", expand=fill_frame)
        self.cancel_frame.grid(row=0, column=1, padx=self.padx, pady=self.pady)
        self.cancel_frame.pack_propagate(False)

        self.grid_object.grid_propagate(True)
        self.grid_object.rowconfigure(0, weight=1)
        self.grid_object.columnconfigure(0, weight=1)
        self.grid_object.columnconfigure(1, weight=1)

        if self.focus:
            self.ok_button.focus_set()

        self.insert_into_grid(self.grid_object, self.frame, self.row, self.column, self.columnspan)


class EasyLogo(EasyWidget):

    def __init__(self, EasyDialogue, frame=None):

        EasyWidget.__init__(self)
        self.EasyDialogue = EasyDialogue

        if frame is None:
            self.frame = EasyDialogue.main_frame
        else:
            if isinstance(frame, EasyLabelFrame) or isinstance(frame, EasyFrame):
                frame = frame.object
                self.frame = frame
            else:
                self.frame = frame

        logo_path = os.path.join(module_path, "images", "easytk_logo.png")
        logo_original = Image.open(logo_path)
        original_image_width_to_height_ratio = logo_original.size[0] / logo_original.size[1]
        self.image_height = 50
        self.image_width = round(self.height * original_image_width_to_height_ratio)
        resized = logo_original.resize((self.image_width, self.image_height))
        EasyDialogue.logo = ImageTk.PhotoImage(resized)
        self.grid_object = tkinter.Frame(self.frame, background=self.background_color, width=self.image_width, height=self.image_height)
        self.object = tkinter.Label(self.grid_object, image=EasyDialogue.logo, width=self.image_width, height=self.image_height, background=self.background_color)
        self.object.pack()
        self.grid_object.pack_propagate(False)
        self.insert_into_grid(self.grid_object, self.frame, row=1, column=0, columnspan=1)
