# TODO When going back still keep a copy of the previous files
# TODO When excluding minerals make it automaticall run previous run
# TODO Add remove minerals that are zeroing and use the mineral_exclusion_pop

import tkinter as tk
from tkinter import *
from tkinter import ttk
import platform
from run_chimxpt import *
    
checkbox_vars = []
mineral_list = []
mineral_list_percent = []

def create_original_folder():
    # Function call for 'Confirm Folder Name' button
    # Makes folder for the original RUN file provided by the user
    
    # Makes folder after getting and then passing in the name from 'original folder entry'
    folder_name = original_folder_entry.get()
    make_original_folder(folder_name)
    
    # Assings parameters to the entry filds in the window
    original_parameters()
    current_step_values()
    
    # Enables rest of the Buttons, Entries, and Texts
    state_change()

def state_change():
    # Helper function for 'create_original_folder
    
    original_folder_entry['state'] = 'disabled'
    original_folder_button['state'] = 'disabled'
    new_pH_entry['state'] = 'enabled'
    new_pFluid_entry['state'] = 'enabled'
    step_increment_entry['state'] = 'enabled'
    step_limit_entry['state'] = 'enabled'
    new_temp_entry['state'] = 'enabled'
    new_conditions_button['state'] = 'enabled'
    auto_increase_button['state'] = 'enabled'
    manually_increase_button['state'] = 'enabled'
    run_button['state'] = 'enabled'

def original_parameters():
    # Gets the original parameters from file that the user passed in and sets values to the pH, pFluid, and temp entries
    
    newpH, newpFluid, newtemp = get_parameters()
    pH_text.set(newpH)
    pFluid_text.set(newpFluid)
    temp_text.set(newtemp)

def current_step_values():
    # Gets the current step values from the RUN files sets values to the increment and limit entries
    
    newincrement, newlimit = get_current_step()
    increment_text.set(newincrement)
    limit_text.set(newlimit)
    
def make_new_folder():
    # Button call for 'Make New Folder'
    # Makes a name for folder with new conditions and passes it in to make a new RUN file
    
    if float(new_pH_entry.get()) >= 1000:
        new_ph_entry_name = f'{new_pH_entry.get()}'
    else:
        new_ph_entry_name = f'{new_pH_entry.get():.3}'
        
    if float(new_pFluid_entry.get()) >= 1000:
        new_pFluid_entry_name = f'{new_pFluid_entry.get()}'
    else:
        new_pFluid_entry_name = f'{new_pFluid_entry.get():.3}'
        
    if float(new_temp_entry.get()) >= 1000:
        new_temp_entry_name = f'{new_temp_entry.get()}'
    else:
        new_temp_entry_name = f'{new_temp_entry.get():.3}'
    
    folder_name = f'{new_ph_entry_name} pH {new_pFluid_entry_name} pF {new_temp_entry_name} °C {original_folder_entry.get()}'
    make_new_condition(folder_name, float(pH_text.get()), float(pFluid_text.get()), float(temp_text.get()))
    
def auto_increase_step():
    # Button call for 'Auto Increase by 10x'
    # Automatically increase step increm and limit by 10 and then updates the text
    
    auto_step_increase()
    new_increm, new_limit = get_current_step()
    increment_text.set(new_increm)
    limit_text.set(new_limit)
    
def manual_increase_step():
    # Button call for 'Load Manual Increase'
    # Manually increase step increm and limit and then updates the text

    increment_change = float(step_increment_entry.get())
    limit_change = float(step_limit_entry.get())
    manual_step_increase(increment_change, limit_change)
    new_increm, new_limit = get_current_step()
    increment_text.set(new_increm)
    limit_text.set(new_limit)

def previous_chimrun():
    # Button call for Previous Run
    # Reverts all CHIMRUN to the run right before this one (mainly for ERROR recovery)
        
    # Disables auto and previous button to prevent repetition
    previous_button['state'] = 'disabled'
    auto_increase_button['state'] = 'disabled'
    
    # Sets current run to one lower
    previous_counter = run_counter_text.get().strip().split()
    current_run = int(previous_counter[1]) - 1
    run_counter_text.set(f'Run {current_run}')
    
    # Calls function and updates increm and limit entry text
    revert_to_previous()
    get_current_step()

