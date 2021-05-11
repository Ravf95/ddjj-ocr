from os import mkdir
from os import path
from os import listdir
from os import sep as os_sep
from subprocess import Popen 
from subprocess import PIPE

from PIL import Image
from cv2 import imread
from pytesseract import Output
from pytesseract import image_to_data
from pdf2image import convert_from_path

def pdfseparate(file, dumpfolder):
    try:
        folder = file.strip().split(os_sep)
        folder = folder[len(folder) -1].split('.')[0]
        outfolder = path.join(dumpfolder, folder)
        if not path.isdir(outfolder):
            mkdir(outfolder)

        fileformat = path.join(outfolder, 'part-%d.pdf')
        proc = Popen(['pdfseparate', file, fileformat], stdout = PIPE, stderr = PIPE)
    except Exception as e:
        print(str(e))
    else:
        outs, errs = proc.communicate()
        if errs:
            return

        if not outs:
            return [len(listdir(outfolder)), outfolder]

    return 0, None

def pdfparts2images(folder, outfolder):
    subfolders = folder.split(os_sep)
    outfolder = path.join(outfolder, subfolders[len(subfolders) -1])

    if not path.isdir(outfolder):
        mkdir(outfolder)

    for file in listdir(folder):
        filepath = path.join(folder, file)
        image = convert_from_path(filepath, dpi=300, single_file=True, fmt='jpeg',
             output_file=file.split('.')[0], jpegopt={'quality': 100}, output_folder=outfolder)

def main():
    '''
    count, folder = pdfseparate('../dataset/1558097_7054dc2ad56744930096bb38a1c7c4eb.pdf', '../pdfseparate-out')
    pdfparts2images(folder, '../pdf2images-out')
    '''

    # test: c.i is on the first page
    imgpath = '../pdf2images-out/1558097_7054dc2ad56744930096bb38a1c7c4eb/part-1.jpg'
    img = imread(imgpath)
    d = image_to_data(img, output_type=Output.DICT)
    n_boxes = len(d['level'])
    
    x,y,w,h = 0,0,0,0
    for i in range(n_boxes):
        x, y, w, h = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        if 'suscribe' in d['text'][i]:
            print(d['text'][i], x, y, w, h)
            break

    im = Image.open(imgpath)
    w, h = im.size
    # (left, upper, right, lower).
    box = (x, y - 50, w - 600, y + 100)
    region = im.crop(box)

    # A4 portrait
    a4 = Image.new("RGB", size=(2480, 3508))
    a4.paste(region, (0,0))
    a4.save("ci.jpg", "jpeg")

if __name__ == '__main__':
    main()
