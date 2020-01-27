"""
remove_jitter.py

reads thru face position data, looking at 3 consecutive entries,
 if first and third entry are the same, change middle value to match.

  Created by Ed on 1/15/2020
 """

import numpy as np

in_filename = 'MVI_9464_filter.csv'
out_filename = in_filename[:-10] + 'rem_jitter.csv'

x_changed_count = 0
y_changed_count = 0

# load the filtered values we will start with
faces = np.loadtxt("MVI_9464_filter.csv", delimiter=',', dtype=np.int32)
# faces = np.loadtxt("MVI_9464_filled.csv", delimiter=',', dtype=np.int32)

# loop through faces array counting suspect values

for i in range(2, len(faces)-3):
    if faces[i+1][1] == faces[i-1][1] and faces[i][1] != faces[i-1][1]:
        faces[i][1] = faces[i-1][1]
        x_changed_count += 1
        print(faces[i][0], faces[i-2][1], faces[i-1][1], faces[i][1], faces[i+1][1], faces[i+2][1], faces[i][1] - faces[i-1][1])

for i in range(2, len(faces)-3):
    if faces[i+1][2] == faces[i-1][2] and faces[i][2] != faces[i-1][2]:
        faces[i][2] = faces[i-1][2]
        y_changed_count += 1
        print(faces[i][0], faces[i-2][2], faces[i-1][2], faces[i][2], faces[i+1][2], faces[i+2][1], faces[i][2] - faces[i-1][2])

print("x changed: ", x_changed_count)
print("y changed: ", y_changed_count)

np.savetxt(out_filename, faces, delimiter=',')
print('filtered data saved as ', out_filename)





