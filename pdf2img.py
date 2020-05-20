#coding:utf-8
import fitz
import os
from file_path import get_path

'''
# 将PDF转化为图片
pdfPath pdf文件的路径
imgPath 图像要保存的文件夹
zoom_x x方向的缩放系数
zoom_y y方向的缩放系数
rotation_angle 旋转角度
'''
def pdf_image(pdfPath,imgPath,zoom_x,zoom_y,rotation_angle):
    # 打开PDF文件
    pdf = fitz.open(pdfPath)
    # 逐页读取PDF
    for pg in range(0, pdf.pageCount):
        page = pdf[pg]
        # 设置缩放和旋转系数
        trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotation_angle)
        pm = page.getPixmap(matrix=trans, alpha=False)
        # 开始写图像
        pm.writePNG(imgPath+str(pg)+".png")
    pdf.close()
    


if __name__ == '__main__':

    pdf_root = './pdfs/'
    pdf_paths, pdf_names = get_path(pdf_root, ('.pdf',))
    file_count = len(pdf_paths)
    print('found {} pdf files'.format(file_count))
    i = 1
    for pdf_path, pdf_name in zip(pdf_paths,pdf_names):
        if not pdf_path:
            continue
        print('processing {}th file...'.format(i))
        pdf_image_path = pdf_root + pdf_name
        if not os.path.exists(pdf_image_path):
            os.makedirs(pdf_image_path)
        pdf_image_path += '/'
        pdf_image(pdf_path, pdf_image_path,5,5,0)
        i += 1
    print('finished!')
    
