# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:10:50 2019

@author: Derek Boutin
"""

from numpy import math

locations = [(0,0), (9,0), (-17,3)] # Locations of reference points on the grid
wearable_location = [(3,2),(3,2),(3,2)] # Location of moveable point on the grid

location_pair_1 = locations[0] # Coordinate pair for the first reference point
location_pair_2 = locations[1] # Coordinate pair for the second reference point
location_pair_3 = locations[2] # Coordinate pair for the third reference point

d = location_pair_2[0] # x-coordinate of second reference point
i = location_pair_3[0] # x-coordinate of third reference point
j = location_pair_3[1] # y-coordinate of third reference point


def distance_to_wearable(lon1, lat1, lon2, lat2):
    # This function calculates the distance from each reference point to the 
    # moveable point
    x_dist = abs(lon1-lon2)
    y_dist = abs(lat1-lat2)
    distance = math.sqrt((x_dist)**2 + (y_dist)**2)
    #print("Distance: ", distance)
    return distance

def distance(locations, wearable_location):
    # This function creates an array of distances from each reference point to 
    # the moveable point
    distances = []
    for location, wearable in zip(locations,wearable_location):
        distances.append(distance_to_wearable(location[0],location[1], wearable[0], wearable[1]))
         
    return distances

result = distance(locations, wearable_location) #Calls distance function
print(result)


x_coord = ((result[0]**2-result[1]**2+d**2)/(2*d)) # Equation for x-coordinate

y_coord = ((result[0]**2-result[2]**2+x_coord**2+(x_coord-i)**2+j**2)/(2*j)) # Equation for y-coordinate

print("x-coordinate: ",x_coord)
print("y-coordinate: ",y_coord)   
    
    
    
    
    