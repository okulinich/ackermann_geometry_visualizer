from draw import RectangleVisualizer
import time

test_data = [{"x": 2, "y":3, "angle":90},
             {"x": 3, "y":4, "angle":100},
             {"x": 4, "y":5, "angle":110},
             {"x": 5, "y":6, "angle":120}]

# Create visualizer instance
visualizer = RectangleVisualizer()

# Initial position
x, y = 2, 3
width, height = 4, 2

try:
    while True:
        # Rotate through different angles
        for item in test_data:
            visualizer.update_rectangle(item["x"], item["y"], width, height, item["angle"])
            time.sleep(1)
except KeyboardInterrupt:
    print("\nAnimation stopped by user")
