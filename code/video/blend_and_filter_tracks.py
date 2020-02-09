"""
blend_and_filter_tracks.py

takes two tracked arrays and appends and filters them
  Created by Ed on 2/6/2020
 """
import numpy as np
from scipy.signal import savgol_filter

frame_width = 480
frame_height = 270

first_file = 'MVI_9465_small_tracked-3060-13686-2.csv'
# second_file = 'MVI_9463_small_tracked-9001-21663-2.csv'

if __name__ == '__main__':

    # load the files to blend
    faces = np.loadtxt(first_file, delimiter=',', dtype=np.int32)
    # more_faces = np.loadtxt(second_file, delimiter=',', dtype=np.int32)

    all_faces = faces
    # all_faces = np.append(faces, more_faces, axis=0)

    # filter the face data with a moving average window of 5
    x_vals = savgol_filter(all_faces[:, 1], 5, 3)
    y_vals = savgol_filter(all_faces[:, 2], 5, 3)

    for i in range(len(all_faces)):
        all_faces[i][1] = round(x_vals[i])
        all_faces[i][2] = round(y_vals[i])

    # filter the face data again with a moving average window of 11
    x_vals = savgol_filter(all_faces[:, 1], 11, 3)
    y_vals = savgol_filter(all_faces[:, 2], 11, 3)

    for i in range(len(all_faces)):
        all_faces[i][1] = round(x_vals[i])
        all_faces[i][2] = round(y_vals[i])

    # need to trim face_window_array to stay within frame window
    max_width = frame_width - all_faces[0][3]
    max_height = frame_height - all_faces[0][4]
    for i in range(len(all_faces)):
        if all_faces[i][1] < 0:
            all_faces[i][1] = 0
        elif all_faces[i][1] > max_width:
            all_faces[i][1] = max_width
        if all_faces[i][2] < 0:
            all_faces[i][2] = 0
        elif all_faces[i][2] > max_height:
            all_faces[i][2] = max_height

    range_start = all_faces[0][0]
    range_end = all_faces[-1][0]

    out_filename = first_file[:22] + '-' + str(range_start) + '-' + str(range_end) + '-2A.csv'

    np.savetxt(out_filename, all_faces, delimiter=',')
    print('tracked data filtered and saved as ', out_filename)
