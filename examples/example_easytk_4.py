import os
import easytk

test_gui = easytk.Window(window_type="SelectionFalse")
test_gui.config(width=450)
test_gui.config(label_width=20)
test_gui.add_entry("Test Entry.")
test_gui.add_file_dialogue("PNG File (*.png)", filetypes=("Portable Network Graphics (*.png)", "*.png"))
return_values = test_gui.show()
print("Returned values: ", return_values)