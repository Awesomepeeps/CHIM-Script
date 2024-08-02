import os
import csv
import pandas as pd
import os
import re
from collections import defaultdict

weight_mineral_list = []       # Mineral list for storing all minerals with weight percent before logwr is added
csv_weight_mineral_list = []   # Mineral list for storing all minerals to add into the csv
mole_mineral_list = []         # Mineral list for storing all minerals with aq moles before logwr is added
csv_mole_mineral_list = []
folder_count = 0        # Amount of folders
folder_names = ['Folder Name']       # List of folder names
current_run = 0         # Total amount of runs done

def find_file_pairs(folder_path):
    # Ensure the folder_path is valid
    if not os.path.isdir(folder_path):
        raise ValueError(f"The path {folder_path} is not a valid directory.")
    
    # Dictionary to hold file pairs
    file_pairs = defaultdict(lambda: {'CHIMOUT': None, 'CHIMTERMINAL': None})

    # Pattern to extract the number from the filename
    pattern = re.compile(r'(\d+)\.DAT$')

    # List all files in the folder
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        
        if os.path.isfile(file_path):
            match = pattern.search(file)
            if match:
                number = match.group(1)
                if 'CHIMOUT' in file:
                    file_pairs[number]['CHIMOUT'] = file_path
                elif 'CHIMTERMINAL' in file:
                    file_pairs[number]['CHIMTERMINAL'] = file_path
    
    # Filter out pairs where both files are present
    pairs = [(info['CHIMOUT'], info['CHIMTERMINAL']) 
             for info in file_pairs.values() 
             if info['CHIMOUT'] and info['CHIMTERMINAL']]

    return pairs

def list_files_in_folder(folder_path):
    # Check if the folder_path is a directory
    if not os.path.isdir(folder_path):
        raise ValueError(f"The path {folder_path} is not a valid directory.")
    
    # List all files in the folder
    files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    return files

# Class for storing one mineral and data
class item_weight:
    def __init__(self, name, temp, pfluid, ph, mix_frac, logwr, weight_per):
        self.name = name
        self.temp = temp
        self.pfluid = pfluid
        self.ph = ph
        self.mix_frac = mix_frac
        self.logwr = logwr
        self.weight_per = weight_per

    def logwr_set(self, new_logwr):
        self.logwr = new_logwr
        
    def get_weight_per(self):
        return self.weight_per
        
    def print_all(self):
        print(f'Name: {self.name}')
        print(f'Temp: {self.temp}')
        print(f'pFluid: {self.pfluid}')
        print(f'pH: {self.ph}')
        print(f'Mix Frac: {self.mix_frac}')
        print(f'Log WR: {self.logwr}')
        print(f'Weight Percentage: {self.weight_per}')
        print()
        
# Class for storing one mineral and data
class item_mole:
    def __init__(self, name, temp, pfluid, ph, mix_frac, logwr, aq_moles):
        self.name = name
        self.temp = temp
        self.pfluid = pfluid
        self.ph = ph
        self.mix_frac = mix_frac
        self.logwr = logwr
        self.aq_moles = aq_moles

    def logwr_set(self, new_logwr):
        self.logwr = new_logwr
        
    def get_aq_moles(self):
        return self.aq_moles
        
    def print_all(self):
        print(f'Name: {self.name}')
        print(f'Temp: {self.temp}')
        print(f'pFluid: {self.pfluid}')
        print(f'pH: {self.ph}')
        print(f'Mix Frac: {self.mix_frac}')
        print(f'Log WR: {self.logwr}')
        print(f'Aq. Moles: {self.aq_moles}')
        print()

def write_to_weight_csv(filename, weight_per_mineral_list):
    # Define the header for the CSV
    header = ['Name', 'Temperature', 'PFluid', 'pH', 'MixFrac', 'LogWR', 'Weight%']

    # Open the CSV file for writing
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(header)
        
        # Write each mineral's data
        for mineral in weight_per_mineral_list:
            writer.writerow([
                mineral.name,
                mineral.temp,
                mineral.pfluid,
                mineral.ph,
                mineral.mix_frac,
                mineral.logwr,
                mineral.weight_per
            ])
            
