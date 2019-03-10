"""
 histogram plotting
  Created by Ed and Zack on 2/14/2019
 """
import cv2
import numpy as np

bins = np.arange(256).reshape(256, 1)

def create_blank_hist_pic():
    return np.zeros((150, 256, 3), dtype=np.uint8)

def hist_curve(image):
    hist_pic = create_blank_hist_pic()
    if len(image.shape) == 2:
        color = [(255, 255, 255)]
    elif image.shape[2] == 3:
        color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    for ch, col in enumerate(color):
        hist_item = cv2.calcHist([image],[ch], None, [256], [0, 256])
        cv2.normalize(hist_item, hist_item, 5, 145, cv2.NORM_MINMAX)
        hist = np.int32(np.around(hist_item))
        pts = np.int32(np.column_stack((bins, hist)))
        cv2.polylines(hist_pic, [pts], False, col)
    return np.flipud(hist_pic)

def hist_curve_split(image):
    hist_pics = []
    hist_pics.append(create_blank_hist_pic())
    hist_pics.append(create_blank_hist_pic())
    hist_pics.append(create_blank_hist_pic())
    hist_pics.append(create_blank_hist_pic())

    if image.shape[2] == 3:
        color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    for ch, col in enumerate(color):
        hist_item = cv2.calcHist([image],[ch], None, [256], [0, 256])
        cv2.normalize(hist_item, hist_item, 5, 145, cv2.NORM_MINMAX)
        hist = np.int32(np.around(hist_item))
        pts = np.int32(np.column_stack((bins, hist)))
        cv2.polylines(hist_pics[ch], [pts], False, col)
        hist_pics[ch] = np.flipud(hist_pics[ch])
    return hist_pics

def hist_lines_split(image):
    hist_pics = []
    hist_pics.append(create_blank_hist_pic())
    hist_pics.append(create_blank_hist_pic())
    hist_pics.append(create_blank_hist_pic())
    hist_pics.append(create_blank_hist_pic())


    color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    for ch, col in enumerate(color):
        hist_item = cv2.calcHist([image],[ch], None, [256], [0, 256])
        cv2.normalize(hist_item, hist_item, 5, 145, cv2.NORM_MINMAX)
        hist = np.int32(np.around(hist_item))
        for x, y in enumerate(hist):
            cv2.line(hist_pics[ch], (x, 5), (x, y), col)
        hist_pics[ch] = np.flipud(hist_pics[ch])
    return hist_pics

def hist_lines(image):
    hist_pic = create_blank_hist_pic()
    if len(image.shape) !=2:
        print("hist_lines works with a grayscale image only")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist_item = cv2.calcHist([image], [0], None, [256], [0,256])
    cv2.normalize(hist_item, hist_item, 5, 145, cv2.NORM_MINMAX)
    hist = np.int32(np.around(hist_item))
    for x, y in enumerate(hist):
        cv2.line(hist_pic, (x, 5), (x, y), (255, 255, 255))
    return np.flipud(hist_pic)



