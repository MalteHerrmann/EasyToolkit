import os
import sys
import easytk

def test():
    print("Testbutton")

def quit():
    sys.exit()

test_gui = easytk.Window(window_type="Message")
test_gui.config(width=200)
label = test_gui.add_label("Example GUI with multiple Buttons", row=0, column=0, columnspan=2)
label.object.config(font="bold")
frame_1 = test_gui.add_label_frame("Frame 1", row=1, column=0)
test_gui.add_button(text="Button 1.1", command=test, frame=frame_1)
test_gui.add_button(text="Button 1.2", command=test, frame=frame_1)
frame_2 = test_gui.add_label_frame("Frame 2", row=1, column=1)
test_gui.add_button(text="Button 2.1", command=test, frame=frame_2)
test_gui.add_button(text="Button 2.2", command=test, frame=frame_2)
frame_3 = test_gui.add_label_frame("Frame 3", columnspan=2)
test_gui.add_button(text="Button 3.1", command=test, frame=frame_3)
test_gui.add_button(text="Button 3.2", command=test, frame=frame_3)
test_gui.add_button(text="Button 3.3", command=test, frame=frame_3)
quit_button = test_gui.add_button(text="Exit", command=quit, columnspan=2, fill_frame=False)
quit_button.object.config(background="lightgrey", width=25)
test_gui.show()
