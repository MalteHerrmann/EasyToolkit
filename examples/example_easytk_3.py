import os
import easytk

test_gui = easytk.Window(window_type="SelectionFalse")
test_gui.add_label("A veeery simple GUI - just choose one of the listed values:")
test_frame = test_gui.add_label_frame("Simple Input")
# test_frame = test_gui.add_frame()
test_gui.add_combobox(["Item 1", "Item 2"], title="Test-Combo", frame=test_frame)
return_values = test_gui.show()
print("Returned values: ", return_values)