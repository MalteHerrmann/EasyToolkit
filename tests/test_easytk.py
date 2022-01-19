"""test_easytk | Malte Herrmann

Unit testing module for the EasyToolkit."""

import os
import unittest
module_path = os.path.dirname(os.path.dirname(__file__))

import easytk
from easytk import widgets


class TestEasyToolkitWindowTypes(unittest.TestCase):

    def test_yes_no_dialogue(self):
        window_type = "YesNo"
        self.dialogue = easytk.Window(window_type, testing=True)
        self.dialogue.show()
        self.assertEqual(self.dialogue.window_type, window_type)

    def test_selection_dialogue(self):
        window_type = "Selection"
        self.dialogue = easytk.Window(window_type, testing=True)
        self.dialogue.show()
        self.assertEqual(self.dialogue.window_type, window_type)

    def test_selection_none_dialogue(self):
        window_type = "SelectionFalse"
        self.dialogue = easytk.Window(window_type, testing=True)
        self.dialogue.show()
        self.assertEqual(self.dialogue.window_type, window_type)

    def test_ok_cancel_dialogue(self):
        window_type = "OkCancel"
        self.dialogue = easytk.Window(window_type, testing=True)
        self.dialogue.show()
        self.assertEqual(self.dialogue.window_type, window_type)

    def test_message_dialogue(self):
        window_type = "Message"
        self.dialogue = easytk.Window(window_type, testing=True)
        self.dialogue.show()
        self.assertEqual(self.dialogue.window_type, window_type)


class TestEasyToolkitWindow(unittest.TestCase):

    def setUp(self):
        self.dialogue = easytk.Window(testing=True)


    # Labels
    def test_label_can_be_added(self):
        added_label = self.dialogue.add_label("Test")
        self.assertEqual(len(self.dialogue.labels), 1)

    
    # Entries
    def test_entry_can_be_added(self):
        added_entry = self.dialogue.add_entry("Test", default_value="Default")
        self.assertEqual(len(self.dialogue.entries), 1)


    def test_entry_value_can_be_returned(self):
        added_entry = self.dialogue.add_entry("Test", default_value="Default")
        self.assertEqual(added_entry.get(), "Default")


    def test_entry_value_can_be_set(self):
        new_value = "Test"
        added_entry = self.dialogue.add_entry("Test", default_value="Default")
        added_entry.set(new_value)
        self.assertEqual(added_entry.get(), new_value)


    # Combobox
    def test_combobox_can_be_added(self):
        added_combobox = self.dialogue.add_combobox(["1", "2", "3"])
        self.assertEqual(len(self.dialogue.combos), 1)

    
    def test_combobox_value_can_be_returned(self):
        added_combobox = self.dialogue.add_combobox(["1", "2", "3"])
        self.assertEqual(added_combobox.get(), "1")

    
    def test_combobox_value_can_be_set(self):
        new_value = "Test"
        added_combobox = self.dialogue.add_combobox(["1", "2", "3"])
        added_combobox.set(new_value)
        self.assertEqual(added_combobox.get(), new_value)

    
    # Text
    def test_text_can_be_added(self):
        value = "Test"
        added_text = self.dialogue.add_text(value)
        self.assertEqual(len(self.dialogue.labels), 1)


    def test_text_can_be_returned(self):
        value = "Test"
        added_text = self.dialogue.add_text(value)
        self.assertEqual(added_text.get(), value)


    def test_text_can_be_set(self):
        value = "Test"
        added_text = self.dialogue.add_text("123")
        added_text.set(value)
        self.assertEqual(added_text.get(), value)


    # Checkbutton
    def test_checkbutton_can_be_added(self):
        value = True
        added_checkbutton = self.dialogue.add_checkbutton("Test", value)
        self.assertEqual(len(self.dialogue.checkbuttons), 1)
        self.assertIsInstance(added_checkbutton, widgets.EasyCheckbutton)


    def test_checkbutton_value_can_be_returned(self):
        value = True
        added_checkbutton = self.dialogue.add_checkbutton("Test", value)
        self.assertEqual(added_checkbutton.get(), value)


    def test_checkbutton_value_can_be_set(self):
        value = True
        added_checkbutton = self.dialogue.add_checkbutton("Test", not(value))
        added_checkbutton.set(value)
        self.assertEqual(added_checkbutton.get(), value)


    # Image
    def test_image_can_be_added(self):
        filepath = os.path.join(module_path, "images", "test.jpg")
        added_image = self.dialogue.add_image(filepath, width=200, height=200)
        self.assertEqual(len(self.dialogue.images), 1)
        self.assertIsInstance(added_image, widgets.EasyImage)


    # Label Frame
    def test_label_frame_can_be_added(self):
        title = "Test"
        added_label_frame = self.dialogue.add_label_frame(title)
        self.assertIsInstance(added_label_frame, widgets.EasyLabelFrame)


    # File Dialogue
    def test_file_dialogue_can_be_added(self):
        added_file_dialogue = self.dialogue.add_file_dialogue("123")
        self.assertIsInstance(added_file_dialogue, widgets.EasyFileDialogue)
        self.assertEqual(len(self.dialogue.entries), 1)


    def test_file_dialogue_value_can_be_returned(self):
        value = "Test"
        added_file_dialogue = self.dialogue.add_file_dialogue("123", default_value=value)
        self.assertEqual(added_file_dialogue.get(), value)


    def test_file_dialogue_value_can_be_set(self):
        value = "Test"
        added_file_dialogue = self.dialogue.add_file_dialogue("123", default_value="ABC")
        added_file_dialogue.set(value)
        self.assertEqual(added_file_dialogue.get(), value)


    # Button
    def test_button_can_be_added(self):
        added_button = self.dialogue.add_button("123", dummy_command)
        self.assertIsInstance(added_button, widgets.EasyButton)
        self.assertEqual(len(self.dialogue.custom_buttons), 1)


    # Frame
    def test_frame_can_be_added(self):
        added_frame = self.dialogue.add_frame()
        self.assertIsInstance(added_frame, widgets.EasyFrame)


    # Table
    def test_table_can_be_added(self):
        table_dict = {"1": "Test 1"}
        added_table = self.dialogue.add_table(table_dict)
        self.assertIsInstance(added_table, widgets.EasyTable)


    # Listbox
    def test_listbox_can_be_added(self):
        values = ["value 1", "value 2", "value 3"]
        added_listbox = self.dialogue.add_listbox(values)
        self.assertIsInstance(added_listbox, widgets.EasyListbox)

        
    def test_listbox_value_can_be_returned_single(self):
        values = ["value 1", "value 2", "value 3"]
        added_listbox = self.dialogue.add_listbox(values)
        self.assertEqual(added_listbox.get(), values[0])

        
    def test_listbox_value_can_be_set(self):
        values = ["value 1", "value 2", "value 3"]
        added_listbox = self.dialogue.add_listbox(values)
        added_listbox.set(values[1])
        self.assertEqual(added_listbox.get(), values[1])

        
    def test_listbox_new_value_can_be_inserted(self):
        values = ["value 1", "value 2", "value 3"]
        new_value = "value 4"
        added_listbox = self.dialogue.add_listbox(values)
        added_listbox.set(new_value)
        self.assertEqual(added_listbox.get(), new_value)


    def test_listbox_value_can_be_returned_multiple(self):
        values = ["value 1", "value 2", "value 3"]
        added_listbox = self.dialogue.add_listbox(values, select_mode="multiple")
        self.assertEqual(added_listbox.get(), [values[0]])


def dummy_command(*args, **kwargs):
    ...


if __name__ == "__main__":
    unittest.main()
