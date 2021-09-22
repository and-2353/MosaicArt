# coding: utf-8
import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import cv2
import pickle
import time
from tqdm import tqdm
from utils import *


def preprocess_target_image():
    """
    target_image の読み込みと整形
    入力: なし, 出力: torch.Tensor, torch.Tensor, list(値: torch.Tensor)
    """
    with Image.open('target_data/idphoto.jpg') as img:
        target_image = np.expand_dims(np.asarray(img, np.float32), axis=0)
    target_image = torch.as_tensor(target_image) # target_image.size() = (1, 1024, 768, 3)
    target_image = target_image.unfold(1, 32, 32).unfold(2, 32, 32) # target_image.size() = (1, 32, 24, 3, 32, 32)
    target_image = target_image.reshape(-1, 3, 32, 32) # target_image.size() = (768, 3, 32, 32)

    photo_parts = torchvision.datasets.CIFAR100('./cifar-100',
        train=True, download=True, transform=transforms.ToTensor())
    with open('cifar100object.pickle', mode='rb') as f:
        photo_parts_histograms = pickle.load(f)
    return target_image, photo_parts, photo_parts_histograms


def search_similar_histogram(target_image, search_num, photo_parts_histograms, no_duplication_flag):
    """
    target_imageの全エリアに対してヒストグラムに変換 => search_num 回の間 photo_parts_histogram と比較
    入力: (torch.Tensor, int, list), 出力: int
    """
    most_similar_image_ids = []
    for i in tqdm(range(768)):
        most_similar_image_id = 0
        max_similarity = 0
        target_area = target_image[i]
        target_area_histogram = convert_image_to_histogram(target_area)
        target_area_histogram = target_area_histogram.numpy().astype(np.float32)
        for j in range(search_num):
            if no_duplication_flag and j in most_similar_image_ids:
                continue
            photo_parts_histogram = photo_parts_histograms[j].numpy().astype(np.float32)
            similarity = cv2.compareHist(target_area_histogram, photo_parts_histogram, cv2.HISTCMP_CORREL) # 相関
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_image_id = j
        most_similar_image_ids.append(most_similar_image_id)
    return most_similar_image_ids

def plotimage(ids, data):
    """
    ids からモザイクアートを生成し、png形式で保存
    入力: (list, list), 出力: なし
    """
    generated_image = torch.Tensor(768, 3, 32, 32)
    for i, item in enumerate(ids):
        generated_image[i] = data[item][0]
    torchvision.utils.save_image(generated_image, "generated.png", nrow=24, padding=0) # (32, 24, 3, 32, 32) で保存


def main():
    search_num = 50000
    no_duplication_flag = False # True: フォトパーツの重複を許容しない, False: 許容する
    target_image, photo_parts, photo_parts_histograms = preprocess_target_image()
    most_similar_image_ids = search_similar_histogram(target_image, search_num, photo_parts_histograms, no_duplication_flag)
    plotimage(most_similar_image_ids, photo_parts)


if __name__ == '__main__':
    t1 = time.time()
    main()
    t2 = time.time()
    elapsed_time = t2 - t1
    print(f'elapsed_time: {elapsed_time}')