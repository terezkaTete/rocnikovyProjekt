import tkinter as tk
import json
class Hold:
    def __init__(self, x, y, hold_type):
        self.x = x
        self.y = y
        if hold_type not in ["jugs", "crimps", "pinches", "slopers"]:
            raise ValueError("Invalid hold type")
        self.hold_type = hold_type
    
    def get_hold_color(self):
        if self.hold_type == "jugs":
            return "green"
        elif self.hold_type == "crimps":
            return "red"
        elif self.hold_type == "pinches":
            return "blue"
        elif self.hold_type == "slopers":
            return "yellow"


class ClimbingWall:
    def __init__(self, width, height, holds_data=None, id=None):
        self.width = width
        self.height = height
        self.holds = []
        if(id is None):
            self.id = -1
        else:
            self.id = id
        if holds_data is not None:
            for hold_data in holds_data:
                hold = Hold(hold_data["x"], hold_data["y"], hold_data["hold_type"])
                self.holds.append(hold)
        
        self.selected_hold_type = "jugs"  # Default hold type is jugs

    def display(self):
        root = tk.Tk()
        canvas = tk.Canvas(root, width=self.width*40, height=self.height*40)
        canvas.pack(side=tk.LEFT)
        
        self.selected_color = "green"  # Default color is green

        def add_hold(event):
            x = event.x // 40
            y = event.y // 40
            hold = Hold(x, y, self.selected_hold_type)  # Pass the selected color and hold type to the Hold object
            self.holds.append(hold)
            canvas.create_oval(x*40+10, y*40+10, x*40+30, y*40+30, fill=self.selected_color)

        def select_jugs():
            self.selected_hold_type = "jugs"
            self.selected_color = "green"
            selected_hold_label.config(text="Selected Hold: Jugs")

        def select_crimps():
            self.selected_hold_type = "crimps"
            self.selected_color = "red"
            selected_hold_label.config(text="Selected Hold: Crimps")

        def select_pinches():
            self.selected_hold_type = "pinches"
            self.selected_color = "blue"
            selected_hold_label.config(text="Selected Hold: Pinches")

        def select_slopers():
            self.selected_hold_type = "slopers"
            self.selected_color = "yellow"
            selected_hold_label.config(text="Selected Hold: Slopers")

        def save_wall():
            try:
                with open("walls.json", "r") as file:
                    walls = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                walls = []

            if walls:
                wall_id = walls[-1]["id"] + 1
            else:
                wall_id = 0

            if self.id != -1:
                print("Updating wall...")
                for wall in walls:
                    if wall["id"] == self.id:
                        wall["wall"]["width"] = self.width
                        wall["wall"]["height"] = self.height
                        wall["wall"]["holds"] = [
                            {"x": hold.x, "y": hold.y, "hold_type": hold.hold_type}
                            for hold in self.holds
                        ]
                        break
            else:
                data = {
                    "id": wall_id,
                    "wall": {
                        "width": self.width,
                        "height": self.height,
                        "holds": [
                            {"x": hold.x, "y": hold.y, "hold_type": hold.hold_type}
                            for hold in self.holds
                        ]
                    }
                }
                walls.append(data)

            with open("walls.json", "w") as file:
                json.dump(walls, file, indent=4)

            print("Wall saved successfully!")

        canvas.bind("<Button-1>", add_hold)

        jugs_button = tk.Button(root, text="Jugs", command=select_jugs)
        jugs_button.pack(side=tk.LEFT)

        crimps_button = tk.Button(root, text="Crimps", command=select_crimps)
        crimps_button.pack(side=tk.LEFT)

        pinches_button = tk.Button(root, text="Pinches", command=select_pinches)
        pinches_button.pack(side=tk.LEFT)

        slopers_button = tk.Button(root, text="Slopers", command=select_slopers)
        slopers_button.pack(side=tk.LEFT)

        save_button = tk.Button(root, text="Save Wall", command=save_wall)
        save_button.pack(side=tk.LEFT)

        for row in range(self.height):
            for col in range(self.width):
                x1 = col * 40
                y1 = row * 40
                x2 = x1 + 40
                y2 = y1 + 40
                canvas.create_rectangle(x1, y1, x2, y2, fill="gray")
                
        for hold in self.holds:
            canvas.create_oval(hold.x*40+10, hold.y*40+10, hold.x*40+30, hold.y*40+30, fill=hold.get_hold_color())
        

        selected_hold_label = tk.Label(root, text="Selected Hold: Jugs")
        selected_hold_label.pack()

        root.mainloop()
        
