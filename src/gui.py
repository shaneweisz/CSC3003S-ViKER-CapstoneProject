from tkinter import Label, Canvas, Button, Menu, filedialog, Tk, messagebox
import sys

X_SIZE = 825
Y_SIZE = 600


def main():
    window = Tk()
    window.title("ViKER Transformations")
    window.geometry('{}x{}'.format(X_SIZE, Y_SIZE))
    window.config(bg='black')  # set background color to black

    window.grid_rowconfigure(1, minsize=20)
    window.grid_columnconfigure(0, minsize=50)
    lbl_header = Label(window, text="ViKER Transformation Tool",
                       bg="black", fg="white", font=("Courier", 25))
    lbl_header.grid(row=0, column=2, columnspan=3)

    # EER Model Label and Canvas
    lbl_eer = Label(window, text="EER Model")
    lbl_eer.config(font=("Courier", 14))
    lbl_eer.grid(column=2, row=5)

    canvas_eer = Canvas(window, width=300, height=400, bg="white")
    canvas_eer.grid(column=2, row=7)

    # ARM Model Label and Canvas
    lbl_arm = Label(window, text="ARM Model")
    lbl_arm.config(font=("Courier", 14))
    lbl_arm.grid(column=4, row=5)

    canvas_arm = Canvas(window, width=300, height=400, bg="white")
    canvas_arm.grid(column=4, row=7)

    # Adds space between ARM/EER labels and respective canvas
    window.grid_rowconfigure(6, minsize=10)

    # Spacing between the models i.e. column 3 will be at least 50px wide
    window.grid_columnconfigure(3, minsize=50)

    # Menu for Loading and Saving

    root_menu = Menu(window)
    window.config(menu=root_menu)

    def open_file_picker():
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select file",
                                              filetypes=(
                                                  ("xml files", "*.xml"),
                                                  ("all files", "*.*")))
        messagebox.showinfo("Load", "File Directory Selected:\n{}".format(filename))

    load_menu = Menu(root_menu)
    root_menu.add_cascade(label="Load", menu=load_menu)
    load_menu.add_command(label="Load ARM", command=open_file_picker)
    load_menu.add_command(label="Load EER", command=open_file_picker)

    save_menu = Menu(root_menu)
    root_menu.add_cascade(label="Save", menu=save_menu)
    save_menu.add_command(label="Save ARM",
                          command=lambda: messagebox.showinfo(
                              "Save", "Save ARM Clicked"))
    save_menu.add_command(label="Save EER",
                          command=lambda: messagebox.showinfo(
                              "Save", "Save EER Clicked"))

    # Transform Button

    btn_transform = Button(window, text="Transform", font=("Courier, 20"))
    window.grid_rowconfigure(8, minsize=20)
    btn_transform.grid(row=9, column=2, columnspan=3, sticky='ew')

    # Help Button
    help_msg = "Consult Help PDF for transformation assistance."
    btn_help = Button(window, text="?", fg="blue",
                      command=lambda: messagebox.showinfo("Help", help_msg))
    btn_help.config(font=("Courier", 14))
    btn_help.grid(row=0, column=6)

    window.grid_columnconfigure(5, minsize=10)
    window.grid_columnconfigure(7, minsize=10)

    # Exit Button
    btn_exit = Button(window, text="Exit", fg="red",
                      command=lambda: window.quit())
    btn_exit.config(font=("Courier", 14))
    btn_exit.grid(row=0, column=8)

    window.mainloop()


if __name__ == "__main__":
    main()
