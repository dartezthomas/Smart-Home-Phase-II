import numpy as np
from math import sqrt
from collections import Counter



def k_nearest_neighbor(data, predict, k):
	distances = []
	for group in data:
		for features in data[group]:
			euclidean_distance = np.linalg.norm(np.array(features)-np.array(predict))
			distances.append([euclidean_distance, group]) 

	votes = [i[1] for i in sorted(distances)[:k]]
	vote_result = Counter(votes).most_common(1)[0][0]
	return vote_result

dataset = {'bedroom':[[-60,-75,-92], [-62,-77,-90],[-63,-71,-88]], 'kitchen:':[[-90, -75, -62], [-92,-79, -59], [-89, -76, -64]], 'living-room': [[-75, -62, -75], [-77, -62, -80], [-74, -65, -82]]}

new_features = [-63, -78, -94]
feature_2 = [-95, -79, -65]
result = k_nearest_neighbor(dataset, new_features, 3)

print(result)
result1 = k_nearest_neighbor(dataset, feature_2, 3)
print(result1)
