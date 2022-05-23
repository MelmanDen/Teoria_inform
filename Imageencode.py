from PIL import Image
import random
import numpy as np
import copy
import matplotlib.pyplot as plt
import os, sys

im = Image.open('testpic2.jpg').resize((400,400))
a = np.array(im)
im.show()
b = copy.deepcopy(a)


def zashumlenie(matrica):
    shumka = random.randint(1, 255)
    oshibka = bin(matrica ^ shumka)
    return int(oshibka,2)


for i in range(len(a)):
    for j in range(len(a[i])):
        for m in range(len(a[i][j])):
            a[i][j][m] = zashumlenie(a[i][j][m])


im3 = Image.fromarray(a, mode="RGB")
im3.save('myimg.jpg')
im3.show()

#
#
#
#
# img = Image.open("testpic.png").resize((400,400))
# img.convert("RGB").save('myimg.jpg')

# im2 = Image.open("testpic.png")
# if not im2.mode == 'RGB':
#   im2 = im2.convert('RGB')
#   im2.save("image_name.jpg","JPEG")
# rgb_im = Image.open('image_name.jpg')
# print(rgb_im.format, rgb_im.size, rgb_im.mode)
# rgb_im.show()
