from controller import Robot
from libraries.utils import wrap_to_pi, Side, coord_matrix_to_webots, coord_webots_to_matrix, save_np
from libraries.wavefrontlib import find_path
from config import *
from devices_setup import setup_devices

import numpy as np
import math
from copy import deepcopy

class EPuck:
    
    def __init__(self):

        self.TIME_STEP = TIME_STEP
        self.MAX_SPEED = MAX_SPEED_ENGINES
        self.OBSTACLE_THRESHOLD = OBSTACLE_THRESHOLD
        self.state = STATE_STOP
        self.WHEEL_RADIUS = WHEEL_RADIUS

        self.robot = Robot()

        self.init_devices()
        self.init_navigation()

    def init_devices(self):
        """ Configures the robot's devices using setup_devices """
        devices = setup_devices(self.robot)
        self.ps = devices['ps']
        self.gps = devices['gps']
        self.compass = devices['compass']
        self.left_motor = devices['left_motor']
        self.right_motor = devices['right_motor']

    def init_navigation(self):
        """ Configures the navigation variables """
        # Situation variables
        self.pos = self.get_position()
        self.heading = self.get_heading()
        # Route variables
        self.milestones = []
        self.route = []
        self.remaining_path = []
        self.remaining_path_wbc = []
        # Navigation variables
        self.map = None
        self.mshape = None
        self.target = None
        self.target_wb = None
        self.next_waypoint = None
        self.next_wp_wbc = None
        self.waypoint_heading = None
        self.desired_heading = None
        self.dist_to_waypoint = None
        self.dist_to_target = None
        # Movement variables
        self.tried = 0

    # Devices functions ----------------------------
    
    def get_position(self):
        """
        Gibt die aktuelle Richtung des Roboters zurück. Indem die GPS-Daten 
        (self.gps.getValues()) abruft und die x- und y- Koordinaten extrahiert. 
        Die wird dann als Tupel (x,y) zurückgegeben

        Returns:
            type: Tuple 
            return: (x, y) Koordinaten des Roboters.
        """
    
        coords = self.gps.getValues()
        return (coords[0], coords[1])
    
    def get_heading(self):
        """
        Gibt die aktuelle Richtung des Roboters in Radiant zurück.
        Indem er den Kompasswert mit der Methode self.compass.getValues()
        abruft, dann verwendet math.atan2, um die Orientierung (nördlich)
        in Radiant zu berechnen und den Wert auf den Bereich[-π,π] zu begrenzen.
        Short description of what the function does.

        Returns:
            type: float
            return: Die aktuelle Richtung des Roboters in Radiant.
        """
        north = self.compass.getValues()  # [nx, ny, nz]
        heading_rad = wrap_to_pi(math.atan2(north[0], north[1])) # [π/2 to -π/2]
        return heading_rad
    
    def obstacle_detected(self, ps=None, max_ir_intensity=OBSTACLE_THRESHOLD):
        """
        überprüft, ob ein Hindernis in der Nähe des Roboters erkannt wird.
        
        Args: ps (list): Liste der Indizes der Näherungssensoren, die überprüft werden sollen.
        max_ir_intensity (float): Schwellenwert für die Intensität des Infrarotlichts,
        das als Hindernis erkannt wird.
        
        Returns:    
        type: bool
        return: True, wenn ein Hindernis erkannt wird, andernfalls False.
        """ 
        if ps: return any(self.ps[ps_index].getValue() > max_ir_intensity for ps_index in ps)
        else: return any(ps.getValue() > max_ir_intensity for ps in self.ps)
    
    def obstacle_detected_front(self): 
        """
        überprüft, ob ein Hindernis in der Nähe des Roboters erkannt wird und 
        zwar in den vorderen Sensoren (0,1,6,7).
        
        Returns:
            type: bool
        """
        return self.obstacle_detected([0,1,6,7])
    
    
    def obstacle_detected_front_right(self):
        """
        Prüft auf Hindernisse im Bereich vorne rechts (Sektoren [0, 1]).
        Returns:
            type: bool
        """
        return self.obstacle_detected([0,1])
    
    def obstacle_detected_front_left(self):
        """
        Prüft auf Hindernisse im Bereich vorne links (Sektoren [6, 7]).
        returns:
            type: bool
        """
        return self.obstacle_detected([6,7])
    
    def obstacle_detected_right(self):
        """ 
        Prüft auf Hindernisse im Bereich rechts (Sektor [2]).
        returns:
            type: bool
        """
        return self.obstacle_detected([2])
   
    def obstacle_detected_left(self):
        """ 
        Prüft auf Hindernisse im Bereich links (Sektor [5]).
        returns:
            type: bool
        """
        return self.obstacle_detected([5])
    
    
     # Motor functions --------------------------


    def set_speed(self, left_speed, right_speed):
        """
        setzt die Geschwindigkeit der Motoren. 
        Multipliziert die Eingaben mit der maximalen Geschwindigkeit.
    
        Args:left_speed (float): Geschwindigkeit des linken Motors.
        right_speed (float): Geschwindigkeit des rechten Motors.

        """
        self.left_motor.setVelocity(left_speed * self.MAX_SPEED)
        self.right_motor.setVelocity(right_speed * self.MAX_SPEED)
   
        
    def stop(self):
        """
        Stoppt die Motoren, indem die Geschwindigkeit auf 0 gesetzt wird.
    
        """
        self.set_speed(0, 0)
        print("Se ha llamado a stop")
    
    
    def move_forward(self, distance=None, speed=0.5):
        """ 
        Bewegt den Roboter vorwärts. Falls eine Distanz übergeben wird,
        berechnet sie die Radrotation.
    
        Args:
        distanz (float): Die zurückzulegende Distanz.
        geschwindigkeit (float): Die Geschwindigkeit, mit der sich der Roboter bewegen soll.
        
        """
        if distance:
            # Calculate wheel-rotation-angle to move given distance
            wheel_rotation = distance / self.WHEEL_RADIUS   
            # Set wheel position and speed
            self.left_motor.setPosition(self.left_motor.getTargetPosition() + wheel_rotation)
            self.right_motor.setPosition(self.right_motor.getTargetPosition() + wheel_rotation)
        self.set_speed(speed, speed)
    # Drehen den Roboter durch entgegengesetzte Drehgeschwindigkeiten der Räder.
    def turn_left(self, speed=0.3): self.set_speed(-speed, speed)
    def turn_right(self, speed=0.3): self.set_speed(speed, -speed)

    # Navigation functions ------------------------
    def load_map(self, map_path):
        """
        wird verwendet, um die Karte zu laden, die der Roboter verwenden wird, um
        den Weg zu berechnen. Die Karte wird als NumPy-Array gespeichert.
        
        args:
        mappath (str): Der Pfad zur .npy-Datei, die die Karte enthält.
        
        """
        try:
            self.map = np.load(map_path)
            self.mshape = self.map.shape
        except FileNotFoundError:
            print(f"Error: File not found at path: {map_path}")
        except Exception as e:
            print(f"An error ocurred when loading .npy file: {e}")
    
    
    def load_route(self, route_osp):
        """
        Es wird verwendet, um den Weg zu laden, den der Roboter folgen soll.
        Der Weg wird als NumPy-Array gespeichert.
        Es konvertiert auch die Matrixkoordinaten in Webots-Koordinaten.
        
        Args:
        route_osp (str): Der Pfad zur .npy-Datei, die den Weg enthält.
    
        """

        self.route = self.remaining_path = np.load(route_osp)
        self.remaining_path_wbc = coord_matrix_to_webots(self.remaining_path, self.mshape, MAP_GRID_RESOLUTION)

        self.next_waypoint = self.remaining_path.pop(0)
        self.next_wp_wbc = coord_matrix_to_webots(self.next_waypoint, self.mshape, MAP_GRID_RESOLUTION)

        self.state == STATE_GPS

        print(f"Path: {route_osp} loaded")
    
        
    def update_situation(self):
        """
        Aktualisiert die Navigationssituation des Roboters:
        - Position
        - Richtung
        - Entfernung zum nächsten Wegpunkt
        - Richtung zum nächsten Wegpunkt
        - Entfernung zum Ziel
    
        """ 
        self.pos = self.get_position()
        self.heading = self.get_heading()
        self.dist_to_waypoint = round(self.distance_to_point(self.next_wp_wbc), 2)
        self.waypoint_heading = self.desired_heading = self.get_heading_to_point(self.next_wp_wbc)
        self.dist_to_target = round(self.distance_to_point(self.target), 2)
       
    def distance_to_point(self, point):
        """
        Berechnet die Entfernung zwischen dem Roboter und einem Punkt.
        
        Args:
        point (tuple): Die Koordinaten des Punktes.
        
        Returns:    
            type: float
            return: Die Entfernung zwischen dem Roboter und dem Punkt.
        """
        return math.sqrt((point[0] - self.pos[0])**2 + (point[1] - self.pos[1])**2)
    
    
    def get_heading_to_point(self, point):
        """
        Berechnet die Richtung des Roboters zu einem Punkt.
        
        Args:
        point (tuple): Die Koordinaten des Punktes.
        
        Returns:   
            type: float
            return: Die Richtung des Roboters zum Punkt.
    
        """
        return math.atan2(point[1] - self.pos[1], point[0] - self.pos[0])
    
    
    def heading_error_to_point(self, point):
        """
        Berechnet den Fehler zwischen der aktuellen Richtung des Roboters und der Richtung zu einem Punkt.
        
        Args:
        point (tuple): Die Koordinaten des Punktes.
        
        returns:
            type: float
            return: Der Fehler zwischen der aktuellen Richtung des Roboters und der Richtung zum Punkt.
    
        """
        if not point: raise ValueError("Reference point for error-heading missing")
        return wrap_to_pi(self.get_heading_to_point(point) - self.heading)
    
    
    def move_towards_heading(self, heading):
        """
        Bewegt den Roboter in Richtung einer bestimmten Richtung.
        
        Args:
        heading (float): Die Richtung, in die sich der Roboter bewegen soll.
        
        """
        error = wrap_to_pi(heading - self.heading)
        if abs(error) < HEADING_ERROR_THRESHOLD:
            self.move_forward()
        elif error > 0:
            self.turn_left()
        else:
            self.turn_right()
            
   

    def move_to_point(self, point):
        """
        Bewegt den Roboter zu einem bestimmten Punkt.
        
        Args:   
        point (tuple): Die Koordinaten des Punktes.
       
        """
        self.move_towards_heading(self.get_heading_to_point(point))
    

    def arrived_to_point(self, point=None):
        """
        Überprüft, ob der Roboter einen bestimmten Punkt erreicht hat.
        
        Args:
        point (tuple): Die Koordinaten des Punktes Null.
        
        Returns:
            type: bool
            return: True, wenn der Roboter den Punkt erreicht hat, andernfalls False
        """
        if not point: point = self.next_wp_wbc
        if self.distance_to_point(point) < DISTANCE_THRESHOLD:
            print(f"Waypoint ( {point[0]:.2f} | {point[1]:.2f} ) reached")
            return True
        else: return False
        
    

    def reset_navigation_data(self):
        """
        Setzt die Navigationsdaten zurück.
        """
        self.route = self.remaining_path = self.remaining_path_wbc = []
        
    
            

    # Bug Algorithm --------------------------

    def avoid_obstacle(self, side=Side.LEFT):
        """
        reagiert auf ein Hindernis, das vom Roboter erkannt wird.
        es kann entweder ein Hindernis vor dem Roboter sein oder ein Hindernis, das den Weg blockiert.
        
        Args:
        side (Side): Die Seite, auf der das Hindernis vermieden werden soll.
        
        """

        # If no obstacle detected anymore
        if not self.obstacle_detected():
            if self.tried <= AVOIDANCE_MAX_TRIES:
                self.move_forward(AVOIDANCE_DISTANCE)
                if self.obstacle_detected(max_ir_intensity=OBSTACLE_DANGER_THRESHOLD):
                    self.stop()
                self.tried += 1
            else:
                self.state = STATE_GPS
                self.tried = 0

        # If detected obstacle obstructs
        elif self.obstacle_detected_front():
            self.turn_left() if side == Side.LEFT else self.turn_right()

        # If detected obstacle does not obstruct
        elif side == Side.LEFT and self.obstacle_detected_right():
                self.move_forward(AVOIDANCE_DISTANCE)
        elif side == Side.RIGHT and self.obstacle_detected_left():
            self.move_forward(AVOIDANCE_DISTANCE)
   

    def go_to_point(self, point):
        """
        Bewegt den Roboter zu einem bestimmten Punkt.
        Wenn ein Hindernis erkannt wird, wird die Methode zur Hindernisvermeidung aufgerufen.
        und der Roboter wird entweder nach links oder rechts bewegt.
        es wird auch überprüft, ob der Roboter den Wegpunkt erreicht hat.
        
        Args:
        point (tuple): Die Koordinaten des Punktes.
        """
        if self.obstacle_detected_front():
            if self.obstacle_detected_front_left():
                self.state = STATE_OBSTACLE_LEFT
            else:
                self.state = STATE_OBSTACLE_RIGHT
            # Delete waypoints for flexibility to avoid obstacle
            if self.dist_to_waypoint < AVOIDANCE_DELETE_THRESHOLD:
                # Proof correct value in config
                if AVOIDANCE_DELETE_WP_QTY <= 0: raise ValueError("AVOIDANCE_DELETE_WP_QTY bust be greater than 0")
                # Delete waypoints
                self.next_waypoint = self.remaining_path.pop(0)
                self.next_wp_wbc = self.remaining_path_wbc.pop(0)
                self.remaining_path = self.remaining_path[(AVOIDANCE_DELETE_WP_QTY - 1):]
                self.remaining_path_wbc = self.remaining_path_wbc[(AVOIDANCE_DELETE_WP_QTY - 1):]           
                
        else:
            self.move_to_point(point)
            
    
    # Wavefront Algorithm --------------------------

    def calculate_route(self, milestones=False): # Joins many paths
        """
        Berechnet den Weg, den der Roboter folgen soll, um die Meilensteine zu erreichen.
        indem der Wavefront-Algorithmus verwendet wird
        und die berechneten Pfade werden in einer Liste gespeichert.

        Args:
        milestones (list): Die Liste der Meilensteine, die der Roboter erreichen soll.
        
        Returns:
            type: list
            return: Der berechnete Weg, den der Roboter folgen soll.
        """

        route = []
        if not milestones: milestones = self.milestones

        print(len(milestones))


        for i in range(1, len(milestones)):
            
            # If route_path being built
            if route and i != 1:
                print(f"Continuing calculation {milestones[i-1]} to {milestones[i]}")
                calculated_path = self.calculate_wavefront_path(milestones[i-1], milestones[i])
                route.extend(calculated_path[1:])

            # If no route_path
            elif not route and i == 1: # If empty route_path and FIRST WAYPOINT
                print(f"Starting route calculation {milestones[i-1]} to {milestones[i]}")
                calculated_path = self.calculate_wavefront_path(milestones[i-1], milestones[i])
                route.extend(calculated_path)

            # If Error
            else:
                raise RuntimeError("""ERROR: Previous route_path has not been deleted
                                    or route_path is being deleted on each loop cycle""")        

        print("Route calculation completed")  
        
        return route
    

    def calculate_wavefront_path(self, start, end):
        """
        berechnet den Weg, den der Roboter folgen soll, um von einem Punkt zu einem anderen zu gelangen. 
       
        Args:  
        start (tuple): Die Koordinaten des Startpunkts.
        end (tuple): Die Koordinaten des Endpunkts.
        
        Returns:    
            type: list
            return: Der berechnete Weg, den der Roboter folgen soll.
            
        """

        # Proof format errors
        if self.map is None: # Binary matrix: obstacle (1) | free (0)
            raise ValueError("Map has not been loaded")
        if not isinstance(self.map, np.ndarray):
            raise TypeError("Map must be a NumPy array")
        
        # Orientation parameters
        start_mc = coord_webots_to_matrix(start, self.mshape, MAP_GRID_RESOLUTION)
        end_mc = coord_webots_to_matrix(end, self.mshape, MAP_GRID_RESOLUTION)

        test_path = find_path(deepcopy(self.map), start_mc, end_mc)

        return test_path
    

    def follow_path(self):
        """
        Folgt dem berechneten Weg, indem er die Bewegung des Roboters steuert.
        Wenn der Roboter den Wegpunkt erreicht, wird der nächste Wegpunkt aktualisiert.
        Wenn der Roboter das Ziel erreicht, wird der Roboter gestoppt und die Navigationsdaten zurückgesetzt.
        wechselt auch den Status des Roboters, um auf Hindernisse zu reagieren.
        
        returns:
            type: str
            return: Statusmeldung. 
        """
        
        # Update sensors info
        self.update_situation()

        # Proof if arrived
        if self.arrived_to_point(self.target_wb):
            # Stop
            print("Arrived to target")
            self.state = STATE_STOP
            self.stop()
            print("Stopped")
            # Reset Nav Data
            self.reset_navigation_data()
            print("Navdata reseted")
            return True

        # If waypoint reached --> get next waypoint
        if self.arrived_to_point(self.next_wp_wbc):
            if self.remaining_path: self.next_waypoint = self.remaining_path.pop(0)
            else: print("Route finished")
            if self.remaining_path_wbc: self.remaining_path_wbc.pop(0) # Update remaining path in webots coords for gui
            self.next_wp_wbc = coord_matrix_to_webots(self.next_waypoint, self.mshape, MAP_GRID_RESOLUTION)

        # Move
        if self.state == STATE_GPS:
            self.go_to_point(self.next_wp_wbc)
        elif self.state == STATE_OBSTACLE_RIGHT:
            self.avoid_obstacle(Side.LEFT)
        elif self.state == STATE_OBSTACLE_LEFT:
            self.avoid_obstacle(Side.RIGHT)
        elif self.state == STATE_STOP:
            self.stop()
        
        return "On the way"
    
    