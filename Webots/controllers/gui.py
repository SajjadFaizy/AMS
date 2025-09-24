import tkinter as tk
from config import GUI_SETTINGS

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(GUI_SETTINGS["TITLE"])
        self.root.geometry(GUI_SETTINGS["SIZE"])

        # Main Frame
        self.frame = tk.Frame(self.root, bg=GUI_SETTINGS["BG_COLOR"])
        self.frame.pack(expand=False, fill="x", padx=20, pady=(20,5))
        
        # Create cells
        self.cells = {
            'ps6': self.create_cell(0, 0, "ps6", "0.00"),
            'ps7': self.create_cell(0, 1, "ps7", "0.00"),
            'ps0': self.create_cell(0, 2, "ps0", "0.00"),
            'ps1': self.create_cell(0, 3, "ps1", "0.00"),
            'ps2': self.create_cell(0, 4, "ps2", "0.00"),
            '6': self.create_cell(1, 1, "Position", "X=0.00\n Z=0.00"),
            '7': self.create_cell(1, 0, " Distance to Target ", "0.00"),
            '8': self.create_cell(1, 2, "  Next WP  ", "0.00"),
            '9': self.create_cell(1, 3, "   Heading   ", "0.00"),
            '10': self.create_cell(1, 4, "         Action         ", "0.00")
        }

        # Create frame for route
        self.list_frame = tk.Frame(self.root, bg=GUI_SETTINGS["BG_COLOR"])
        self.list_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Área de texto sin scrollbars, con ajuste de línea automático
        self.text_area = tk.Text(
            self.list_frame, 
            height=10, 
            wrap="word",  # Ajusta el texto automáticamente a la siguiente línea por palabras
            font=("Arial", 14, "bold")
        )
        self.text_area.pack(expand=True, fill="both")

    
    def create_cell(self, row, col, title, value):
        cell = tk.Frame(self.frame, bg=GUI_SETTINGS["BG_COLOR"], bd=2, relief="ridge")
        cell.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        tk.Label(cell, text=title, font=GUI_SETTINGS["TITLE_FONT"], bg=GUI_SETTINGS["BG_COLOR"]).pack()
        value_label = tk.Label(cell, text=value, font=GUI_SETTINGS["VALUE_FONT"], bg=GUI_SETTINGS["BG_COLOR"])
        value_label.pack()
        
        return value_label

    
    def update(self, robot):

        if robot.state == 0: state = "STOP"
        elif robot.state == 1: state = "GPS"
        elif robot.state == 2: state = "Obstacle Left"
        elif robot.state == 3: state = "Obstacle Right"
        else: state = "State missing"

        # ps Sensors
        for i in [6, 7, 0, 1, 2]:
            self.cells[f'ps{i}'].config(text=f"{int(robot.ps[i].getValue())}")

        self.cells['6'].config(text=f"( {robot.pos[0]:.2f} | {robot.pos[1]:.2f} )")
        self.cells['7'].config(text=f"{robot.dist_to_waypoint:.3f}")
        self.cells['8'].config(text=f"( {robot.next_wp_wbc[0]:.2f} | {robot.next_wp_wbc[1]:.2f} )")
        self.cells['9'].config(text=f"{robot.heading:.2f}")
        self.cells['10'].config(text=f"{state}")

        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, f"Route:\n{robot.remaining_path_wbc}")
        
        self.root.update_idletasks()

        