def write_to_mole_csv(filename, aq_mole_mineral_list):
    # Define the header for the CSV
    header = ['Name', 'Temperature', 'PFluid', 'pH', 'MixFrac', 'LogWR', 'Aq. Mole']

    # Open the CSV file for writing
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(header)
        
        # Write each mineral's data
        for mineral in aq_mole_mineral_list:
            writer.writerow([
                mineral.name,
                mineral.temp,
                mineral.pfluid,
                mineral.ph,
                mineral.mix_frac,
                mineral.logwr,
                mineral.aq_moles
            ])

# Function for adding all minerals to a csv file
def record_items_weight(folder):
    global weight_mineral_list, folder_names, csv_weight_mineral_list
    
    pairs = find_file_pairs(folder)
    
    for out_file, terminal_file in pairs:
        
        # Getting file paths
        out_file_name = out_file
        terminal_file_name = terminal_file
        out_file_path = os.path.join(folder, out_file_name)
        terminal_file_path = os.path.join(folder, terminal_file_name)
        
        
        current_name = ''
        current_temp = 0
        current_pfluid = 0
        current_ph = 0
        current_mixer_frac = 0
        current_logwr = 0
        current_weight_per = 0

        # Reading in files and storing them
        with open(out_file_path, 'r') as file:
            out_lines = file.readlines()
        with open(terminal_file_path, 'r') as file:
            terminal_lines = file.readlines()

        # Getting the pH through the terminal output
        for line in enumerate(terminal_lines):
            if 'The pH is:' in line[1]:
                line_split = line[1].strip().split()
                current_ph = line_split[3]

        new_section = False
        weight_per_sec = False  # Weight Percentage Section
        weight_counter = 0
        pconditions = True

        # Goes through every line in the output file                  
        for a, line in enumerate(out_lines):
            line_arr = line.strip().split()  # Strips and splits current line to make it easier to work with

            # Checks if new section of the output file starts by checking for 'temperature' two lines after (accounting for new line)
            if '++++++++++++++++++++++++++++++++++++++++' in line and 'Temperature' in out_lines[a+4].strip().split():
                new_section = True

            # Checks for line with temperature, pfluid, and mixer fraction
            if new_section and 'Temperature' in line and pconditions:
                current_temp = line_arr[2]
                current_pfluid = line_arr[6]
                current_mixer_frac = line_arr[11]
                pconditions = False

            # Checking if section with weight percentages starts
            if new_section and 'Gas or mineral        Moles       Moles     Grams      Grams     Wt.%      (cm3)' in line:
                weight_per_sec = True
                continue

            # Skips if new line
            if weight_per_sec and line.strip() == '':
                weight_counter += 1
                continue

            # If second new line then stop checking for weight percentages
            if weight_counter == 2:
                weight_counter = 0
                weight_per_sec = False

            if weight_per_sec:
                current_weight_per = line_arr[5]
                current_name = line_arr[0]
                new_mineral = item_weight(current_name, current_temp, current_pfluid, current_ph, current_mixer_frac, current_logwr, current_weight_per)
                weight_mineral_list.append(new_mineral)
                
            if '(Water/Rock Ratio), log' in line:
                current_logwr = line_arr[10]
                for mineral in weight_mineral_list:
                    mineral.logwr_set(current_logwr)
                    mineral.print_all()
                    if mineral not in csv_weight_mineral_list and float(mineral.get_weight_per()) > 1:
                        csv_weight_mineral_list.append(mineral)

            if '++++++++++++++++++++++++++++++++++++++++' in line and '++++++++++++++++++++++++++++++++++++++++' in out_lines[a+2]:
                # Resetting all used variables
                current_name = ''
                current_temp = 0
                current_pfluid = 0
                current_ph = 0
                current_mixer_frac = 0
                current_logwr = 0
                current_weight_per = 0
                weight_mineral_list = []
                pconditions = True
                        