def chimrun():
    global mineral_list, checkbox_vars, mineral_list_percent
    
    # Button call for Run
    # Runs the CHIM-XPT program
    
    # Enables previous and auto if they were disables
    run_button['state'] = 'disabled'
    previous_button['state'] = 'enabled'
    auto_increase_button['state'] = 'enabled'
    
    # Runs the code and sets the current run text
    counter = run_chimxpt() # Returns the current run
    run_counter_text.set(f'Run {counter}')
    get_current_step()
    run_button['state'] = 'enabled'
    
    mineral_list, mineral_list_percent = new_mineral()
    print("Mineral list:", mineral_list)
    mineral_exclusion_pop(mineral_list)
    checkbox_vars = []
    
def mineral_exclusion_pop(mineral_exclusion_list):
    top = Toplevel(window)
    top.title("Select Minerals to Exclude")
    tk.Label(top, text="Select the minerals you want to exclude:").pack()
    top.title('Mineral Exclusion')

    print(mineral_list)
    print(mineral_list_percent)

    for count, mineral in enumerate(mineral_list):
        check_var = tk.IntVar()
        checkbox_vars.append(check_var)
        mineral_text = f'Mineral: {mineral}, Weight Percent: {mineral_list_percent[count]}%'
        check = tk.Checkbutton(top, text=mineral_text, variable=check_var,
                            command=lambda var=check_var: print(var.get()))
        check.pack(anchor='w')

        '''print(checkbox_vars)
        print(check_var)
        print(check_var.get())
        check_var.set('On')
        print(check_var.get())'''
        
    confirm_button = tk.Button(top, text="Confirm", command=lambda: on_confirm(top))
    confirm_button.pack()
    
    top.mainloop()
    
def on_confirm(top):
    global mineral_list
    
    if len(checkbox_vars) != 0:
        selected_minerals = [mineral_list[i] for i, var in enumerate(checkbox_vars) if var.get() == 1]
    else:
        print("No new minerals")
        checkbox_vars.clear()
        top.destroy()
        return
    
    if not selected_minerals:
        print('No Minerals Selected')
        checkbox_vars.clear()
        top.destroy()
        return
    else: 
        print("Selected minerals: ", selected_minerals)
        print('Going to previous run')
        previous_chimrun()
        update_suppress_list(selected_minerals)
        checkbox_vars.clear()
        top.destroy()

'''
def find_zeroing_minerals():
    zero_mineral_list = minerals_zeroing()
    
    top = Toplevel(window)
    top.title("Select Minerals to Exclude")
    tk.Label(top, text="Select the minerals you want to exclude:").pack()
    top.title('Mineral Exclusion')

    for count, mineral in enumerate(zero_mineral_list):
        check_var = tk.IntVar()
        checkbox_vars.append(check_var)
        check = tk.Checkbutton(top, text=mineral, variable=check_var,
                            command=lambda var=check_var: print(var.get()))
        check.pack(anchor='w')

        'print(checkbox_vars)
        print(check_var)
        print(check_var.get())
        check_var.set('On')
        print(check_var.get())'
        
    confirm_button = tk.Button(top, text="Confirm", command=lambda: on_confirm(top))
    confirm_button.pack()

    top.mainloop()
'''

# Setup for GUI
window = tk.Tk()
window.title('CHIM-XPT')
window.geometry('700x500')



# Folder Name
original_folder_frame = ttk.Frame(window)
original_folder_frame.pack()

original_folder_name = tk.StringVar(value='Folder Name')

original_folder_entry = ttk.Entry(original_folder_frame, textvariable=original_folder_name)
original_folder_button = ttk.Button(original_folder_frame, text='Confirm Folder Name', command=create_original_folder)

original_folder_entry.pack(side='left', padx=10, pady=15)
original_folder_button.pack(pady=15)



