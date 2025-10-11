from shapely.geometry import LineString, Polygon
from shapely.ops import nearest_points
import matplotlib.pyplot as plt
import os

def read_parkdata(filename):
    with open(filename, "r") as file:
        # Wege einlesen 
        k = int(file.readline().strip())
        paths = []
        for _ in range(k):
            x1, y1, x2, y2 = map(float, file.readline().split())
            paths.append(((x1, y1), (x2, y2)))

        # Seen einlesen 
        s = int(file.readline().strip())
        lakes = []
        for _ in range(s):
            n = int(file.readline().strip())
            polygon_points = []
            for _ in range(n):
                x, y = map(float, file.readline().split())
                polygon_points.append((x, y))
            lakes.append(polygon_points)

    return paths, lakes


input_path = os.path.join(os.path.dirname(__file__), "eingaben", "hund05.txt")
paths, lakes = read_parkdata(input_path)

# Convert to Shapely geometries
paths = [LineString(path) for path in paths]
lakes = [Polygon(coords) for coords in lakes]

# Find minimal distance and corresponding geometries
min_pair = min(
    ((path, lake, path.distance(lake)) for path in paths for lake in lakes),
    key=lambda x: x[2]
)
nearest_path, nearest_lake, min_distance = min_pair

# Get the nearest points (one on path, one on lake)
p1, p2 = nearest_points(nearest_path, nearest_lake)

# --- PLOT ---
for lake in lakes:
    x, y = lake.exterior.xy
    plt.fill(x, y, alpha=0.5, fc='blue', ec='black')

for path in paths:
    x, y = path.xy
    plt.plot(x, y, color='brown', linewidth=2)

# Highlight nearest path in orange
x, y = nearest_path.xy
plt.plot(x, y, color='orange', linewidth=3, label="Nearest path")

# Draw red line showing minimal distance
plt.plot([p1.x, p2.x], [p1.y, p2.y], color='red', linewidth=2, label="Shortest distance")

# Mark the closest points
plt.scatter([p1.x, p2.x], [p1.y, p2.y], color='red', s=60, zorder=5)

plt.title(f"Nearest lake distance: {min_distance:.3f}")
plt.gca().set_aspect("equal", adjustable="box")
plt.legend()
plt.show()
