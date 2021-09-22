import torch
import numpy as np


def decrease_color(value):
    """
    (0~255)の値を4段階(0~3)に減色
    入力: int(0~255), 出力: int(0~3)
    """
    if value < 64:
        return 0
    elif value < 128:
        return 1
    elif value < 196:
        return 2
    else:
        return 3


def convert_image_to_histogram(image):
    """
    (3, 32, 32) の画像を (1, 32, 32) に変換, その後,ヒストグラム(64次元ベクトル) に変換
    値は64段階(0~63)
    R(0~3)*1 + G(0~3)*4 + B(0~3)*16で算出
    入力: torch.Tensor, 出力: torch.Tensor
    """
    converted_image = np.empty((32, 32), dtype=np.int)
    for i in range(32):
        for j in range(32):
            pixel_value = 0
            for k in range(3):
                pixel_RGB_value = decrease_color(image[k, i, j].item())
                pixel_value += pixel_RGB_value * (4**k)
            converted_image[i][j] = pixel_value
    histogram = np.empty(64, dtype=np.int)
    for i in range(64):
        num = np.count_nonzero(converted_image == i)
        histogram[i] = num
    histogram = torch.from_numpy(histogram)
    return histogram
