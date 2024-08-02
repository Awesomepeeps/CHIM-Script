import os
import subprocess
import shutil
import platform

folder_count = 1 # Keeps a count of how many folders there are (different conditions/RUN files)
current_run = 1 # Keeps track of what run the program is on
folder_names = [] # List of all the folder names
all_mineral_list = []

def run_chimxpt():
    """ 
    Runs the CHIM-XTP program with the file provided and any other modified files made after.
    Makes a copy of the RUN file before and after, the OUT file, the PLOT file, and a copy of the TERMINAL output.

    Args: 
        N/A

    Returns: 
        int: The current run that the program is on
    """ 
        
    global current_run, folder_names, folder_count

    # Loops through all versions of the CHIMRUN
    for i in range(folder_count):
        
        # Construct the current CHIMRUN version file name
        chimrun_version = f'CHIMRUN{i}.DAT'
        
        try:
            shutil.copy(chimrun_version, 'CHIMRUN.DAT')
        except FileNotFoundError:
            print(f"Source file '{chimrun_version}' not found.")
            continue
        except PermissionError:
            print(f"Permission denied while copying '{chimrun_version}'.")
            continue
        except Exception as e:
            print(f"Unexpected error while copying '{chimrun_version}': {e}")
            continue

        pre_file_path = f'CHIMRUN-pre{current_run}.DAT'
        
        try:
            shutil.copy('CHIMRUN.DAT', os.path.join(folder_names[i], pre_file_path))
        except Exception as e:
            print(f"Error copying CHIMRUN.DAT to {pre_file_path}: {e}")
            continue

        wine_exe_path = 'wine'
        chimxpt_exe_path = 'chim-xpt.exe'

        try:
            if platform.system() == 'Windows':
                result = subprocess.run([chimxpt_exe_path], capture_output=True, text=True)    
            elif platform.system() == 'Linux':
                result = subprocess.run([wine_exe_path, chimxpt_exe_path], capture_output=True, text=True)
            else:
                raise OSError(f"Unsupported operating system: {platform.system()}")
            
            print(result.stdout)
            print(result.stderr)
        except OSError as e:
            print(f"OS error while running CHIM-XPT: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error during CHIM-XPT execution: {e}")
            continue

        new_file_path = f'CHIMTERMINAL-{current_run}.DAT'

        try:
            with open(new_file_path, "w") as file:
                file.write(result.stdout)

            shutil.copy(new_file_path, os.path.join(folder_names[i], new_file_path))
            os.remove(new_file_path)
        except Exception as e:
            print(f"Error handling terminal output: {e}")
            continue

        try:
            post_file_path = f'CHIMRUN-post{current_run}.DAT'
            shutil.copy('CHIMRUN.DAT', os.path.join(folder_names[i], post_file_path))

            out_file_path = f'CHIMOUT-{current_run}.DAT'
            shutil.copy('CHIMOUT.DAT', os.path.join(folder_names[i], out_file_path))

            plot_file_path = f'CHIMPLOT-{current_run}.DAT'
            shutil.copy('CHIMPLOT.DAT', os.path.join(folder_names[i], plot_file_path))
        except Exception as e:
            print(f"Error copying output files: {e}")
            continue

    # Increment the run counter
    current_run += 1
    return current_run - 1

def revert_to_previous():
    """ 
    Resets all CHIMRUN files to the state that they were right before being ran
    Used mainly for ERROR Recovery

    Args: 
        N/A

    Returns: 
        N/A
    """ 
    
    global current_run, folder_names, folder_count

    # Decreases the run counter to account for reverting
    current_run -= 1

    # Loops though all version of CHIMRUN
    for i in range(folder_count):
        
        replacer_name = f'CHIMRUN-pre{current_run}.DAT'
        replaced_name = f'CHIMRUN{i}.DAT'
            
        try:
            shutil.copy(os.path.join(folder_names[i], replacer_name), replaced_name)
            print(f"Copied {replacer_name} to {replaced_name}.")
        except FileNotFoundError:
            print(f"The file '{replacer_name}' was not found in '{folder_names[i]}'.")
        except PermissionError:
            print(f"Permission denied while copying '{replacer_name}' to '{replaced_name}'.")
        except IOError as e:
            print(f"An error occurred while copying '{replacer_name}' to '{replaced_name}': {e}")
   
