import os
import easytk

testGui = easytk.Window(window_type="SelectionFalse")
testGui.config(title="123")
testGui.add_entry(title="Test Entry")
testGui.add_file_dialogue("Choose your file: ")
testGui.add_dir_dialogue("Choose your directory:")
testGui.add_combobox(["Value 1", "Value 2", "Value 3"], title="Test Combobox")
testGui.add_label("Test Label")
testGui.add_checkbutton("Test Checkbutton", on=True)
return_values = testGui.show()

print("Return values: ", return_values)