# -*- coding: utf8 -*-
import os
import pascal_voc_io
import parseJson
import numpy as np
import globalvar as gl
import sys
gl._init()
gl.set_value('car', 0)
gl.set_value('bus', 0)
gl.set_value('person', 0)
gl.set_value('truck', 0)
gl.set_value('moto', 0)
gl.set_value('light', 0)#全局变量
categorys = ['car', 'bus', 'person',  'truck', 'moto','light']

def main(srcDir, dstDir): 
    # os.walk()
    # dirName是你所要遍历的目录的地址, 返回的是一个三元组(root,dirs,files)
    # root所指的是当前正在遍历的这个文件夹的本身的地址
    # dirs是一个 list ，内容是该文件夹中所有的目录的名字(不包括子目录)
    # files 同样是 list , 内容是该文件夹中所有的文件(不包括子目录)
    i = 1
    flagg=False
    count=0
    objname="bus"#要的物体名字
    for dirpath, dirnames, filenames in os.walk(srcDir):
#        print(dirpath, dirnames, filenames)
        for filepath in filenames:
            flagg = False
            fileName = os.path.join(dirpath,filepath)
            print(fileName)
            print("processing: {}, {}".format(i, fileName))
            i = i + 1
            xmlFileName = filepath[:-5] # remove ".json" 5 character
            # 解析该json文件，返回一个列表的列表，存储了一个json文件里面的所有方框坐标及其所属的类
            objs = parseJson.parseJson(str(fileName)) 
            # 如果存在检测对象，创建一个与该json文件具有相同名的VOC格式的xml文件
            if len(objs):
                tmp = pascal_voc_io.PascalVocWriter(dstDir, xmlFileName, (720,1280,3), fileName)
                for obj in objs:
                    tmp.addBndBox(obj[0],obj[1],obj[2],obj[3],obj[4])
                    if obj[4] == objname:
                        #flag[categorys.index(obj[4])]=flag[categorys.index(obj[4])]+1统计最大数量
                        flagg=True
                        
                        
                
                if flagg==False:
                    continue
                else:
                    count=count+1
                 # 只要30张就够了
                #print(flagg)
                if count == 11:
                    sys.exit()
                #tmp.save(categorys[np.argmax(flag)])统计最大数量
                tmp.save(objname)
            else:
                print(fileName)

if __name__ == '__main__':
    # test
    # these paths should be your own path
    #srcDir = '/home/lzh/Downloads/traffic/bdd100k/labels/100k/val'
    dstDir = '/home/lzh/Downloads/traffic/bdd100k/Annotations/val'
    srcDir = '/home/lzh/Downloads/traffic/bdd100k/labels/100k/train'
    #dstDir = '/media/xavier/SSD256/global_datasets/BDD00K/bdd100k/Annotations/train'
    main(srcDir, dstDir)

