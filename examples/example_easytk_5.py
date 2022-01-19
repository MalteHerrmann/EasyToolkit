import os
import easytk
module_path = os.path.dirname(os.path.dirname(__file__))

testGui = easytk.Window(window_type="SelectionFalse")
testGui.add_checkbutton("Button Text", on=True)
testGui.add_combobox(["Value 1", "Value 2", "Value 3"], title="Title")
testGui.add_entry(title="Title")
testGui.add_file_dialogue("Choose file")
testGui.add_dir_dialogue("Choose folder")
testGui.add_save_file_dialogue("Choose path to save file to")
myimage = testGui.add_image(os.path.join(module_path, "images", "test.jpg"), width=100, height=100)
testGui.add_label("Test Label")
testGui.add_text("This is a longer text, which automatically extends to the next row. Unfortunately, tkinter does not care if it cuts a word in half in that process, so this has to be handled manually.", height=70)
return_values = testGui.show()
print("Returned values: ", return_values)