def manual_step_increase(increment_change, limit_change):
    """ 
    Updates the step increm and the step limit by getting changes from the user
    Required after running 'revert_to_previous'

    Args: 
        increment_change: Takes the input from the increment entry from 'run_gui'
        limit_change: Takes the input from the increment entry from 'run_gui'

    Returns: 
        N/A
    """ 
    
    global folder_count
    
    # Goes through all version of the CHIMRUN
    for i in range(folder_count):
        
        # Get current CHIMRUN file name
        chimrun_version = f'CHIMRUN{i}.DAT'
        
        try:
            with open(chimrun_version, 'r') as file:
                lines = file.readlines()
            print("File read successfully.")
        except FileNotFoundError:
            print(f"The file '{chimrun_version}' was not found.")
        except PermissionError:
            print(f"Permission denied: Unable to read the file '{chimrun_version}'.")
        except IOError as e:
            print(f"An error occurred while reading the file '{chimrun_version}': {e}")
            
        # Find the line with step increment and step limit values
        for i, line in enumerate(lines):
            if '< step increm >< step limit  >< total mixer >' in line:
                parts = lines[i + 1].strip().split()
                
                # Update the values in the parts list
                parts[0] = f'{increment_change:.8E}'
                parts[1] = f'{limit_change:.8E}'
                
                # Join parts and ensure correct formatting
                lines[i + 1] = f' {parts[0]:>12} {parts[1]:>12} {parts[2]:>12}\n'
                break

        # Write the updated content back to CHIMRUN.DAT
        try:
            with open(chimrun_version, 'w') as file:
                file.writelines(lines)
            print(f"File '{chimrun_version}' written successfully.")
        except PermissionError:
            print(f"Permission denied: Unable to write to the file '{chimrun_version}'.")
        except IOError as e:
            print(f"An error occurred while writing to the file '{chimrun_version}': {e}")

def auto_step_increase():
    """ 
    Automatically increases the step values by 10x
    Used for ERROR Recovery

    Args: 
        N/A

    Returns: 
        N/A
    """ 
    
    global folder_count
    
    # Loops through all versions of CHIMRUN
    for i in range(folder_count):
        
        # Get current CHIMRUN file name
        chimrun_version = f'CHIMRUN{i}.DAT'
        
        try:
            with open(chimrun_version, 'r') as file:
                lines = file.readlines()
            print("File read successfully.")
        except FileNotFoundError:
            print(f"The file '{chimrun_version}' was not found.")
        except PermissionError:
            print(f"Permission denied: Unable to read the file '{chimrun_version}'.")
        except IOError as e:
            print(f"An error occurred while reading the file '{chimrun_version}': {e}")
            
        # Find the line with step increment and step limit values
        for i, line in enumerate(lines):
            if '< step increm >< step limit  >< total mixer >' in line:
                parts = lines[i + 1].strip().split()
                
                # Automatically update the values by multiplying by 10
                new_step_increment = float(parts[0]) * 10
                new_step_limit = float(parts[1]) * 10
                
                # Update the values in the parts list
                parts[0] = f'{new_step_increment:.8E}'
                parts[1] = f'{new_step_limit:.8E}'
                
                # Join parts and ensure correct formatting
                lines[i + 1] = f' {parts[0]:>12} {parts[1]:>12} {parts[2]:>12}\n'
                break

        # Write the updated content back to CHIMRUN.DAT
        try:
            with open(chimrun_version, 'w') as file:
                file.writelines(lines)
            print(f"File '{chimrun_version}' written successfully.")
        except PermissionError:
            print(f"Permission denied: Unable to write to the file '{chimrun_version}'.")
        except IOError as e:
            print(f"An error occurred while writing to the file '{chimrun_version}': {e}")

