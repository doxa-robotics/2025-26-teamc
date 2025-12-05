import math
import * from vex

def s_arc(radius_right_mm, angle_right_deg, 
                     radius_left_mm, angle_left_deg, speed_percent=70):

    track_width_mm = 300
    pie = math.pi

    theta_r = angle_right_deg * (pie / 180)
    ratio_r = (radius_right_mm + track_width_mm/2) / (radius_right_mm - track_width_mm/2)
    left_speed_r = speed_percent
    right_speed_r = speed_percent * ratio_r

    left_distance_r = theta_r * (radius_right_mm + track_width_mm/2)
    right_distance_r = theta_r * (radius_right_mm - track_width_mm/2)
    
    left_motor.spin_for(FORWARD, left_distance_r, MM, velocity=left_speed_r, wait=False)
    right_motor.spin_for(FORWARD, right_distance_r, MM, velocity=right_speed_r)
    
    
    theta_l = angle_left_deg * 3.1416 / 180
    ratio_l = (radius_left_mm - track_width_mm/2) / (radius_left_mm + track_width_mm/2)
    left_speed_l = speed_pct * ratio_l
    right_speed_l = speed_pct
    
    left_distance_l = theta_l * (radius_left_mm - track_width_mm/2)
    right_distance_l = theta_l * (radius_left_mm + track_width_mm/2)
    
    left_motor.spin_for(FORWARD, left_distance_l, MM, velocity=left_speed_l, wait=False)
    right_motor.spin_for(FORWARD, right_distance_l, MM, velocity=right_speed_l)

