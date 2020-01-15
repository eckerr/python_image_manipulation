"""
  numpy filtering of front_faces_filled1.csv file
  Created by Ed on 1/14/2020
 """

import numpy as np

# read the faces file
faces = np.loadtxt('front_faces_filled2.csv', delimiter=',', dtype=np.int32)


x_count_changed = 0

for i in range(len(faces)-2):
    if faces[i][1] == faces[i+2][1] and faces[i+1][1] != faces[i][1]:
        faces[i+1][1] = faces[i][1]
        x_count_changed += 1
        print(faces[i][1], faces[i+1][1], faces[i+2][1])

print('x count changed: ', x_count_changed)

y_count_changed = 0
for i in range(len(faces)-3):
    if (faces[i][2] == faces[i+2][2]) and (faces[i+1][2] != faces[i][2]):
        faces[i+1][2] = faces[i][2]
        y_count_changed += 1
        print(faces[i][2], faces[i+1][2], faces[i+2][2])

print('y count changed: ', y_count_changed)

four_x_count_changed = 0
for i in range(len(faces)-3):
    if (faces[i][1] == faces[i+3][1]) and (faces[i+1][1] != faces[i][1]):
        four_x_count_changed += 1
        print(faces[i][1], faces[i+1][1], faces[i+2][1], faces[i+3][1])

print('four x count changed: ', four_x_count_changed)

four_y_count_changed = 0
for i in range(len(faces)-3):
    if (faces[i][2] == faces[i+3][2]) and (faces[i+1][2] != faces[i][2]):
        four_y_count_changed += 1
        print(faces[i][2], faces[i+1][2], faces[i+2][2], faces[i+3][2])

print('four y count changed: ', four_y_count_changed)

np.savetxt('front_faces_filter.csv', faces, delimiter=',')




