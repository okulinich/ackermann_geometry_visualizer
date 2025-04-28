import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_rectangle(x, y, width, height, heading_deg):
    fig, ax = plt.subplots()
    
    # Create a rectangle
    rect = patches.Rectangle(
        (x, y), width, height,
        angle=heading_deg,
        edgecolor='blue',
        facecolor='none',
        lw=2
    )
    
    ax.add_patch(rect)
    
    # Set limits to make it visible
    ax.set_xlim(x - width, x + width*2)
    ax.set_ylim(y - height, y + height*2)
    ax.set_aspect('equal')
    
    plt.grid(True)
    plt.show()

# Example usage
draw_rectangle(x=2, y=3, width=4, height=2, heading_deg=30)
