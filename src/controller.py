import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from arm import ARM_Attribute, ARM_Entity, ARM_Model
import eer


class Controller():
    """
    A Controller class (as part of the MVC framework) used to manage the
    interaction between the user and the model.

    Attributes
    ----------
    view : an object with the following features
        a display_EER(text) method
        a display_ARM(text) method
        a load_ARM() method that returns the filename of an ARM file
        a load_EER() method that returns the filename of an EER file

    Methods
    -------
    load_arm():
        Populates the ARM model object from an XML file


    """

    def __init__(self, gui):
        self.eer_filename = "No EER file selected yet"
        self.arm_filename = "No ARM file selected yet"
        self.eer_model = None  # will store the currently loaded EER model
        self.arm_model = None  # will store the currently loaded ARM model
        self.eer_loaded = False
        self.arm_loaded = False
        self.gui = gui
        self.gui.load_menu.entryconfigure(0, command=self.open_eer_file_picker)  # 1st menu item
        self.gui.load_menu.entryconfigure(1, command=self.open_arm_file_picker)  # 2nd menu item
        self.gui.save_menu.entryconfigure(0, command=self.save_EER)
        self.gui.save_menu.entryconfigure(1, command=self.save_ARM)
        self.gui.btn_transform.config(command=self.transform)

    def open_eer_file_picker(self):
        self.eer_filename = filedialog.askopenfilename(initialdir="/",
                                                       title="Select file",
                                                       filetypes=(
                                                           ("xml files", "*.xml"),
                                                           ("all files", "*.*")))
        if self.eer_filename != "":
            self.gui.txt_eer.delete("1.0", tk.END)  # clear the text from start to end
            self.gui.txt_arm.delete("1.0", tk.END)  # clear the text from start to end
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
        self.arm_filename = filedialog.askopenfilename(initialdir="/",
                                                       title="Select file",
                                                       filetypes=(
                                                           ("xml files", "*.xml"),
                                                           ("all files", "*.*")))
        if self.arm_filename != "":
            messagebox.showinfo("Load", "File Directory Selected:\n{}".format(self.arm_filename))
        else:
            # User clicked cancel
            self.arm_filename = "No ARM file selected yet"

    def save_EER(self):
        messagebox.showinfo("Save", "Save EER Clicked")

    def transform(self):
        if self.eer_loaded:
            self.arm_model = self.eer_model.transform_to_arm()
            self.gui.txt_arm.insert(tk.END, self.arm_model.__str__())
            self.gui.btn_transform.config(text="Transform")
            self.gui.btn_transform.config(state="disabled")
            self.arm_loaded = True
        elif self.arm_loaded:
            pass  # TO DO: Implement transform from ARM to EER

    def save_ARM(self):
        if self.arm_loaded:
            new_filename = self.eer_filename[:-4] + "_transformed.txt"
            f = open(new_filename, "w")
            f.write(self.arm_model.__str__())
            f.close()
            messagebox.showinfo("Save", "ARM Transformation Output Saved ")
        else:
            messagebox.showinfo("Save", "Save ARM Clicked")
