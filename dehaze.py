import cv2
import numpy as np


def read_img(path):
    try:
        img = cv2.imread(path)
    except:
        return None
    return img.astype('float64') / 255


def dark_channel(img, size = 15):
    r, g, b = cv2.split(img)
    min_img = cv2.min(r, cv2.min(g, b))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    dc_img = cv2.erode(min_img,kernel)
    return dc_img


def get_atmo(img, percent = 0.001):
    mean_perpix = np.mean(img, axis = 2).reshape(-1)
    mean_topper = mean_perpix[:int(img.shape[0] * img.shape[1] * percent)]
    return np.mean(mean_topper)


def get_trans(img, atom, w = 0.95):
    x = img / atom
    t = 1 - w * dark_channel(x, 15)
    return t


def dehaze(path):
    img = read_img(path)
    atom = get_atmo(img)
    trans = get_trans(img, atom)

    result = np.empty_like(img)
    for i in range(3):
        result[:, :, i] = (img[:, :, i] - atom) / trans + atom

    cv2.imshow("source",img)
    cv2.imshow("result", result)
    cv2.waitKey()

if __name__ == '__main__':
    dehaze('1.png')