def make_original_folder(folder_name):
    """ 
    Makes the original folder (for the CHIMRUN file provided by the user)

    Args: 
        folder_name: Takes the folder name provided by the user from the gui

    Returns: 
        N/A
    """ 
    
    global folder_names
    
    # Create the folder if it does not exist
    try:
        os.makedirs(folder_name, exist_ok=True)
        print(f"Directory '{folder_name}' created successfully or already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create directory '{folder_name}'.")
    except OSError as e:
        print(f"An error occurred: {e}")
    
    # Copy the initial CHIMRUN.DAT file to CHIMRUN0.DAT
    try:
        shutil.copy('CHIMRUN.DAT', 'CHIMRUN0.DAT')
    except FileNotFoundError:
        print("The source file 'CHIMRUN.DAT' was not found.")
    except PermissionError:
        print(f"Permission denied while copying to {'CHIMRUN0.DAT'}.")
    except IOError as e:
        print(f"An I/O error occurred: {e}")
    
    
    # Add the new folder name to the list
    folder_names.append(folder_name)
    
def make_new_condition(folder_name, pH, pFluid, temp):
    """ 
    Makes a new folder with the conditions that were provided by the user

    Args: 
        folder_name: Name of the original folder
        pH: New pH value provided by user
        pFluid: new pFluid value provided by the user
        temp: new temp value provided by the user

    Returns: 
        N/A
    """ 
    
    global folder_count, folder_names
    
    # Get the CHIMRUN version name
    file_path = f'CHIMRUN{folder_count}.DAT'
    
    # Copy the initial CHIMRUN.DAT file to the new CHIMRUN file
    try:
        shutil.copy('CHIMRUN0.DAT', file_path)
    except FileNotFoundError:
        print("The source file 'CHIMRUN0.DAT' was not found.")
    except PermissionError:
        print(f"Permission denied while copying to {file_path}.")
    except IOError as e:
        print(f"An I/O error occurred: {e}")
        
    # Read the content of CHIMRUN.DAT
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
    except IOError:
        print(f"An error occurred while reading the file at {file_path}.")
        
    # Find the line with the starting conditions and update them
    for i, line in enumerate(lines):        
        if '<  erpc  ><   pH   >< pfluid ><  temp  >' in line:
            parts = lines[i + 1].strip().split()
            
            # Update the parts with new values
            parts[1] = f'{pH:.4f}'
            parts[2] = f'{pFluid:.4f}'
            parts[3] = f'{temp:.4f}'
            
            # Join parts and ensure correct formatting without leading whitespace
            lines[i + 1] = f'{parts[0]:>12} {parts[1]:>9} {parts[2]:>9} {parts[3]:>9} {parts[4]:>9} {parts[5]:>12} {parts[6]:>9} {parts[7]:>9}\n'.strip()
            break

    # Write the updated content back to the new CHIMRUN file
    with open(file_path, 'w') as file:
        file.writelines(lines)
        
    # Create the new folder if it does not exist
    os.makedirs(folder_name, exist_ok=True)
    
    # Check if the folder name already exists in the list
    if folder_name not in folder_names:
        folder_names.append(folder_name)
    
    folder_count += 1

def get_parameters():
    """ 
    Returns the current pH, pFluid, and temp values as a visual aid for the user

    Args: 
        N/A

    Returns: 
        pH: The pH value from the original CHIMRUN file
        pFluid: The pFluid value from the original CHIMRUN file
        temp: The temp value from the original CHIMRUN file
    """ 
    
    file_path = 'CHIMRUN0.DAT'
    
    # Read the content of CHIMRUN.DAT
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
    except IOError:
        print(f"An error occurred while reading the file at {file_path}.")
        
    # Find the line with the current values
    for i, line in enumerate(lines):
        if '<  erpc  ><   pH   >< pfluid ><  temp  >' in line:
            parts = lines[i + 1].strip().split()
            
            # Puts the values into variables
            pH = float(parts[1])
            pfluid = float(parts[2])
            temp = float(parts[3])
            
            # Returns the values
            return pH, pfluid, temp

