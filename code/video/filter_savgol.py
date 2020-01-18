"""
  numpy filtering of front_faces_filled1.csv file
  Created by Ed on 1/14/2020
 """

import numpy as np
from scipy.signal import savgol_filter


# read the faces file
faces = np.loadtxt('front_faces_filled2.csv', delimiter=',', dtype=np.int32)

x_vals = savgol_filter(faces[:, 1], 9, 3)
y_vals = savgol_filter(faces[:, 2], 9, 3)

for i in range(len(faces)):
    faces[i][1] = round(x_vals[i])
    faces[i][2] = round(y_vals[i])

print(faces)


np.savetxt('front_faces_filter.csv', faces, delimiter=',')




