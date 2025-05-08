from visualizer import RectangleVisualizer
import time
import math
import json
from typing import Dict, List, Tuple

def calculate_ackermann_angles(steering_angle: float, wheelbase: float, track_width: float) -> Tuple[float, float]:
    """
    Calculate the Ackermann steering angles for inner and outer wheels.
    
    Args:
        steering_angle: The steering angle in degrees
        wheelbase: Distance between front and rear axles
        track_width: Distance between left and right wheels
    
    Returns:
        tuple: (inner_wheel_angle, outer_wheel_angle) in degrees
    """
    # Handle zero steering angle case
    if abs(steering_angle) < 0.1:  # Using small threshold to handle near-zero angles
        return 0.0, 0.0
    
    # Convert steering angle to radians
    delta = math.radians(steering_angle)
    
    # Calculate turning radius to center of rear axle
    R = wheelbase / math.tan(delta)
    
    # Calculate angles for inner and outer wheels
    inner_angle = math.degrees(math.atan(wheelbase / (R - track_width/2)))
    outer_angle = math.degrees(math.atan(wheelbase / (R + track_width/2)))
    
    return inner_angle, outer_angle

def get_latest_position(events: List[Dict], current_time: float) -> Dict:
    """
    Get the latest position update before or at the current time.
    """
    latest_position = None
    for event in events:
        if event["type"] == "position" and event["ts"] <= current_time:
            latest_position = event
        elif event["ts"] > current_time:
            break
    return latest_position

def get_latest_velocity(events: List[Dict], current_time: float) -> Dict:
    """
    Get the latest velocity update before or at the current time.
    """
    latest_velocity = None
    for event in events:
        if event["type"] == "velocity" and event["ts"] <= current_time:
            latest_velocity = event
        elif event["ts"] > current_time:
            break
    return latest_velocity

def play(events: List[Dict], wheelbase: float, track_width: float, current_time: float) -> Dict:
    """
    Calculate vehicle state at the current time using the latest position and velocity data.
    """
    # Get latest position and velocity updates
    position = get_latest_position(events, current_time)
    velocity_data = get_latest_velocity(events, current_time)
    
    if not position or not velocity_data:
        raise ValueError(f"No valid position or velocity data found for time {current_time}")
    
    # Calculate Ackermann angles
    inner_angle, outer_angle = calculate_ackermann_angles(
        velocity_data["steering_angle"],
        wheelbase,
        track_width
    )
    
    # Calculate turning radius to center of rear axle
    if abs(velocity_data["steering_angle"]) < 0.1:
        turning_radius = float('inf')  # Infinite radius for straight line
        angular_speed = 0.0  # No rotation when going straight
    else:
        turning_radius = wheelbase / math.tan(math.radians(velocity_data["steering_angle"]))
        angular_speed = velocity_data["velocity"] / turning_radius
    
    return {
        "x": position["x"],
        "y": position["y"],
        "heading": velocity_data["steering_angle"],
        "inner_angle": inner_angle,
        "outer_angle": outer_angle,
        "velocity": velocity_data["velocity"],
        "turning_radius": turning_radius
    }

# Load test data from JSON file
with open('test_data.json', 'r') as f:
    data = json.load(f)
    events = data['events']

# Create visualizer instance
visualizer = RectangleVisualizer()

# Car dimensions
wheelbase = 4.0  # Distance between front and rear axles
track_width = 2.0  # Distance between left and right wheels

try:
    current_time = 0.0
    while current_time <= events[-1]["ts"]:
        # Calculate vehicle state with Ackermann steering
        state = play(events, wheelbase, track_width, current_time)
        
        # Update visualization
        visualizer.update_rectangle(
            state["x"],
            state["y"],
            wheelbase,
            track_width,
            state["heading"]
        )
        
        # Print debug information
        print(f"Time: {current_time:.1f}s")
        print(f"Position: ({state['x']:.1f}, {state['y']:.1f})")
        print(f"Velocity: {state['velocity']:.1f} m/s")
        print(f"Inner wheel angle: {state['inner_angle']:.1f}°")
        print(f"Outer wheel angle: {state['outer_angle']:.1f}°")
        if state['turning_radius'] != float('inf'):
            print(f"Turning radius: {state['turning_radius']:.1f} m")
        else:
            print("Turning radius: infinite (straight line)")
        print("---")
        
        time.sleep(0.1)  # Update at 10Hz
        current_time += 0.1
except KeyboardInterrupt:
    print("\nAnimation stopped by user")
