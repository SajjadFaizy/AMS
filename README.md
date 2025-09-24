# Dokumentation
| Gruppenteilnehmer       | Matrikelnummer |
| ----------------------- | -------------- |
| Sajjad Faizy            |         |
| Michel Radloff          |         |
| Aran Sadeghi Yazdankhah |         |
| Daniel Cortés Caparrós  |        |


| Betreuer                 | Abgabedatum |
| ------------------------ | ----------- |
| Prof. Dr. Stephan Schulz | xx.xx.2025  |

# Einleitung
In dem Modul Autonome mobile Systeme der HAW Hamburg haben die Studierenden erste Anwendungen in Python kennengelernt, mit denen Eingaberessourcen verarbeitet werden können. Desweiteren wurden Pfadplanungs-Methoden wie der Bug-Algorithmus und der Wavefront-Algorithmus, die in einem abschließenden Projekt zusammengeführt wurden. Dieses Projekt wurde mit einem Roboter in der Simulationssoftware "Webots" in der Programmiersprache Python realisiert.

# Inhaltsverzeichnis
- [Algorithmen mit Python](#algorithmen-mit-python)
   - [Schwerpunktberechnung](#algorithmen-mit-python)
   - [ArUco-Marker](#aruco-marker)
   - [Wavefront](#wavefront)
- [Webots Projekt](#webots)
   - [Epuck](#e-puck)
   - [Welt und Route](#welt-und-route)
   - [Logikstruktur der Navigation](#logikstruktur-der-navigation)
      - [Erklärung der Hauptfunktion follow_path()](#hauptfunktion-follow_path)
      - [Logik der Navigation ohne Hindernisse](#logik-der-navigation-ohne-hindernisse)
      - [Logik der Vermeidung von Hindernisse](#logik-der-vermeidung-von-hindernisse)
         - [🛜 Detektion](#detektion)
         - [⤴️ Vermeidung](#vermeidung)


# Algorithmen mit Python

## Schwerpunktberechnung
[Dieser Code](https://github.com/nichtMichel/AMS_WS24-25_G1_Projektarbeit/blob/main/2_Bildverarbeitung/Schwerpunktbestimmung.ipynb) 
zeigt den Schwerpunkt eines Objekts in einem Bild an. Ein zweidimensionales Objekt wird im Bild erkannt, der Schwerpunkt des Objekts wird berechnet und anschließend im Bild markiert.
Aus dem Bild eines eines gleichschenkligen Dreiecks wird in diesem Beispiel der Schwerpunkt dargestellt.

Eingangsbild:

![Eingangsbild](/0_Bilder_Dokumentation/Schwerpunkt_1.png)

Ausgangsbild:

![Ausgangsbild](/0_Bilder_Dokumentation/Schwerpunkt_2.png)

Die einzelnen Funktionen des Skripts werden im Folgenden erläutert:

### 1. Bild laden und anzeigen
```python
Das Bild soll geladen und im Anschluss angezeit werden
imgclr = mpimg.imread('dreieck.png')
imgclr = (imgclr*255).astype(int)
plt.imshow(imgclr)
plt.show()
```

### 2. Bildanalyse
Bildinformationen, wie Höhe, Breite und Farbkanäle werden überprüft und eine vertikale Linie durch die Mitte wird geplottet.
```python
plt.plot(imgclr[:, int(nx/2)])
plt.show()
```

### 3. Umwandlung des Bildes in Graustufen und Analyse
Die RGB Kanäle werden mit den Luminanzwerten konvertiert und gerundet. So wird das Bild in Graustufen konvertiert. Anschließend wird eine vertikale und eine horizontale Linie durch die Bildmitte geplottet um die Grauwertverteilung zu visualisieren.

### 4. Binärisierung
as Graustufenbild wird in ein binäres Bild konvertiert, wobei alle Pixel mit einem Wert über 50 als True (weiß) gesetzt werden:
```python
binimg = imggry > 50
plt.imshow(binimg)
plt.show()
```
### 5. Berechnung
Für jedes Pixel im binären Bild wird überprüft, ob es True ist. Falls ja, werden die x- und y-Koordinaten aufaddiert, und der Gesamtpunktestand wird erfasst. Der Schwerpunkt wird durch den Durchschnitt dieser Koordinaten berechnet:
```python
for k in range(nx):
    for m in range (ny):
        if binimg[m, k]:
            spges += 1
            spunkt += [m, k]
spunkt = (spunkt/spges).astype('int')
```
### 6. Visualisierung des Schwerpunkts
Abschließend wird das ursprüngliche Bild mit einer Markierung an der berechneten Schwerpunktposition angezeigt.

## ArUco-Marker

Die Marker sind eine gängige Methode in der autonomen Robotik für die räumliche Orientierung.
Sie sind eine Ansammlung von wenigen schwarzen und weißen Pixel in quadratischer Form. Der hohe Kontrast von schwarz zu weiß eignet sich sehr gut, um von der Software auf Bildern erkannt zu werden. Durch eine feste Ordnung von mehreren Markern im Raum lässt sich die Pose von einem Gegenstand bzw. der Kamera im Raum bestimmen.
Über einfachen Code ist es möglich, in einem Live-Bild der Webcam die Marker zu erkennen und zu markieren.

### Erzeugung von ArUco-Markern

***Quelle:** *ArucoGenerator.py*

Dieses Skript erzeugt ein Gitter mit 12 **ArUco-Markern** (3 Zeilen x 4 Spalten) und zeigt sie in einer Abbildung an.

#### Beschreibung:

1. **Definieren des ArUco-Dictionarys**:
   - `ar_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)`: Verwendet ein 6x6 Dictionary mit 250 Markern.

2. **Erzeugen und Anzeigen der Marker**:
   - Die Schleife `for k in range(1, 13)` erzeugt 12 Marker und zeigt sie in Subplots mit einer Größe von 700x700 px an.
   - `plt.imshow(img, cmap='gray')`: Zeigt die Marker in Graustufen an.

3. **Anzeige**:
   - `plt.show()`: Zeigt die Abbildung mit den 12 Markern an.

#### Hinweis:
- Verwende `plt.savefig("markers.pdf")`, um die Marker als PDF zu speichern.


### Erkennung von Arucos

Dieses Skript erkennt und zeigt **ArUco-Markern** in einem Bild mithilfe von OpenCV.

#### Beschreibung:

1. **Bild laden**:
   - `img = cv2.imread("Material/aru1.jpg")`: Lädt das Bild im **BGR**-Format (Standard in OpenCV).
   - `imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`: Wandelt das Bild von **BGR** in **Graustufen** um.

2. **ArUco-Dictionary und Parameter einrichten**:
   - `aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)`: Verwendet ein 6x6 Dictionary mit 250 Markern.
   - `parameters = aruco.DetectorParameters()`: Erstellt die Detektionsparameter (mit den Standardeinstellungen).

3. **Erkennung der ArUco-Markern**:
   - `corners, ids, rejectedImgPoints = aruco.detectMarkers(imggray, aruco_dict, parameters=parameters)`: Erkennt die Marker im Bild.
   - `img_markers = aruco.drawDetectedMarkers(img.copy(), corners, ids)`: Zeichnet die erkannten Marker auf das Originalbild.

4. **Anzeige des Bildes mit den Markern**:
   - `img_markers_rgb = cv2.cvtColor(img_markers, cv2.COLOR_BGR2RGB)`: Wandelt das Bild von **BGR** in **RGB** für Matplotlib um.
   - `plt.imshow(img_markers)`: Zeigt das Bild mit den erkannten Markern an.
   - Die Mittelpunkte der Marker werden mit einem Punkt markiert, und die **ID** jedes Markers wird in der Legende angezeigt.

#### Hinweis:
- Der auskommentierte Codeblock (`img_markers = img.copy()`) zeigt, wie man die Rechtecke manuell um die Marker zeichnet.

Über die Python Bibliothek "OpenCV", welche für Aufgaben der Bildverarbeitung erstellt wurde, können ArUco-Marker direkt erstellt werden.
(Quelle: https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html)

#### Live-ArUco Erkennung
In [diesem Code](https://github.com/nichtMichel/AMS_WS24-25_G1_Projektarbeit/blob/main/2_Bildverarbeitung/ArUco_Live_Webcam.py) wurde umgesetzt, dass die Webcam des nutzenden Endgeräts dazu genutzt wird, ArUco-Marker live im Bild zu erkennen, zu markieren und zu numerieren.

#### ArUco-Marker Auswertung
Bei der Verwendung der Live-Kamera war es schwierig, die Ergebnisse zu bewerten, da die Hände oder die Kamera sich bewegen konnten. Dies führte dazu, dass nicht alle Marker gleichzeitig oder korrekt erkannt wurden.

Die Live-Kamera erfasst kontinuierlich Frames, was die Analyse der Ergebnisse in Echtzeit erschwert, insbesondere wenn sich die Marker oder die Kamera bewegen. Deswegen haben wir Statische Bilder für bessere Bewertung genutzt. Um die Ergebnisse besser auswerten zu können, wurden statische Bilder mit verschiedenen Winkeln und Abständen aufgenommen. Dies ermöglicht eine präzisere Analyse der Erkennungsgenauigkeit.
Die Ergebnisse wurden im Verzeichnis ./results/ gespeichert, sodass sie später detailliert ausgewertet werden konnten.

Bei der Bewertung der Ergebnisse fällt auf, dass die ArUco-Marker in allen Bildern konsistent und korrekt erkannt wurden. Es gab keine Unterschiede in der Erkennungsgenauigkeit zwischen den verschiedenen Bildern, da in jedem Fall alle Marker korrekt identifiziert und ihre IDs richtig angezeigt wurden. Dies zeigt, dass der Code robust ist und unabhängig von Winkel oder Abstand zuverlässig funktioniert.

##### Konsistenz der Egebnisse 

   - In allen Bildern wurden die ArUco-Marker vollständig und korrekt erkannt.

   - Die IDs der Marker wurden richtig zugeordnet, und es gab keine Fehlerkennungen oder falschpositiven Ergebnisse.

   ![Bild0](/2_Bildverarbeitung/results/result_bild0.jpg)

   ![bild1](/2_Bildverarbeitung/results/result_bild1.jpg)

   ![bild2](/2_Bildverarbeitung/results/result_bild2.jpg)

   ![bild3](/2_Bildverarbeitung/results/result_bild3.jpg)
   
   ![bild4](/2_Bildverarbeitung/results/result_bild4.jpg)

#### Änderungen im Code im Vergleich zur Live-Kamera-Version
Im Vergleich zur Live-Kamera-Version wurden folgende Änderungen vorgenommen, um die Erkennung und Auswertung zu verbessern:

   1. Bilddateien statt Live-Kamera:
      - Der Code lädt statische Bilder mit `cv2.imread(image_name)` und verarbeitet sie einzeln.
      - Dies ermöglicht eine präzisere Analyse der Erkennungsgenauigkeit.

   2. Automatisches Speichern der Ergebnisse:
      - Die bearbeiteten Bilder (mit erkannten Markern und IDs) werden automatisch im Verzeichnis ./results/ gespeichert.
      - Beispiel: `result_bild1.jpg`, `result_bild2.jpg`.

   3. Skalierung der Bilder:
      - Die Bilder wurden skaliert, um sicherzustellen, dass sie vollständig auf dem Bildschirm angezeigt werden.
      - Dies wurde mit `cv2.resize()` erreicht.

   4. Schriftgröße und -dicke angepasst:
      - Die Schriftgröße (fontScale) und -dicke (thickness) wurden erhöht, um die IDs besser sichtbar zu machen.
      - Beispiel: `fontScale=1.5`, `thickness=4`.

   5. Fehlerbehandlung hinzugefügt:
      - Der Code überprüft, ob die Bilddatei existiert und korrekt geladen wurde. 
      - Falls nicht, wird eine Fehlermeldung ausgegeben.

   


## Wavefront

### Beschreibung
Der Wavefront Algorithmus dient dazu, den idealen Weg von Punkt A zu Punkt B zu finden.
Die dazu benötigte Karte wird binär in Hindernis (1) und kein Hindernis (0) beschrieben. 
Vom einem definierten Zielpunkt (2) werden allen anliegenden Feldern der Wert (3) zugeordnet. Den an diesen nun anliegenden 
Feldern wird der Wert (4) zugeordnet. Ein Hindernis kann nicht überschrieben werden. Nach diesem Prinzip erstreckt sich über die Karte ein Muster, welches nun zulässt, einen kürzesten Weg zum Start zu berechnen und festzulegen.


### erstes Beispiel
![Wavefront_einführung](/0_Bilder_Dokumentation/wavefront_einstieg.jpg)
Als ersten runtergebrochenen Versuch wurde eine sehr simple Karte in Gimp erstellt. Einem weißes Bild mit niedriger Auflösung von wenigen Pixeln wurde ein "Hindernis" in Form von schwarzen Pixeln hinzugefügt (Bild links). Diese Grafik wurde anschließend im Code in eine binäre Matrix umgewandelt (Bild mitte) und der Wavefront Algorithmus angewandt (Bild rechts).

### Funktionsweise des Algorithmus
Es wurden zwei Varianten des Algorithmus erstellt. Einmal mit Algorithmusregeln, die die relative Position vom berechnenden Punkt gegenüber des Endpunktes bei der Bestimmung vom Pfad zu berücksichtigen. Diese Datei heißt [bresenham_err.py](https://github.com/nichtMichel/AMS_WS24-25_G1_Projektarbeit/blob/main/3_Wavefront/Prototypen%20Daniel/bresenhamMitErrParam(Entwurf)/bresenham_err.py) und ist ein Prototyp, welcher zur nächsten Variante geführt hat.

Die Endvariante heißt [bresenham_Schulz.py](https://github.com/nichtMichel/AMS_WS24-25_G1_Projektarbeit/tree/main/3_Wavefront/Prototypen%20Daniel/BresenhamNachSchulz) und ist optimiert, um den kürzesten Pfad zwischen Start- und Endpunkt bei verringerter Rechendauer zu bestimmen.

#### Erklärung
1. Bild mit [**img_to_matrix()**](/3_Wavefront/Prototypen%20Daniel/BresenhamNachSchulz/wavefrontlib.py) einlesen und in eine binäre Matrix umwandeln.

2. Mit [**validate_points()**](/3_Wavefront/Prototypen%20Daniel/BresenhamNachSchulz/wavefrontlib.py) prüfen ob Start- und Zielkoordinaten gültig sind.

3. Von Punkt ausgehende Wellen (Schichten) erzeugen mit [**generate_wavefront()**](/3_Wavefront/Prototypen%20Daniel/BresenhamNachSchulz/wavefrontlib.py). Für jeden befahrbaren Punkt wird Distanz zum Ziel berechnet. 

4. Überflüssige Punkte werden mithilfe von [**delimite_wavefront()**](/3_Wavefront/Prototypen%20Daniel/BresenhamNachSchulz/wavefrontlib.py) und [**optimize_wavefront()**](/3_Wavefront/Prototypen%20Daniel/BresenhamNachSchulz/wavefrontlib.py)  in Hindernisse umgewandelt.

5. Zurückverfolgen aller möglichen Wege mit [**trace_paths()**](/3_Wavefront/Prototypen%20Daniel/BresenhamNachSchulz/wavefrontlib.py) und Auswählen des kürzesten Wegs mit [**find_shortest_path()**](/3_Wavefront/Prototypen%20Daniel/BresenhamNachSchulz/wavefrontlib.py).

6. Darstellung des kürzesten Pfads mit [**plot_martix_with_path()**](/3_Wavefront/Prototypen%20Daniel/BresenhamNachSchulz/wavefrontlib.py).

![delimted_wavefront](/0_Bilder_Dokumentation/delimited_wavefront.jpg)
Unnötige bzw. nicht zugängliche Punkte werden als Hindernisse markiert, um Rechenzeit beim späteren Pfadfinden einzusparen.

![shortest_path](/0_Bilder_Dokumentation/wavefront_sp.jpg)

Matrix mit Verfügbaren Pfaden, Überflüssige Punkte wurden als Hindernisse definiert, der kürzeste Pfad wurde berechnet und als rote Linie dargestellt.

### Webots Karte
Als aufbauendes Beispiel wird auf die Karte eingegangen, die im Nachfolgenden Webots-Projekt genutzt wird. 
Hier befindet sich der Start bei der 2 oben links im Bild, und das Ziel bei der Zahl 50 unten rechts.

![Beispiel einer Wavefront-Map](/0_Bilder_Dokumentation/wavefront.png)
Fortgeschrittene Hindernisse in einer Karte für späteres Webots-Projekt. Pfadplanung durch Wavefront-Algorithmus, Start oben links, Ziel unten Rechts.

### Hinweis
Das Skript kann leicht an verschiedene Anwendungsfälle angepasst werden, indem man die Matrix auf Grundlage eines Bildes oder durch manuelle Eingabe von Hindernissen erstellt.


# Webots

**Inhaltsverzeichnis [Webots - Projekt](#webots):**
- [Epuck](#e-puck)
- [Welt und Route](#welt-und-route)
- [Logikstruktur der Navigation](#logikstruktur-der-navigation)
   - [Erklärung der Hauptfunktion follow_path()](#hauptfunktion-follow_path)
   - [Logik der Navigation ohne Hindernisse](#logik-der-navigation-ohne-hindernisse)
   - [Logik der Vermeidung von Hindernisse](#logik-der-vermeidung-von-hindernisse)
      - [🛜 Detektion](#detektion)
      - [⤴️ Vermeidung](#vermeidung)


## E-puck
Der E-Puck ist ein Roboter, welcher 2 Reifen zur Bewegung besitzt und 7 Laser-Enfernungsmesser verbaut hat.

![E-Puck](/0_Bilder_Dokumentation/e_puck.jpg)

### IR-Sensoren
Der E-puck kann Hindernisse erkennen. Dafür werden Infrarotsensoren Sensoren benutzt. Diese Sensoren messen die Intensität vom reflektierten Infrarotlicht in 8 verschiedene Richtungen. Mit einem Grenzwert kann bestimmt werden, ob die Intensität der reflektierten Infrarotlicht so groß ist, dass es sich um ein Hindernis handelt, das in der Nähe liegt.

### Epuck Controller
Zunächst wird ein einfacher Controller für den E-Puck für Webots in Python erstellt. Von Webots wird ein Controller zur Verfügung gestellt, welcher den verwendeteten Roboter auf einer leichten Kurve fahren lässt und bei Wandkontakt sich in eine Richtung dreht.

Im Skript [michels_test_controller.py](https://github.com/nichtMichel/AMS_WS24-25_G1_Projektarbeit/blob/main/4_Webot%20Project/controllers/michels_test_controller/michels_test_controller.py) wurde ein Algorithmus erstellt, welcher den Roboter gerade aus fahren lässt. Bei Wandnähe dreht sich der Roboter eine zufällige Zeit in eine zufällige Richtung und versucht, weiter geradeaus zu fahren.

Als Ergebnis wird eine Heatmap erstellt, welche den Positionsverlauf des Roboters darstellt. Dies verdeutlicht, dass der Algorithmus zwar einfach und schnell ist, jedoch nicht dazu geeignet ist, einen Raum vollständig zu befahren. Es sind auch nach langer Simulationszeit noch immer Bereiche im Raum, die nicht befahren wurden. Auch wurden einige Positionen mehrfach befahren:

![Heatmap](/0_Bilder_Dokumentation/random_drive.png)


## Welt und Route

### Map:
Es wurde eine Karte erstellt, die mehrere Reihen von Bäumen darstellen soll. Als Vorbild diente ein Beispiel aus einem wissenschaftlichen Artikel "[Robot Farmers](/1_Wissenschaftliche_Artikeln/robot_farmers.pdf)". Es wurden zusätzlich Hindernisse definiert, wie Sie in der realen Welt vorkommen könnten.

![AMS_Garden_overview](/0_Bilder_Dokumentation/AMS_Garden_overview.png)
5 Reihen von Bäumen sind parallel aufgereiht, Startpunkt ist unten Links, Zielpunkt oben Rechts. Der Roboter soll zwischen den Bäumen hin- und herfahren und dabei den Hindernissen ausweichen.

### Meilensteine:
Die Meilensteine sind Punkte auf der Karte, die der Roboter befahren soll.
Die oberen und unteren Enden der Zwischenräume der Baumreihen werden als Meilensteine definiert, ebenso ein Start- und Endpunkt.
Zwischen den Meilensteinen wird ein Pfad über den Wavefront-Algorithmus definiert.


### Route:
Die Route wird durch die Meilensteine und den Wavefront Algorithmus definiert und beinhaltet zusätzlich zu den Meilensteinen auch noch weitere Punkte (Waypoints), die die Meilensteine verbinden.
Die Punkte befinden sich im Abstand von 5cm (konfigurierbar in [config.py](/4_Projekt_Webots/controllers/controller_d/config.py)) und werden in einem seperaten Fenster (GUI) während der Fahrt angezeigt.

### Hindernisse:
Werden auf dem Weg Hindernisse erkannt, wird vom Wavefront-Algorithmus zum Bug-Algorithmus gewechselt, bis das Hindernis umfahren ist. Danach wird der Wavefront-Pfad weiter verfolgt.

## Logikstruktur der Navigation

### Hauptfunktion - *follow_path()*

**follow_path()** ist die Hauptfunktion vom Roboter. Sie wird im while - main loop aufgerufen, damit der Roboter entlang seiner zugewiesenen GNSS-Route* navigiert. Dabei kann der Roboter selbständig Hindernisse vermeiden. Wie ihre Navigationslogik und Hindernisvermeidungsalgorithmus funktioniert, wird anschließend erklärt.

**Wie die GNSS-Route zugewiesen wird, wurde im Kapitel [Vorbereitung und Kalkulation der Route](#vorbereitung-und-kalkulation-der-route)
 erklärt*

### Logik der Navigation <u>ohne Hindernisse</u>

#### Skizze vom Aufbau
- follow_path()
   - [update_situation()](/4_Projekt_Webots/controllers/controller_d/robot.py)
   - If [robot.state](/4_Projekt_Webots/controllers/controller_d/robot.py) == **STATE_GPS**
   - [go_to_point( next waypoint )](/4_Projekt_Webots/controllers/controller_d/robot.py)
      - [obstacle_detected()](/4_Projekt_Webots/controllers/controller_d/robot.py)
      - [move_to_point( next waypoint )](/4_Projekt_Webots/controllers/controller_d/robot.py)
         - [get_heading_to_point()](/4_Projekt_Webots/controllers/controller_d/robot.py)
         - [move_towards_heading()](/4_Projekt_Webots/controllers/controller_d/robot.py)
            - [move_forward()](/4_Projekt_Webots/controllers/controller_d/robot.py)
            - [turn_left()](/4_Projekt_Webots/controllers/controller_d/robot.py)
            - [turn_right()](/4_Projekt_Webots/controllers/controller_d/robot.py)

#### Vorgehen
1. Erstmal wird der nächste Waypoint der Route, der Navigationsstatus und weitere Navigationsvariablen wie zum Beispiel, **heading**, durch [**update_situation()**](/4_Projekt_Webots/controllers/controller_d/robot.py) aktualisiert.

2. Wir prüfen, dass der **Status** vom Roboter == **STATE_GPS**. Dies bedeutet, dass bisher keine Hindernisse detektiert wurden und, dass es weiternavigiert wird, ohne Hindernisse zu berücksichtigen.

3. Dann weisen wir dem Roboter hin, zum nächsten Waypoint zu fahren ([**go_to_point()**](/4_Projekt_Webots/controllers/controller_d/robot.py)).

4. Der Roboter prüft ([**obstacle_detected()**](/4_Projekt_Webots/controllers/controller_d/robot.py)), ob es Hindernisse gibt, und entscheidet, ob er sie umfahren soll, oder ob es zum nächsten Waypoint weitergefahren werden soll ([**move_to_point**](/4_Projekt_Webots/controllers/controller_d/robot.py)).

5. Der Heading zum Waypoint wird mit [**get_heading_to_point()**](/4_Projekt_Webots/controllers/controller_d/robot.py) bestimmt.

6. [**move_towards_heading()**](/4_Projekt_Webots/controllers/controller_d/robot.py) kümmert sich darum, den Roboter nach links ([**turn_left()**](/4_Projekt_Webots/controllers/controller_d/robot.py)) oder rechts ([**turn_right()**](/4_Projekt_Webots/controllers/controller_d/robot.py)) zu drehen, wenn er nicht in Richtung Waypoint gerichtet ist. Ist der Roboter richtig orientiert, dann wird er mit [**move_forward()**](/4_Projekt_Webots/controllers/controller_d/robot.py) gerade aus zum Waypoint fahren.

#### Visuelle Darstellung

![Veranschaulichung Waypoint-Navigation](/0_Bilder_Dokumentation/waypoint_navigation.png)

### Logik der Vermeidung von Hindernisse

<h4 id="detektion">🛜 Detektion</h4>

##### Skizze vom Aufbau
- [follow_path()](/4_Projekt_Webots/controllers/controller_d/controller_d.py)
   - [update_situation()](/4_Projekt_Webots/controllers/controller_d/robot.py)
   - robot.state == **STATE_GPS**
   - [go_to_point( next waypoint )](/4_Projekt_Webots/controllers/controller_d/robot.py)
      - [obstacle_detected()](/4_Projekt_Webots/controllers/controller_d/robot.py)
      - robot.state = **STATE_OBSTACLE_LEFT** oder **STATE_OBSTACLE_LEFT**
      - Anpassung der Route

##### Erklärung
1. Die Navigationsvariablen (Navigations- und Sensordaten, etc.) werden mit [**update_situation()**](/4_Projekt_Webots/controllers/controller_d/robot.py) aktualisiert.

2. Der **Status** vom Roboter ist **STATE_GPS**, weil bisher keine Hindernisse detektiert worden sind.

3. Dann wird dem Roboter mit [**go_to_point()**](/4_Projekt_Webots/controllers/controller_d/robot.py) hingewiesen, zum nächsten Waypoint zu fahren.

4. Bevor es weitergefahren wird, wird in [**go_to_point()**](/4_Projekt_Webots/controllers/controller_d/robot.py) geprüft, ob es Hindernisse gibt.

5. Der **Status** vom Roboter wird auf **STATE_OBSTACLE_LEFT** oder **STATE_OBSTACLE_LEFT** eingestellt (abhängig davon, ob das Hinderniss sich links oder rechts befindet), damit bei der nächsten Iteration der Hauptschleife, die Funktion [**avoid_obstacle()**](/4_Projekt_Webots/controllers/controller_d/robot.py) aufgerufen wird.

6. Die ersten **AVOIDANCE_DELETE_WP_QTY**(Standard = 3)-Waypoints werden aus **robot.remaining_path** gelöscht. Dies wird gemacht, weil es sein kann, dass sich die detektierten Hindernisse auf den nächsten Waypoints der Route befinden. Indem man ein Paar wenige Waypoints löscht, gibt man dem Roboter genügend Flexibilität, um die Hindernisse umzugehen.

   **AVOIDANCE_DELETE_WP_QTY** kann angepasst werden mit Berücksichtigung auf die Größe der erwarteten Hindernisse (Abhängig von der Anwendung und Anwendungsort vom Roboter).

<h4 id="vermeidung">⤴️ Vermeidung</h4>

> ⚠️ **Beispiel für die Erklärung:** Hindernis steht links | Ausweichung auf rechte Seite

##### Skizze vom Aufbau
- [follow_path()](/4_Projekt_Webots/controllers/controller_d/controller_d.py)
   - [update_situation()](/4_Projekt_Webots/controllers/controller_d/robot.py)
   - robot.state == **STATE_OBSTACLE_LEFT**
   - [avoid_obstacle( Side.RIGHT )](/4_Projekt_Webots/controllers/controller_d/robot.py)
      - If obstacle_detected_front()
         - turn_right
      - If obstacle_detected_left()
         - move_forward()
      - If not obstacle_detected()
         - If das Hindernis wurde weniger als **AVOIDANCE_MAX_TRIES**(Standard = 2)-Mal ausgewichen
            - move_forward()
         - If wurde schon **AVOIDANCE_MAX_TRIES**(Standard = 2)-Mal ausgewichen
            - robot.state = **STATE_GPS**
      
##### Erklärung
1. Die Navigationsvariablen (Navigations- und Sensordaten, etc.) werden mit [**update_situation()**](/4_Projekt_Webots/controllers/controller_d/robot.py) aktualisiert.

2. Der **Status** vom Roboter ist **STATE_OBSTACLE_LEFT**, weil ein Hinderniss auf der linken Seite detektiert wurde.

3. Die Funktion [avoid_obstacle( Side.RIGHT )] wird mit dem "Side.RIGHT" Parameter aktiviert, um das Hindernis auf der rechten Seite (Entgegengesetzte) umzugehen.

4. Es wird geprüft, ob ein Hindernis vor dem Roboter liegt, wenn ja, wird nach rechts gelenkt, bis kein Hindernis mehr vor dem Roboter detektiert wird.

5. (Falls 4 nicht zutrifft) Es wird geprüft, ob das Hindernis sich nun auf der linken Seite befindet (wird detektiert, stört aber nicht den Weg). Wenn ja, dann wird gerade aus gefahren.

6. (Weder 4 noch 5 treffen zu) An dieser Stelle werden keine Hindernisse mehr erkannt. Es wird **AVOIDANCE_MAX_TRIES**-Mal gerade aus gefahren, solange keine Hindernisse detektiert werden. Ist man schon **AVOIDANCE_MAX_TRIES** gerade aus gefahren, und keine Hindernisse mehr sind detektiert worden, dann geht man davon aus, dass das Hindernis umgefahren wurde. Der Status vom Roboter wird zurück in den **STATE_GPS** gesetzt, damit der Roboter entlang seiner programmierten Route weiterfährt.

##### Visuelle Darstellung

![Veranschaulichung GNSS-Navigation kombiniert mit Hindernisvermeidung - 1](/0_Bilder_Dokumentation/Navigation_1.jpg)
![Veranschaulichung GNSS-Navigation kombiniert mit Hindernisvermeidung - 2](/0_Bilder_Dokumentation/Navigation_2.jpg)
![Veranschaulichung GNSS-Navigation kombiniert mit Hindernisvermeidung - 3](/0_Bilder_Dokumentation/Navigation_3.jpg)

