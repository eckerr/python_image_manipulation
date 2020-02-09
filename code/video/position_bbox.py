"""
position_bbox.py

Looks at list of found faces within a range, then locates first found face
and displays bounding box. Loops to allow repositioning of bbox.

  Created by Ed on 2/1/2020
 """

import cv2
# import sys
# import csv
# import time
# import numpy as np
# from trackers import set_up_tracker
#
# x_offset = 35
# y_offset = 20
# track_width = 120
# track_height = 120

def adjust_bbox(in_frame, x, x_os, y, y_os, width, height):
    frame = in_frame
    ul_x = x
    ul_y = y
    offset_x = x_os
    offset_y = y_os
    width = width
    height = height

    # loop while we make positioning adjustments
    position = True
    while True:
        display_frame = frame.copy()
        # draw the found face bounding box
        cv2.rectangle(display_frame, (ul_x-offset_x, ul_y-offset_y),
                     (ul_x-offset_x+width, ul_y-offset_y+height), (0, 0, 255), 2, 1)
        if position:
            pos_text = 'Position'
        else:
            pos_text = 'Width'
        # Display adjustment type on frame - position, width
        cv2.putText(display_frame, pos_text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        # display offsets
        offsets_text = str(ul_x - offset_x) + '  ' + str(ul_y - offset_y) + '  ' + str(width) + '  ' + str(height)
        # offsets_text = str(ul_x) + '  ' + str(ul_y) +  '  ' + str(offset_x) + '  ' + str(offset_y) + '  ' + str(width) + '  ' + str(height)
        cv2.putText(display_frame, offsets_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        # display the frame for review
        # Display result
        cv2.imshow("adjust position", display_frame)

        # Exit if ESC pressed
        k = cv2.waitKey() & 0xff
        if k == 27:
            cv2.destroyAllWindows()
            print('final values: ', offset_x, offset_y, width, height)
            return [x, y, offset_x, offset_y, width, height]
        elif k == 97:
            print('left arrow - a')
            if position:
                offset_x += 10
            else:
                width -= 10
        elif k == 100:
            print('right arrow - d')
            if position:
                offset_x -= 10
            else:
                width += 10
        elif k == 119:
            print('up arrow - w')
            if position:
                offset_y += 10
            else:
                height -= 10
        elif k == 120:
            print('down arrow - x')
            if position:
                offset_y -= 10
            else:
                height += 10
        elif k == 115:
            print('toggle position / width - s')
            position = not position
            print(position)

        elif k == 65:
            print('left arrow - A')
            if position:
                offset_x += 1
            else:
                width -= 1
        elif k == 68:
            print('right arrow - D')
            if position:
                offset_x -= 1
            else:
                width += 1
        elif k == 87:
            print('up arrow - W')
            if position:
                offset_y += 1
            else:
                height -= 1
        elif k == 88:
            print('down arrow - X')
            if position:
                offset_y -= 1
            else:
                height += 1



    # ===============================================================================
    #     # save the window bounding box as the track area
    #     bbox = (ul_x-x_offset, ul_y-y_offset, track_width, track_height)






    # video.release()
    # print('Video released')
    #
    # np.savetxt(out_filename, face_window_array[range_start:range_end], delimiter=',')
    # print('tracked data saved as ', out_filename)
    #
    # cv2.destroyAllWindows()






