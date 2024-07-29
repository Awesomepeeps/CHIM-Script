import tkinter as tk
from tkinter import ttk
import platform
from run_chimxpt import *

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
    
    folder_name = f'{new_pH_entry.get():.3} pH {new_pFluid_entry.get():.3} pF {new_temp_entry.get():.3} °C {original_folder_entry.get()}'
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
    
    
    
# Setup for GUI
window = tk.Tk()
window.title('CHIM-XPT')
window.geometry('700x500')



# folder Name
original_folder_frame = ttk.Frame(window)
original_folder_frame.pack()

original_folder_name = tk.StringVar(value='Folder Name')

original_folder_entry = ttk.Entry(original_folder_frame, textvariable=original_folder_name)
original_folder_button = ttk.Button(original_folder_frame, text='Confirm Folder Name', command=create_original_folder)

original_folder_entry.pack(side='left', padx=10, pady=15)
original_folder_button.pack(pady=15)



# new conditions
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


# TODO: Add GUI for error recovery

# TODO: Add GUI for graphing

# running the GUI 
window.mainloop()


if __name__ == '__main__':
    if platform.system() == 'Windows' or platform.system() == 'Linux':
        # setup()
        print()
    else:
        raise OSError(f"Unsupported operating system: {platform.system()}")    
