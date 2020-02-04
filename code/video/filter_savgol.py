"""
  numpy filtering of front_faces_filled1.csv file
  Created by Ed on 1/14/2020
 """

import numpy as np
from scipy.signal import savgol_filter

in_filename = 'MVI_9466_small_tracked-8500-17000-.csv'
# in_filename = 'MVI_9464_filled.csv'
out_filename = in_filename[:-4] + 'filter.csv'
# out_filename = in_filename[:-10] + 'filter.csv'

# read the faces file
faces = np.loadtxt(in_filename, delimiter=',', dtype=np.int32)

x_vals = savgol_filter(faces[:, 1], 5, 3)
y_vals = savgol_filter(faces[:, 2], 5, 3)

for i in range(len(faces)):
    faces[i][1] = round(x_vals[i])
    faces[i][2] = round(y_vals[i])

print(faces)


np.savetxt(out_filename, faces, delimiter=',')
print('filtered data saved as ', out_filename)




