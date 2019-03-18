from scipy import optimize
from numpy import math

###############################################################################

"""
This portion of code finds the distances from each reference point and the 
moveable point and stores these values in an array
"""

initial_location = (0,0) # Initial guess for moveable point
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
    
    return distance

def distance(locations, wearable_location):
    # This function creates an array of distances from each reference point to 
    # the moveable point
    distances = []
    for location, wearable in zip(locations,wearable_location):
        distances.append(distance_to_wearable(location[0],location[1], wearable[0], wearable[1]))
         
    return distances

module_distances = distance(locations, wearable_location) #Calls distance function

###############################################################################

"""
This portion of code uses the mean squared error function to find the x and y
coordinates of the moveable point
"""

def great_circle_distance(lon1, lat1, lon2, lat2): 
    # This function calculates the great circle distance between two points 
    
    x_dist = abs(lon1-lon2);
    y_dist = abs(lat1-lat2);
    distance = math.sqrt((x_dist)**2 + (y_dist)**2)
    return distance

def mse(x, locations, distances):
    # This function calculates the mean squared error of the reference points
    # and the point x    
    
	mse = 0.0
	for location, distance in zip(locations, distances):
		distance_calculated = great_circle_distance(x[0], x[1], location[0], location[1])
		mse += math.pow(distance_calculated - distance, 2.0)
	return mse / 3

   
result = optimize.minimize( # This function minimizes the error function
	mse,                         # The error function
	initial_location,            # The initial guess
	args=(locations, module_distances), # Additional parameters for mse
	method='L-BFGS-B',           # The optimisation algorithm
	options={
		'ftol':1e-5,         # Tolerance
		'maxiter': 1e+7      # Maximum iterations
	})
location = result.x # Calls the minimize function
print("x-coordinate: ", location[0])
print("y-coordinate: ", location[1])