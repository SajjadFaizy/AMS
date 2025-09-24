from robot import EPuck
from gui import GUI
from config import MAP_NAME, STATE_GPS, MAP_GRID_RESOLUTION
from os import path as osp
from libraries.utils import coord_matrix_to_webots

if __name__ == '__main__':

    # Init robot and GUI
    epuck = EPuck()
    gui = GUI()

    # Load world map as matrix
    map_fname = osp.abspath(osp.join(osp.dirname(__file__), '..', '..', 'maps', f"{MAP_NAME}.npy"))
    epuck.load_map(map_fname)

    # Navigation Milestones
    # milestones = [(0.5, -0.45), (-0.55, -0.45), (0.0, -1.0)]
    milestones = [(-0.45, 0.45), (0.5, 0.45), (0.5, 0.15), (-0.45, 0.15), (-0.45, -0.15), (0.5, -0.15), (0.5, -0.45), (-0.55, -0.45), (0.0, -1.0)]
    # milestones = [(34,41), (15,41), (15,47), (34,47), (34,53), (15,53), (15,59), (34,59), (25,70)] # Zic-zac in mc
    # milestones = [(-0.4, 1.2), (0.5, 0.8), (0.5, 0.3)] # Medium
    # milestones = [(-0.3, 1.1), (-0.2, 1.1)] # Short
    if len(milestones) == 1: raise ValueError("To trace a route, minimum two points are required")

    # Load Milestones
    epuck.milestones = milestones

    # Calculate route and save in Epuck
    try: epuck.route = epuck.remaining_path = epuck.calculate_route(epuck.milestones)
    except: ValueError("Route calculation could not be completed")

    # Print Calculated Route
    print("------------------------------")
    print("Route:\n", "--\n", epuck.route, "\n--\n")
    print("Remaining path (matrix) init:\n", "--\n", epuck.remaining_path, "\n--\n")

    # Set Up Navigation
    epuck.next_waypoint = epuck.remaining_path.pop(0)
    epuck.remaining_path_wbc = coord_matrix_to_webots(epuck.remaining_path, epuck.mshape, MAP_GRID_RESOLUTION)
    print("Remaining path (webots) init:\n", "--\n", epuck.remaining_path_wbc, "\n--\n")
    epuck.next_wp_wbc = coord_matrix_to_webots(epuck.next_waypoint, epuck.mshape, MAP_GRID_RESOLUTION)
    epuck.state = STATE_GPS
    epuck.target = epuck.route[-1]
    epuck.target_wb = coord_matrix_to_webots(epuck.target, epuck.mshape, MAP_GRID_RESOLUTION)
    epuck.dist_to_target = epuck.distance_to_point(epuck.target)

    # Main Loop
    while epuck.robot.step(epuck.TIME_STEP) != -1:
        
        # Navigate route
        if epuck.follow_path() == True: break

        # Update GUI
        gui.update(epuck)


    # Close gui manually
    gui.root.mainloop()