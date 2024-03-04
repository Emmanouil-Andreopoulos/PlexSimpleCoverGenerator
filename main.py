import os
import tkinter as tk
from tkinter import filedialog, ttk
import image_generator


class FolderSelector:
    def __init__(self, master):
        self.master = master
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)

        # Create the tabs
        self.select_tab = ttk.Frame(self.notebook)
        self.selected_tab = ttk.Frame(self.notebook)
        self.finish_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.select_tab, text='Select')
        self.notebook.add(self.selected_tab, text='Selected')
        self.notebook.add(self.finish_tab, text='Finish')

        # Populate the 'Select' tab
        # Create Treeview
        self.tree = ttk.Treeview(self.select_tab)
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Create scrollbar for the treeview
        self.tree_scrollbar = ttk.Scrollbar(self.select_tab, orient="vertical", command=self.tree.yview)
        self.tree_scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)

        self.folder_path = filedialog.askdirectory()
        self.insert_data()

        # Configure grid weights to make Treeview fill the window
        self.select_tab.grid_rowconfigure(0, weight=1)
        self.select_tab.grid_columnconfigure(0, weight=1)

        # Create the 'Continue' button below the Treeview
        self.continue_button = tk.Button(self.select_tab, text="Continue", command=self.get_selected)
        self.continue_button.grid(row=1, column=0, columnspan=2, pady=5)

        # Create the text area in the 'Selected' tab
        self.text_area = tk.Text(self.selected_tab)
        self.text_area.pack(expand=True, fill="both")
        self.text_area.config(state=tk.DISABLED)
        # Create the 'Continue' button below the text area
        self.continue_button = tk.Button(self.selected_tab, text="Continue", command=self.generate_selected)
        self.continue_button.pack()

        # Create the text area in the 'Finish' tab
        self.text_area2 = tk.Text(self.finish_tab)
        self.text_area2.pack(expand=True, fill="both")
        self.text_area2.config(state=tk.DISABLED)
        # Create the 'Exit' button in the 'Finish' tab
        self.generate_button = tk.Button(self.finish_tab, text="Exit", command=master.quit)
        self.generate_button.pack()

    def insert_data(self):
        self.tree.delete(*self.tree.get_children())
        for folder_name in os.listdir(self.folder_path):
            full_path = os.path.join(self.folder_path, folder_name)
            if os.path.isdir(full_path):
                self.tree.insert("", "end", text=folder_name, values=[full_path])

    def get_selected(self):
        selected_items = self.tree.selection()
        selected_paths = [self.tree.item(item)["values"][0] for item in selected_items]

        # Insert the selected paths into the text area
        self.text_area.config(state=tk.NORMAL)
        for path in selected_paths:
            self.text_area.insert(tk.END, path + "\n")
        self.text_area.config(state=tk.DISABLED)

        # Switch to the 'Selected' tab
        self.notebook.select(self.selected_tab)

    def generate_selected(self):
        selected_items = self.tree.selection()
        selected_paths = [self.tree.item(item)["values"][0] for item in selected_items]
        self.text_area2.config(state=tk.NORMAL)
        for path in selected_paths:
            self.text_area2.insert(tk.END, image_generator.generate_image(path) + "\n")
        self.text_area2.config(state=tk.DISABLED)
        # Switch to the 'Finish' tab
        self.notebook.select(self.finish_tab)


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)  # This line disables window resizing

    # Center the window
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    app = FolderSelector(root)
    root.mainloop()
