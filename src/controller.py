import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import arm
import eer


class Controller():
    """
    A Controller class (as part of the MVC framework) used to manage the
    interaction between the user and the model.

    Instantiated with a view object that has the following components:
        1) A `txt_eer` text widget
        2) A `txt_arm` text widget
        3) A `btn_transform` button
        4) A `load_menu` menu item
        4) A `save_menu` menu item
    """

    def __init__(self, view):
        self.eer_filename = "No EER file selected yet"
        self.arm_filename = "No ARM file selected yet"
        self.eer_model = None  # will store the currently loaded EER model
        self.arm_model = None  # will store the currently loaded ARM model
        self.eer_loaded = False
        self.arm_loaded = False
        self.gui = view
        self.gui.load_menu.entryconfigure(0, command=self.open_eer_file_picker)
        self.gui.load_menu.entryconfigure(1, command=self.open_arm_file_picker)
        self.gui.save_menu.entryconfigure(0, command=self.save_EER)
        self.gui.save_menu.entryconfigure(1, command=self.save_ARM)
        self.gui.btn_transform.config(command=self.transform)

    def open_eer_file_picker(self):
        self.eer_filename = fd.askopenfilename(initialdir="/",
                                               title="Select file",
                                               filetypes=(
                                                   ("xml files", "*.xml"),
                                                   ("all files", "*.*")))
        if self.eer_filename != "":
            # Clears the text from start ("1.0") to end
            self.gui.txt_eer.delete("1.0", tk.END)
            self.gui.txt_arm.delete("1.0", tk.END)
            self.eer_model = eer.EER_Model()
            self.eer_model.load_eer(self.eer_filename)
            self.gui.txt_eer.insert(tk.END, self.eer_model.__str__())
            self.eer_loaded = True
            self.arm_loaded = False
            self.gui.btn_transform.config(text="Transform to ARM")
            self.gui.btn_transform.config(state="normal")
        else:
            # User clicked cancel
            self.eer_filename = "No EER file selected yet"

    def open_arm_file_picker(self):
        self.arm_filename = fd.askopenfilename(initialdir="/",
                                               title="Select file",
                                               filetypes=(
                                                   ("xml files", "*.xml"),
                                                   ("all files", "*.*")))
        if self.arm_filename != "":
            messagebox.showinfo("Load",
                                "File Directory Selected:\n{}"
                                .format(self.arm_filename))
        else:
            # User clicked cancel
            self.arm_filename = "No ARM file selected yet"

    def save_EER(self):
        if self.eer_loaded:
            f = fd.asksaveasfile(initialdir="/",
                                 title="Choose Name and Location to \
                                           Save Transformation Output",
                                 filetypes=(
                                     ("text files", "*.txt"),
                                     ("all files", "*.*")))
            f.write(self.eer_model.__str__())
            f.close()
            messagebox.showinfo("Save", "EER Model Saved ")
        else:
            messagebox.showinfo("Warning", "No EER Model to save")

    def save_ARM(self):
        if self.arm_loaded:
            f = fd.asksaveasfile(initialdir="/",
                                 title="Choose Name and Location to \
                                           Save Transformation Output",
                                 filetypes=(
                                     ("text files", "*.txt"),
                                     ("all files", "*.*")))
            f.write(self.arm_model.__str__())
            f.close()
            messagebox.showinfo("Save", "ARM Model Saved ")
        else:
            messagebox.showinfo("Warning", "No ARM model to save")

    def transform(self):
        if self.eer_loaded:
            self.arm_model = self.eer_model.transform_to_arm()
            self.gui.txt_arm.insert(tk.END, self.arm_model.__str__())
            self.gui.btn_transform.config(text="Transform")
            self.gui.btn_transform.config(state="disabled")
            self.arm_loaded = True
        elif self.arm_loaded:
            pass  # TO DO: Implement transform from ARM to EER
