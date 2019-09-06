import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

X_SIZE = 850
Y_SIZE = 600
FONT = 'Courier'


class GUI(tk.Frame):
    '''
    A class that construct the appearance of the core GUI of the application.

    Attributes
    ----------
    window : tk.Tk
        A top-level widget for the main window of the application
    txt_eer : tk.Text
        A text widget for displaying the EER Model
    txt_arm : tk.Text
        A text widget for displaying the ARM Model
    load_menu : tk.Menu
        A menu object providing load ARM and load EER options
    save_menu : tk.Menu
        A menu object providing save ARM and save EER options
    btn_transform : tk.Button
        A button clicked to transform from ARM to EER and vice versa.
    '''

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Basic Frame Options - Title, Size, Background Colour
        self.window = parent
        self.window.title("ViKER Transformations")
        self.window.geometry('{}x{}'.format(X_SIZE, Y_SIZE))
        self.window.config(bg='black')  # set background color to black

        self.window.grid_rowconfigure(1, minsize=20)  # space below heading
        self.window.grid_columnconfigure(0, minsize=100)  # left padding space
        lbl_header = tk.Label(self.window,
                              text="ViKER Transformation Tool",
                              bg="black",
                              fg="white",
                              font=(FONT, 25))
        lbl_header.grid(row=0, column=2, columnspan=3)

        # EER Model Label and Text Area
        lbl_eer = tk.Label(self.window, text="EER Model")
        lbl_eer.config(font=(FONT, 14))
        lbl_eer.grid(column=2, row=2)
        frm_txtcontainer_eer = tk.Frame(self.window,
                                        borderwidth=1,
                                        relief="sunken")
        self.txt_eer = tk.Text(frm_txtcontainer_eer,
                               wrap='none',
                               width=40,
                               height=27,
                               bg="white")
        text_vsb_eer = tk.Scrollbar(frm_txtcontainer_eer,
                                    orient="vertical",
                                    command=self.txt_eer.yview)
        text_hsb_eer = tk.Scrollbar(frm_txtcontainer_eer,
                                    orient="horizontal",
                                    command=self.txt_eer.xview)
        self.txt_eer.configure(yscrollcommand=text_vsb_eer.set,
                               xscrollcommand=text_hsb_eer.set)
        self.txt_eer.grid(row=0, column=0, sticky="nsew")
        text_vsb_eer.grid(row=0, column=1, sticky="ns")
        text_hsb_eer.grid(row=1, column=0, sticky="ew")
        frm_txtcontainer_eer.grid(column=2, row=4)

        # ARM Model Label and Text Area
        lbl_arm = tk.Label(self.window, text="ARM Model")
        lbl_arm.config(font=(FONT, 14))
        lbl_arm.grid(column=4, row=2)
        frm_txtcontainer_arm = tk.Frame(self.window,
                                        borderwidth=1,
                                        relief="sunken")
        self.txt_arm = tk.Text(frm_txtcontainer_arm,
                               wrap='none',
                               width=40,
                               height=27,
                               bg="white")
        text_vsb_arm = tk.Scrollbar(frm_txtcontainer_arm,
                                    orient="vertical",
                                    command=self.txt_arm.yview)
        text_hsb_arm = tk.Scrollbar(frm_txtcontainer_arm,
                                    orient="horizontal",
                                    command=self.txt_arm.xview)
        self.txt_arm.configure(yscrollcommand=text_vsb_arm.set, xscrollcommand=text_hsb_arm.set)
        self.txt_arm.grid(row=0, column=0, sticky="nsew")
        text_vsb_arm.grid(row=0, column=1, sticky="ns")
        text_hsb_arm.grid(row=1, column=0, sticky="ew")
        frm_txtcontainer_arm.grid(column=4, row=4)

        # Adds space between ARM/EER labels and respective canvas
        self.window.grid_rowconfigure(3, minsize=10)

        # Spacing between the models i.e. column 3 will be at least 50px wide
        self.window.grid_columnconfigure(3, minsize=50)

        # Root Menu
        self.root_menu = tk.Menu(self.window)
        self.window.config(menu=self.root_menu)

        # Load Menu
        self.load_menu = tk.Menu(self.root_menu)

        # Save Menu
        self.save_menu = tk.Menu(self.root_menu)

        # Transform Button
        self.btn_transform = tk.Button(self.window,
                                       text="Transform",
                                       font=(FONT, 20))
        self.btn_transform.config(state='disabled')
        self.window.grid_rowconfigure(8, minsize=20)
        self.btn_transform.grid(row=9, column=2, columnspan=3, sticky='ew')

        # Help Button
        help_msg = "1. Click the Load Menu Item to load a EER or ARM XML file.\n"
        help_msg += "2. Click the Transform Button to transform a loaded model.\n"
        help_msg += "3. Click the Save Menu Item to save a model.\n"
        help_msg += "4. Consult the User Manual for further assistance."
        btn_help = tk.Button(self.window,
                             text="?",
                             fg="blue",
                             command=lambda: messagebox.showinfo("Help",
                                                                 help_msg))
        btn_help.config(font=(FONT, 14))
        btn_help.grid(row=0, column=6)

        # Spacing between the Help and Exit Buttons
        self.window.grid_columnconfigure(5, minsize=10)
        self.window.grid_columnconfigure(7, minsize=10)

        # Exit Button
        btn_exit = tk.Button(self.window,
                             text="Exit",
                             fg="red",
                             command=lambda: self.window.quit() if messagebox.askyesno("Exit", "Are you sure you wish to exit?", icon='warning') is True else None)
        btn_exit.config(font=(FONT, 14))
        btn_exit.grid(row=0, column=8)


# View the static GUI
if __name__ == '__main__':
    gui = GUI(tk.Tk())
    gui.window.mainloop()
