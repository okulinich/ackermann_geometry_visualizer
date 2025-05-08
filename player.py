from visualizer import RectangleVisualizer
import time
import math

def calculate_ackermann_angles(steering_angle, wheelbase, track_width):
    """
    Calculate the Ackermann steering angles for inner and outer wheels.
    
    Args:
        steering_angle: The steering angle in degrees
        wheelbase: Distance between front and rear axles
        track_width: Distance between left and right wheels
    
    Returns:
        tuple: (inner_wheel_angle, outer_wheel_angle) in degrees
    """
    # Convert steering angle to radians
    delta = math.radians(steering_angle)
    
    # Calculate turning radius to center of rear axle
    R = wheelbase / math.tan(delta)
    
    # Calculate angles for inner and outer wheels
    inner_angle = math.degrees(math.atan(wheelbase / (R - track_width/2)))
    outer_angle = math.degrees(math.atan(wheelbase / (R + track_width/2)))
    
    return inner_angle, outer_angle

def play(position_update, wheelbase, track_width):
    previous_ts = 0.0
    
    # Calculate delta t
    delta_time = position_update["ts"] - previous_ts
    previous_ts = position_update["ts"]
    
    # Calculate Ackermann angles
    inner_angle, outer_angle = calculate_ackermann_angles(
        position_update["angle"],
        wheelbase,
        track_width
    )
    
    # Calculate turning radius to center of rear axle
    turning_radius = wheelbase / math.tan(math.radians(position_update["angle"]))
    
    # Calculate angular speed
    angular_speed = position_update["velocity"] / turning_radius
    
    # Update heading
    heading = math.radians(position_update["angle"]) + angular_speed * delta_time
    
    return {
        "x": position_update["x"],
        "y": position_update["y"],
        "heading": math.degrees(heading),
        "inner_angle": inner_angle,
        "outer_angle": outer_angle
    }

# Test data
test_data = [
    {"ts": 1, "x": 2, "y": 3, "angle": 90, "velocity": 2},
    {"ts": 2, "x": 3, "y": 4, "angle": 100, "velocity": 2},
    {"ts": 3, "x": 4, "y": 5, "angle": 110, "velocity": 2},
    {"ts": 4, "x": 5, "y": 6, "angle": 120, "velocity": 2}
]

# Create visualizer instance
visualizer = RectangleVisualizer()

# Car dimensions
wheelbase = 4.0  # Distance between front and rear axles
track_width = 2.0  # Distance between left and right wheels
length, width = 4, 2

try:
    while True:
        # Rotate through different angles
        for item in test_data:
            # Calculate vehicle state with Ackermann steering
            state = play(item, wheelbase, track_width)
            
            # Update visualization
            visualizer.update_rectangle(
                state["x"],
                state["y"],
                length,
                width,
                state["heading"]
            )
            
            # Print Ackermann angles for debugging
            print(f"Inner wheel angle: {state['inner_angle']:.2f}°")
            print(f"Outer wheel angle: {state['outer_angle']:.2f}°")
            
            time.sleep(1)
except KeyboardInterrupt:
    print("\nAnimation stopped by user")