# New Conditions
new_conditions_frame = ttk.Frame(window)

pH_text = tk.StringVar(value='pH')
pFluid_text = tk.StringVar(value='pFluid')
temp_text = tk.StringVar(value='Temp')

new_pH = ttk.Label(new_conditions_frame, text='pH')
new_pFluid = ttk.Label(new_conditions_frame, text='pFliud')
new_temp = ttk.Label(new_conditions_frame, text='Temp')

new_pH_entry = ttk.Entry(new_conditions_frame, textvariable=pH_text)
new_pFluid_entry = ttk.Entry(new_conditions_frame, textvariable=pFluid_text)
new_temp_entry = ttk.Entry(new_conditions_frame, textvariable=temp_text)

new_pH_entry['state'] = 'disabled'
new_pFluid_entry['state'] = 'disabled'
new_temp_entry['state'] = 'disabled'

new_conditions_button = ttk.Button(new_conditions_frame, text='Make New Folder', command=make_new_folder)

new_pH.grid(row=0, column=0, padx=5, pady=5)
new_pFluid.grid(row=0, column=1, padx=5, pady=5)
new_temp.grid(row=0, column=2, padx=5, pady=5)

new_pH_entry.grid(row=1, column=0, padx=5, pady=5)
new_pFluid_entry.grid(row=1, column=1, padx=5, pady=5)
new_temp_entry.grid(row=1, column=2, padx=5, pady=5)

new_conditions_button.grid(row=2, column=1, columnspan=1, pady=10)

new_conditions_frame.pack(padx=10, pady=10)



# Step Conditions
step_frame = ttk.Frame(window)


auto_increase_button = ttk.Button(step_frame, text='Auto Increase by 10x', command=auto_increase_step)
manually_increase_button = ttk.Button(step_frame, text='Load Manual Increase', command=manual_increase_step)

run_counter_text = tk.StringVar(value='Run 0')
increment_text = tk.StringVar(value='increment')
limit_text = tk.StringVar(value='limit')

step_increment_label = ttk.Label(step_frame, text='Step Increment')
step_limit_label = ttk.Label(step_frame, text='Step Limit')
run_label = ttk.Label(step_frame, textvariable=run_counter_text)

step_increment_entry = ttk.Entry(step_frame, textvariable=increment_text)
step_limit_entry = ttk.Entry(step_frame, textvariable=limit_text)

previous_button = ttk.Button(step_frame, text='Previous Run', command=previous_chimrun)
run_button = ttk.Button(step_frame, text='Run', command=chimrun)

auto_increase_button.grid(row=0, column=0, padx=5, pady=15)
manually_increase_button.grid(row=0, column=2, padx=5, pady=15)
step_increment_label.grid(row=1, column=0, padx=5, pady=5)
step_limit_label.grid(row=1, column=2, padx=5, pady=5)
step_increment_entry.grid(row=2, column=0, padx=5, pady=5)
step_limit_entry.grid(row=2, column=2, padx=5, pady=5)
previous_button.grid(row=3, column=0, pady=30)
run_button.grid(row=3, column=2, pady=30)
run_label.grid(row=3, column=1, pady=30)

step_frame.pack()
step_increment_entry['state'] = 'disabled'
step_limit_entry['state'] = 'disabled'



# Setting Starting States
new_conditions_button['state'] = 'disabled'
auto_increase_button['state'] = 'disabled'
manually_increase_button['state'] = 'disabled'
previous_button['state'] = 'disabled'
run_button['state'] = 'disabled'



# Zeroing Mineral
# find_zeroing_minerals_button = ttk.Button(window, text='Find Zeroing Minerals', command=find_zeroing_minerals)
# find_zeroing_minerals_button.pack(pady=20)



# Running the GUI 
window.mainloop()


# Checking for user OS
if __name__ == '__main__':
    if platform.system() == 'Windows' or platform.system() == 'Linux':
        print()
    else:
        raise OSError(f"Unsupported operating system: {platform.system()}")    
