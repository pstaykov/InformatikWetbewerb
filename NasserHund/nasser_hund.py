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

from shapely.geometry import LineString, Polygon

# Example path
path = LineString([(0, 0), (5, 0)])

# Example lakes (polygons)
lakes = [
    Polygon([(2, 3), (4, 3), (4, 5), (2, 5)]),   # Lake A
    Polygon([(7, -1), (8, -1), (8, 0), (7, 0)]), # Lake B
    Polygon([(10, 10), (12, 10), (12, 12), (10, 12)])  # Lake C
]

# Find nearest polygon to the path
nearest_lake = min(lakes, key=lambda lake: path.distance(lake))
min_distance = path.distance(nearest_lake)

print("Nearest lake distance:", min_distance)
print("Nearest lake geometry:", nearest_lake)
