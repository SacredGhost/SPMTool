import tkinter as tk

class SPM_Multi:
    def __init__(self, master):
        self.padding = 5
        self.master = master
        self.master.title("SPM Multi")
        self.master.configure(bg="light grey")

        # Set padding for the main window
        self.master.grid_rowconfigure(0, minsize=self.padding)
        self.master.grid_columnconfigure(0, minsize=self.padding)
        self.master.grid_rowconfigure(2, minsize=self.padding)
        self.master.grid_columnconfigure(2, minsize=self.padding)

        # Configure the grid layout
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=0)

        # Create the text box
        self.text_box = tk.Text(self.master, width=50, height=20, state='disabled')
        self.text_box.grid(row=0, column=0, padx=self.padding, pady=self.padding, sticky="nsew")

        # Create a scroll bar for the text box
        self.scrollbar = tk.Scrollbar(self.master, command=self.text_box.yview)
        self.scrollbar.grid(row=0, column=1, padx=self.padding, pady=self.padding, sticky="nsw")

        # Connect the scroll bar to the text box
        self.text_box.config(yscrollcommand=self.scrollbar.set)

        # Create the input field
        self.input_field = tk.Entry(self.master, width=50)
        self.input_field.grid(row=1, column=0, columnspan=2, padx=self.padding, pady=self.padding, sticky="ew")
        self.input_field.bind("<Return>", self.send_text)  # Bind the <Return> event to the send_text method

    def send_text(self, event=None):
        text = self.input_field.get()
        self.text_box.configure(state='normal')
        self.text_box.insert(tk.END, text + "\n")
        self.text_box.configure(state='disabled')
        self.input_field.delete(0, tk.END)
        self.text_box.see(tk.END)  # Scroll to the end of the text box

if __name__ == "__main__":
    root = tk.Tk()
    app = SPM_Multi(root)
    root.mainloop()