# Function for adding all minerals to a csv file
def record_items_moles(folder):
    global mole_mineral_list, folder_names, csv_mole_mineral_list
    
    pairs = find_file_pairs(folder)
    
    for out_file, terminal_file in pairs:
        
        # Getting file paths
        out_file_name = out_file
        terminal_file_name = terminal_file
        out_file_path = os.path.join(folder, out_file_name)
        terminal_file_path = os.path.join(folder, terminal_file_name)
        
        
        current_name = ''
        current_temp = 0
        current_pfluid = 0
        current_ph = 0
        current_mixer_frac = 0
        current_logwr = 0
        current_aq_mole = 0

        # Reading in files and storing them
        with open(out_file_path, 'r') as file:
            out_lines = file.readlines()
        with open(terminal_file_path, 'r') as file:
            terminal_lines = file.readlines()

        # Getting the pH through the terminal output
        for line in enumerate(terminal_lines):
            if 'The pH is:' in line[1]:
                line_split = line[1].strip().split()
                current_ph = line_split[3]

        new_section = False
        aq_moles_sec = False    # Aq. moles Section
        aq_mole_counter = 0
        pconditions = True

        # Goes through every line in the output file                  
        for a, line in enumerate(out_lines):
            line_arr = line.strip().split()  # Strips and splits current line to make it easier to work with

            # Checks if new section of the output file starts by checking for 'temperature' two lines after (accounting for new line)
            if '++++++++++++++++++++++++++++++++++++++++' in line and 'Temperature' in out_lines[a+4].strip().split():
                new_section = True

            # Checks for line with temperature, pfluid, and mixer fraction
            if new_section and 'Temperature' in line and pconditions:
                current_temp = line_arr[2]
                current_pfluid = line_arr[6]
                current_mixer_frac = line_arr[11]
                pconditions = False
                
            # Checking if section with weight percentages starts
            if new_section and 'Component          Tot moles       Aq. moles       Solid moles     Gas moles' in line:
                aq_moles_sec = True
                continue

            # Skips if new line
            if aq_moles_sec and line.strip() == '':
                aq_mole_counter += 1
                continue

            # If second new line then stop checking for weight percentages
            if aq_mole_counter == 2:
                aq_mole_counter = 0
                aq_moles_sec = False

            if aq_moles_sec:
                current_aq_mole = line_arr[3]
                current_name = line_arr[1]
                new_mineral = item_mole(current_name, current_temp, current_pfluid, current_ph, current_mixer_frac, current_logwr, current_aq_mole)
                mole_mineral_list.append(new_mineral)

            if '(Water/Rock Ratio), log' in line:
                current_logwr = line_arr[10]
                for mineral in mole_mineral_list:
                    mineral.logwr_set(current_logwr)
                    mineral.print_all()
                    if mineral not in csv_mole_mineral_list:     # and float(mineral.get_weight_per()) > 1:
                        csv_mole_mineral_list.append(mineral)

            if '++++++++++++++++++++++++++++++++++++++++' in line and '++++++++++++++++++++++++++++++++++++++++' in out_lines[a+2]:
                # Resetting all used variables
                current_name = ''
                current_temp = 0
                current_pfluid = 0
                current_ph = 0
                current_mixer_frac = 0
                current_logwr = 0
                current_weight_per = 0
                mole_mineral_list = []
                pconditions = True
                
           
           
def main_call(selected_folders):
    
    for folder in selected_folders:
        record_items_weight(folder)
        record_items_moles(folder)
    
    write_to_weight_csv('weight_output.csv', csv_weight_mineral_list)
    
    # Load the CSV file into a DataFrame
    df = pd.read_csv('weight_output.csv')

    # Sort the DataFrame by the first column (change 'column_name' to the actual name of the first column)
    df_sorted = df.sort_values(by='Name')

    # Save the sorted DataFrame to a new CSV file
    df_sorted.to_csv('sorted_weight_file.csv', index=False)
    
    

    write_to_mole_csv('mole_output.csv', csv_mole_mineral_list)
    
    # Load the CSV file into a DataFrame
    df = pd.read_csv('mole_output.csv')

    # Sort the DataFrame by the first column (change 'column_name' to the actual name of the first column)
    df_sorted = df.sort_values(by='Name')

    # Save the sorted DataFrame to a new CSV file
    df_sorted.to_csv('sorted_mole_file.csv', index=False)
            
            

if __name__ == '__main__':
    pass