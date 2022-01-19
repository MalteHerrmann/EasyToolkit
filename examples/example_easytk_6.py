import os
import easytk


values = ["Value 1", "Value 2", "Value 3"]

testGui = easytk.Window(window_type="SelectionFalse")
testGui.config(width=550)
test_listbox = testGui.add_listbox(values, text="Single Selection")
test_listbox.set("Value 4")
multiple_selection_listbox = testGui.add_listbox(values, text="Multiple Selection", select_mode="multiple")
extended_selection_listbox = testGui.add_listbox(values, text="Extended Selection", select_mode="extended")
return_values = testGui.show()
print("Returned values: ", return_values)
