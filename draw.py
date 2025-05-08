import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class RectangleVisualizer:
    def __init__(self):
        # Set the matplotlib style to dark background
        plt.style.use('dark_background')
        
        # Create a new figure and axes (plot area)
        self.fig, self.ax = plt.subplots()
        
        # Initialize rectangle as None (will be created later)
        self.rect = None
        
        # Call setup_plot to configure the plot area
        self.setup_plot()
        
        # Show the plot window without blocking the program
        plt.show(block=False)
        
    def setup_plot(self):
        # Set the x-axis limits from -2 to 8
        self.ax.set_xlim(-20, 20)
        
        # Set the y-axis limits from -1 to 7
        self.ax.set_ylim(-1, 40)

        # Make sure the plot maintains equal aspect ratio
        # (so the rectangle doesn't look stretched)
        self.ax.set_aspect('equal')
        
        # Add a grid with gray color and 30% opacity
        self.ax.grid(True, color='gray', alpha=0.3)
        
        # Enable interactive mode for real-time updates
        plt.ion()
        
    def update_rectangle(self, x, y, width, height, heading_deg):
        # If there's an existing rectangle, remove it
        if self.rect is not None:
            self.rect.remove()
            
        # Create a new rectangle with the given parameters:
        # - (x, y): position of the bottom-left corner
        # - width, height: dimensions of the rectangle
        # - angle: rotation angle in degrees
        # - edgecolor: color of the rectangle's border (lime green)
        # - facecolor: color inside the rectangle (none = transparent)
        # - lw: line width of the border
        self.rect = patches.Rectangle(
            (x, y), width, height,
            angle=heading_deg,
            edgecolor='lime',
            facecolor='none',
            lw=2
        )
        
        # Add the new rectangle to the plot
        self.ax.add_patch(self.rect)
        
        # Redraw the canvas to show the changes
        self.fig.canvas.draw()
        
        # Process any pending events
        self.fig.canvas.flush_events()
        
        # Add a small pause to ensure the plot updates
        plt.pause(0.001)
