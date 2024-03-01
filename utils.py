import math

def direction_changes(data, coord, sensitivity):
    extreme_point = getattr(data[0], coord)
    num_changes = 0

    # Iterate over pairs of consecutive data points
    for current in data[1:]:

        current_val = getattr(current, coord)

        # If the difference between neighboring points is significant...
        if abs(extreme_point - current_val) > sensitivity:

            # Determine the direction
            if extreme_point > current_val:
                current_dir = 'rising'
            else:
                current_dir = 'falling'

            # Check for a direction change
            if 'prev_dir' in locals() and current_dir != prev_dir:
                num_changes += 1
                extreme_point = current_val

            # First time direction is determined
            elif 'prev_dir' not in locals():
                prev_dir = current_dir
                extreme_point = current_val

    return num_changes


def calculate_velocity(start_point, end_point, time_taken):
    start_point = (start_point.x, start_point.y)
    end_point = (end_point.x, end_point.y)
    distance = math.sqrt((end_point[0] - start_point[0]) ** 2 + (end_point[1] - start_point[1]) ** 2)
    velocity = distance / time_taken
    return velocity


