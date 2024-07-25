import tkinter as tk
from run_chimxpt import new_mineral, update_suppress_list

checkbox_vars = []
mineral_list = []

def on_confirm(root):
    selected_minerals = [mineral_list[i] for i, var in enumerate(checkbox_vars) if var.get() == 1]
    print("Selected minerals: ", selected_minerals)
    update_suppress_list(selected_minerals)
    root.destroy()

def on_god():
    print("Var list contents: ", [var.get() for var in checkbox_vars])

root = tk.Tk()
root.title("Select Minerals to Exclude")

tk.Label(root, text="Select the minerals you want to exclude:").pack()
    
mineral_list = new_mineral()
print("Mineral list:", mineral_list)

for mineral in mineral_list:
    var = tk.IntVar(value=1)
    checkbox = tk.Checkbutton(root, text=mineral, variable=var)
    checkbox.pack(anchor='w')
    checkbox_vars.append(var)

confirm_button = tk.Button(root, text="Confirm", command=lambda: on_god())
confirm_button.pack()

root.mainloop()