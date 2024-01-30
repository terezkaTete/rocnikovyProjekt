import json
from climbingWall import ClimbingWall
from tkinter import Tk, Button, messagebox, Listbox

# Function to load a saved wall from walls.json file
def load_saved_wall():
    # Load the data from walls.json file
    # Assuming the data is stored as a list of dictionaries
    with open('walls.json', 'r') as file:
        walls_data = json.load(file)

    # Create a listbox to display the available walls
    wall_listbox = Listbox(window)
    wall_listbox.pack()

    # Add each wall to the listbox
    for wall_data in walls_data:
        wall_listbox.insert('end', f"Wall {wall_data['id']}")  # Adjusted the key to 'id'

    # Display a messagebox to select a wall
    def select_wall():
        selected_wall_index = wall_listbox.curselection()
        window.destroy()
        if selected_wall_index:
            selected_wall_data = walls_data[selected_wall_index[0]]['wall']  # Adjusted the key to ['wall'
            wall = ClimbingWall(selected_wall_data['width'], selected_wall_data['height'], selected_wall_data['holds'], walls_data[selected_wall_index[0]]['id'])  # Adjusted the keys to 'width' and 'height'
            wall.display()
        else:
            messagebox.showinfo("No Wall Selected", "Please select a wall.")

    # Create a button to select a wall
    select_wall_button = Button(window, text="Select Wall", command=select_wall)
    select_wall_button.pack()

# Function to create a new wall
def create_new_wall():
    # Example usage
    wall = ClimbingWall(8, 12)
    window.destroy()
    wall.display()
    

# Ask the user if they want to load a saved wall or create a new wall
def on_load_wall_button_click():
    load_saved_wall()

def on_create_wall_button_click():
    create_new_wall()

# Create a GUI window
window = Tk()

# Create a button for loading a saved wall
load_wall_button = Button(window, text="Load Saved Wall", command=on_load_wall_button_click)
load_wall_button.pack()

# Create a button for creating a new wall
create_wall_button = Button(window, text="Create New Wall", command=on_create_wall_button_click)
create_wall_button.pack()

# Run the GUI window
window.mainloop()
