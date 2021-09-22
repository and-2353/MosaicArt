# coding: utf-8
import torchvision
import torchvision.transforms as transforms
import pickle
import time
from tqdm import tqdm
from utils import *


def main():
    photo_parts = torchvision.datasets.CIFAR100('./cifar-100',train=True, download=True, transform=transforms.ToTensor())
    photo_parts_histograms = [] # list (each item = torch.Tensor)
    for i in tqdm(range(50000)):
        histogram = convert_image_to_histogram(photo_parts[i][0]* 255)
        photo_parts_histograms.append(histogram)
    with open('cifar100object.pickle',mode='wb') as f:
        pickle.dump(photo_parts_histograms, f)

if __name__ == '__main__':
    t1 = time.time()
    main() 
    t2 = time.time()
    elapsed_time = t2 - t1
    print(f'elapsed_time: {elapsed_time}')