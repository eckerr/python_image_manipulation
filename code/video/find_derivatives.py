"""
find_derivatives both first and second for face movement in x and y
  Created by Ed on 1/15/2020
 """

import numpy as np

# load the filtered values we will start with
faces = np.loadtxt("front_faces_filter.csv", delimiter=',', dtype=np.int32)

# create an array to store the derivatives
x_deriv = np.zeros((faces.shape[0], 3), dtype=np.float32)

# loop thru arrays computing first derivative in x
for i in range(1, len(faces)-2):
    x_deriv[i][0] = faces[i][1]
    x_deriv[i][1] = (faces[i+1][1] - faces[i-1][1]) / 2

# loop thru array computing second derivative in x
for i in range(1, len(x_deriv)-2):
    x_deriv[i][2] = (x_deriv[i+2][1] - x_deriv[i-1][1]) / 2

print(x_deriv[6:300,:])




