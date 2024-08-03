# CHIM-XPT GUI and User Interface

This project was created as a tool to help more effectively manage and use the program CHIM-XTP that was developed and made at the University of Oregon. CHIM-XPT (Chemical Interactions Model - Extended Processing Tool) is a geochemical modeling software used for simulating chemical reactions between water and rock.

## Current State

Currently, the propgram consists of a GUI and some comand line outputs. The GUI exists as a visual aid to the user in order to simplify a majority of the work that they have to do. This can range from creating modified versions of the original file and running it paralley to automatically incrementing the file for the user

# Getting Started

Clone the repository, the program consists of two main files, run_chimxpt.py and run_gui.py.

```git clone https://github.com/Awesomepeeps/CHIM-Script```

Run in the command line to start the program

```python3 chimxpt_gui.py```

In order to access the CHIM-XPT program, you must contact the creators of the program, Mark H. Reed, Nicolas F. Spycher, or James Palandri from the University of Oregon. 

Run in order to run the graphing program

```python3 graph_gui.py```

The only libraries required are installed with the default python package except for matplotlib and pandas. These can be installed by running:

```pip install matplotlib```

```pip install pandas```

It is important to note that this program will only run on Windows and Linux, and if is being run on Linux then the extra step of installing "Wine" must be used. That can be done by first running 

```sudo apt update```

```sudo apt install wine64```

## GUI Interface

### Folder Creation and Start
__Folder Name Text Box__: Enter the name of the folder that you want to create, all other folders created will be based of this too. The rest of the GUI will be locked until this is set.

__Confirm Folder Name__: This locks in the file name.

### New Conditions and RUN Files
__pH Entry__: In order to create a new RUN file that will be run aloing with the original, then use this field to change pH.

__pFluid__: Use this to change the pFluid in new RUN file.

__Temp__: Use this to change the Temp in new RUN file.

__Make New Folder__: Use to to create a new RUN file using the values from entries from above as the modification values.

### Running and Increasing Step Increments and Limits
__Auto Increase by 10x__: Increase the step increm and step limit of all RUN files by 10x.

__Step Increment__: Shows current step increment for all RUN files, can be used to create new Step Increment.

__Step Limit__: Shows current step limit for all RUN files, can be used to create new Step Limit.

__Load Manual Increase__: Loads the Step Increment and the Step Limit from the entries into all RUN files.

__Run__: Runs all RUN files and saves OUT, PLOT, RUN-pre, RUN-post, and terminal output into the proper folder.

__Previous Run__: Changes all current RUN files to the way they were right before last Run. Locks Auto increase by 10 and Previous Run buttons until program is Run again.

## Graphing and CSV Creation
__Browse__: Hitting this button will bring up a file select screen where you can select a folder that cotains CHIMOUT.DAT and CHIMTERMINAL.DAT files that you want to compile into a CSV. Multiple folders can be selected

__Create CSV with Selected Folders__: Creates two CSV files with all CHIMOUT and CHIMTERMINAL files in all selected folders, one for the weight percentages and one for the Aq. Moles

__Load CSV Files__: Loads the selected CSV file to be the on that is being graphed

__Two Drop Down Menus__: These are for selecting which column should be the x and y axis, first one is x and second one is y

__Plot Graph__: This plots a graph with all selected options above

## Other Important Information
All four .py files must be located in the same folder that contains the rest of the CHIM-XPT files such as CHIMRUN.DAT and chim-xpt.exe in order to run properly

The original output of the CHIM-XPT program will still be printed to the terminal. If there are multiple CHIMRUN files and runs, the terminal may become cluttered.

## Future Steps
- Compiling CHIMOUT.DAT files into CSVs for ease of use.
- Add a plottting GUI that allows for custom plotting and takes CSVs.
- Error Recovery.
- Dealing with Zeroing Mineral.
- Terminal Touch-Ups.