def get_current_step():
    """ 
    Returns the current step increm and step limit values as a visual aid for the user

    Args: 
        N/A

    Returns: 
        increm: The increment value from the original CHIMRUN file
        limit: The limit value from the original CHIMRUN file
    """ 
    
    file_path = 'CHIMRUN0.DAT'
    
    # Read the content of CHIMRUN.DAT
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
    except IOError:
        print(f"An error occurred while reading the file at {file_path}.")
        
    # Find the line with the current values
    for i, line in enumerate(lines):
        if '< step increm >< step limit  >< total mixer >' in line:
            parts = lines[i + 1].strip().split()
            
            # Puts the values into variables
            new_increm = parts[0]
            new_limit = parts[1]
            
            # Returns the values
            return new_increm, new_limit


    # 'annite              \n'
    # 14 spaces inbetween the mineral and the \n

def new_mineral():
    global folder_names, folder_count, all_mineral_list
                
    new_mineral_list = []  # Reset the list each time the function is called
    mineral_list_percentage = []
    
    for i in range(folder_count):

        file_path = os.path.join(folder_names[i], f'CHIMTERMINAL-{i+1}.DAT')
                
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"The file at {file_path} was not found.")
        except IOError:
            print(f"An error occurred while reading the file at {file_path}.")
        
        inside_mineral_section = False
        empty = False
        
        for line in lines:
            if 'Gas or mineral        Moles       Moles     Grams      Grams     Wt.%      (cm3)' in line:
                inside_mineral_section = True
                continue  # Skip the header line
            
            if inside_mineral_section:
                if line.strip() == '':
                    
                    if empty:
                        # Reached the end of the mineral section
                        break
                    
                    empty = True
                    continue
                
                # Extract the mineral name (assuming it's the first part of the line)
                mineral_name = line.strip().split()[0]
                mineral_weight = line.strip().split()[5]

                '''if mineral_name not in all_mineral_list:
                    all_mineral_list.append(mineral_name)
                    new_mineral_list.append(mineral_name)
                    mineral_list_percentage.append(mineral_weight)'''
                    
                new_mineral_list.append(mineral_name)
                mineral_list_percentage.append(mineral_weight)

    print(f"New mineral list: {new_mineral_list}")
    return new_mineral_list, mineral_list_percentage

def update_suppress_list(selected_minerals):
    print(selected_minerals)
    for folder_idx in range(folder_count):
        file_path = f'CHIMRUN{folder_idx}.DAT'
        
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"The file at {file_path} was not found.")
        except IOError:
            print(f"An error occurred while reading the file at {file_path}.")

        for line_idx, line in enumerate(lines):
            if '< mins to suppress >' in line:
                # Insert minerals after the < mins to suppress > line
                for mineral in selected_minerals:
                    lines.insert(line_idx + 1, f'{mineral}\n')
                break  # Exit the loop after inserting minerals
        
        with open(file_path, 'w') as file:
            file.writelines(lines)

def minerals_zeroing():
    global folder_names, folder_count, all_mineral_list
                
    zeroing_minerals = []  # Reset the list each time the function is called
    
    for i in range(folder_count):

        file_path = f'CHIMRUN{i}.DAT'
                
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"The file at {file_path} was not found.")
        except IOError:
            print(f"An error occurred while reading the file at {file_path}.")
        
        inside_mineral_section = False

        for line in lines:
            if '<     minerals     >  < min trial moles>' in line:
                inside_mineral_section = True
                continue  # Skip the header line
            
            if inside_mineral_section:
                line_arr = line.strip().split()
                mineral_name = line[0]
                mineral_mol = float(line_arr[1])
                print(mineral_mol)
                if mineral_mol < 1E-03:
                    zeroing_minerals.append(mineral_name)

    print(f"Zeroing mineral list: {zeroing_minerals}")
    return zeroing_minerals

# Ensure the main logic is not executed when imported
if __name__ == "__main__":
    pass
