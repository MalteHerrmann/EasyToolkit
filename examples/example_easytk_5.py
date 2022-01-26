import os
import easytk
module_path = os.path.dirname(os.path.dirname(__file__))


testGui = easytk.Window(window_type="SelectionFalse")
first_frame = testGui.add_label_frame("Entries 1", width=350, column=0, row=0)
testGui.add_checkbutton("Button Text", on=True, frame=first_frame)
testGui.add_combobox(["Value 1", "Value 2", "Value 3"], title="Title", frame=first_frame)
testGui.add_entry(title="Title", frame=first_frame)
testGui.add_file_dialogue("Choose file", frame=first_frame)
testGui.add_dir_dialogue("Choose folder", frame=first_frame)
testGui.add_save_file_dialogue("Choose path to save file to", frame=first_frame)
second_frame = testGui.add_label_frame("Entries 2", width=150, column=1, row=0)
myimage = testGui.add_image(os.path.join(module_path, "images", "test.jpg"), width=100, height=100, frame=second_frame)
testGui.add_label("Test Label", frame=second_frame)
testGui.add_text("This is a longer text, which automatically extends to the next row. Unfortunately, tkinter does not care if it cuts a word in half in that process, so this has to be handled manually.", height=70, frame=second_frame)
return_values = testGui.show()
print("Returned values: ", return_values)
