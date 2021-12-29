# from PIL.Image import Image
import os
from datetime import datetime
# pip install pillow
import PIL.Image as pimg


class MergeImg:
    def __init__(self, vo):
        self.vo = vo

    def process(self, n):
        img_ls = []
        size_ls = []
        path = self.vo.context
        [img_ls.append(pimg.open(f'{path}/test{i}.gif')) for i in range(n)]
        for i, j in enumerate(img_ls):
            img_ls[i] = j.resize((300, 300))
            size_ls.append(j.size)
        new_image = pimg.new('RGB', (sum(i[0] for i in size_ls), size_ls[0][1]), (250, 250, 250))
        new_image.paste(img_ls[0], (0, 0))
        new_image.paste(img_ls[1], (size_ls[0][0]+50, 0))
        new_image.paste(img_ls[2], (size_ls[0][0] + size_ls[1][0]+50, 0))
        new_image.save(f"{path}/merged_image_{str(datetime.now())[:10]}.jpg", "JPEG")
        # new_image.show()
        # [os.remove(f'img/test{i}_.gif') for i in range(n)]
        return f"{path}/merged_image_{str(datetime.now())[:10]}.jpg"


    def test(self):
        image1 = pimg.open('../img/test1.gif')
        # image1.show()
        image2 = pimg.open('../img/test2.gif')
        # image2.show()
        image3 = pimg.open('../img/test3.gif')
        image1 = image1.resize((300, 300))
        image2 = image2.resize((300, 300))
        image3 = image3.resize((300, 300))
        image1_size = image1.size
        image2_size = image2.size
        image3_size = image3.size
        new_image = pimg.new('RGB', (3 * image1_size[0], image1_size[1]), (250, 250, 250))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (image1_size[0], 0))
        new_image.paste(image3, (image1_size[0]+image2_size[0], 0))
        new_image.save("img/merged_image.jpg", "JPEG")
        new_image.show()
        # os.remove('../img/test1.gif')
        # os.remove('../img/test2.gif')
        # os.remove('../img/test3.gif')
