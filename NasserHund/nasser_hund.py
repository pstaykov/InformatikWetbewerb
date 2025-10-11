def read_parkdata(filename):
    with open(filename, "r") as file:
        # Wege einlesen 
        k = int(file.readline().strip())  # Anzahl der Wege
        paths = []
        for _ in range(k):
            x1, y1, x2, y2 = map(float, file.readline().split())
            paths.append(((x1, y1), (x2, y2)))  # ein Weg = zwei Punkte (Start, Ende)

        # Seen einlesen 
        s = int(file.readline().strip())  # Anzahl der Seen
        lakes = []
        for _ in range(s):
            n = int(file.readline().strip())  # Anzahl der Eckpunkte des Sees
            polygon_points = []
            for _ in range(n):
                x, y = map(float, file.readline().split())
                polygon_points.append((x, y))
            lakes.append(polygon_points)

    return paths, lakes

