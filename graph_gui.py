import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, StringVar, IntVar, Entry, filedialog, Listbox
from tkinter import ttk
from csv_create import main_call

# Global list to store selected folders
selected_folders = []

# Function to browse and select folders
def browse_folders():
    folder_path = filedialog.askdirectory()
    if folder_path:
        file_listbox.insert('end', folder_path)  # Corrected here

# Function to add selected folders to the array
def add_folders_to_array():
    global selected_folders
    selected_folders = file_listbox.get(0, 'end')
    print("Selected folders added:", selected_folders)  # For debugging
    csv_mole_weight_creation()
    
def csv_mole_weight_creation():
    main_call(selected_folders)

def load_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path)
        column_names = df.columns.tolist()
        update_options(column_names)

def update_options(columns):
    x_column_menu['menu'].delete(0, 'end')
    y_column_menu['menu'].delete(0, 'end')
    
    for column in columns:
        x_column_menu['menu'].add_command(label=column, command=lambda value=column: x_column_var.set(value))
        y_column_menu['menu'].add_command(label=column, command=lambda value=column: y_column_var.set(value))

def plot_data():
    x_col = x_column_var.get()
    y_col = y_column_var.get()
    num_plots = int(num_plots_var.get())
    
    if not x_col or not y_col:
        return
    
    plt.figure(figsize=(10, 6))
    unique_names = df['Name'].unique()
    
    for name in unique_names[:num_plots]:
        subset = df[df['Name'] == name]
        plt.plot(subset[x_col], subset[y_col], label=name)

    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f'Plot of {y_col} vs {x_col}')
    plt.legend()
    plt.show()

# Create GUI
root = Tk()
root.title("CSV Plotter")

# Frame for file selection
file_frame = ttk.Frame(root)
file_frame.pack(pady=10)

# Label for the selected folders
file_label = ttk.Label(file_frame, text="Selected Folders:")
file_label.pack(side='left', padx=10)

# Listbox to display the selected folders
file_listbox = Listbox(file_frame, width=50, height=10)
file_listbox.pack(side='left', padx=10)

# Browse button to select folders
browse_button = ttk.Button(file_frame, text="Browse", command=browse_folders)
browse_button.pack(side='left', padx=10)

# Button to add selected folders to the array
add_folders_button = ttk.Button(root, text="Create CSV with Selected Folders", command=add_folders_to_array)
add_folders_button.pack(pady=40)

df = pd.DataFrame()

# File loading
load_button = Button(root, text="Load CSV File", command=load_file)
load_button.pack(pady=5)

# Column selection
x_column_var = StringVar()
y_column_var = StringVar()
num_plots_var = IntVar(value=5)

x_column_menu = ttk.OptionMenu(root, x_column_var, "")
x_column_menu.pack(pady=5)
x_column_menu.config(width=20)
y_column_menu = ttk.OptionMenu(root, y_column_var, "")
y_column_menu.pack(pady=5)
y_column_menu.config(width=20)

# Number of plots
num_plots_label = Label(root, text="Number of plots:")
num_plots_label.pack(pady=5)
num_plots_entry = Entry(root, textvariable=num_plots_var)
num_plots_entry.pack(pady=5)

# Plot button
plot_button = Button(root, text="Plot Data", command=plot_data)
plot_button.pack(pady=10)

root.mainloop()
