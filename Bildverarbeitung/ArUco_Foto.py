import cv2
import os

# ArUco-Einstellungen
ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
aruco_parameters = cv2.aruco.DetectorParameters()

# Bild und Ergebnisordner
image_name = "bild3.jpg"  
# wird in einem Unterordner "results" gespeichert
output_folder = "./results/"  


# Ergebnisordner erstellen, falls er nicht existiert
os.makedirs(output_folder, exist_ok=True)

# Überprüfen, ob die Datei existiert
if not os.path.exists(image_name):
    print(f"[ERROR] Datei {image_name} wurde nicht gefunden.")
else:
    # Bild laden
    image = cv2.imread(image_name)
    if image is None:
        print(f"[ERROR] Datei {image_name} konnte nicht geladen werden!")
    else:
        # ArUco-Detektor erstellen
        aruco_detector = cv2.aruco.ArucoDetector(ARUCO_DICT, aruco_parameters)

        # ArUco-Marker detektieren
        corners, ids, rejected = aruco_detector.detectMarkers(image)

        # Wenn Marker erkannt wurden
        if ids is not None and len(ids) > 0:
            ids = ids.flatten()

            # Marker in Bild zeichnen
            for marker_corners, marker_id in zip(corners, ids):
                corners = marker_corners.reshape((4, 2))
                (top_left, top_right, bottom_right, bottom_left) = corners

                # Zu ganzen Zahlen konvertieren
                top_left = tuple(map(int, top_left))
                top_right = tuple(map(int, top_right))
                bottom_right = tuple(map(int, bottom_right))
                bottom_left = tuple(map(int, bottom_left))

                # Marker zeichnen
                cv2.line(image, top_left, top_right, (0, 255, 0), 2)
                cv2.line(image, top_right, bottom_right, (0, 255, 0), 2)
                cv2.line(image, bottom_right, bottom_left, (0, 255, 0), 2)
                cv2.line(image, bottom_left, top_left, (0, 255, 0), 2)

                # Mittelpunkt berechnen und markieren
                center_x = int((top_left[0] + bottom_right[0]) / 2.0)
                center_y = int((top_left[1] + bottom_right[1]) / 2.0)
                cv2.circle(image, (center_x, center_y), 4, (0, 0, 255), -1)

                # ID anzeigen (mit größerer Schrift und Dicke)
                cv2.putText(
                    image,  # Bild
                    f"ID: {marker_id}",  # Text
                    (top_left[0], top_left[1] - 10),  # Position
                    cv2.FONT_HERSHEY_SIMPLEX,  # Schriftart
                    1.5,  # Schriftgröße (fontScale)
                    (255, 0, 0),  # Farbe (Blau)
                    4  # Dicke (thickness)
                )
        else:
            print(f"[INFO] Keine Marker in {image_name} erkannt.")

        # Bild skalieren, damit es auf den Bildschirm passt
        scale_percent = 20  # Skalierungsfaktor in Prozent (hier auf 20 % verkleinert)
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        resized_image = cv2.resize(image, (width, height))

        # Skaliertes Bild in einem scrollbaren Fenster anzeigen
        def show_image_in_scrollable_window(image, window_name="ArUco Marker Detection"):
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_name, 800, 600)  # Anfangsgröße des Fensters
            cv2.imshow(window_name, image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        show_image_in_scrollable_window(resized_image)

        # Ergebnis speichern
        output_path = os.path.join(output_folder, "result_" + image_name)
        cv2.imwrite(output_path, image)
        print(f"[INFO] Ergebnis wurde gespeichert unter: {output_path}")

print("Fertig! Überprüfen Sie die Ergebnisse im Ordner './results/'.")