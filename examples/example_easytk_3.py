import os
import easytk

test_gui = easytk.Window(window_type="SelectionFalse")
test_gui.add_label("A veeery simple GUI - just choose one of the listed values:")
test_gui.add_combobox(["Item 1", "Item 2"], title="Test-Combo")
return_values = test_gui.show()
print("Returned values: ", return_values)