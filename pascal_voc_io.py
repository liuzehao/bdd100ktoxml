#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree
from xml.dom.minidom import parseString
from shutil import copyfile#复制文件操作
import globalvar as gl

class PascalVocWriter:

    def __init__(self, foldername, filename, imgSize, databaseSrc='Unknown', localImgPath=None):
        '''
        params:
          foldername -- 要存储的xml文件的父目录
          filename -- xml文件的文件名
          imgSize -- 图片的尺寸
          databaseSrc -- 数据库名，这里不需要，默认为Unknown
          localImaPath -- xml文件里面的<path></path>标签的内容
      '''
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.boxlist = []
        self.localImgPath = localImgPath

    def prettify(self, elem):
        """
        params:
          elem -- xml的根标签，以<annotation>开始
        return:
          返回一个美观输出的xml（用到minidom），本质是一个str
        """
        xml = ElementTree.tostring(elem)
        dom = parseString(xml)
#        print(dom.toprettyxml('  '))
        prettifyResult = dom.toprettyxml('    ')
        return prettifyResult
        

    def genXML(self):
        """
        return:
          生成一个VOC格式的xml，返回一个xml的根标签，以<annotation>开始
        """
        # Check conditions
        if self.filename is None or \
                self.foldername is None or \
                self.imgSize is None or \
                len(self.boxlist) <= 0:
            return None

        top = Element('annotation') # 创建一个根标签<annotation>
        folder = SubElement(top, 'folder')  # 在根标签<annotation>下创建一个子标签<folder>
        folder.text = self.foldername       # 用self.foldername的数据填充子标签<folder>

        filename = SubElement(top, 'filename')  # 在根标签<annotation>下创建一个子标签<filename>
        filename.text = self.filename           # 用self.filename的数据填充子标签<filename>

        localImgPath = SubElement(top, 'path')  # 在根标签<annotation>下创建一个子标签<path>
        localImgPath.text = self.localImgPath   # 用self.localImgPath的数据填充子标签<path>
        #print(self.localImgPath)


        source = SubElement(top, 'source')          # 在根标签<annotation>下创建一个子标签<source>
        database = SubElement(source, 'database')   # 在根标签<source>下创建一个子标签<database>
        database.text = self.databaseSrc            # 用self.databaseSrc的数据填充子标签<database>

        size_part = SubElement(top, 'size')         # 在根标签<annotation>下创建一个子标签<size>
        width = SubElement(size_part, 'width')      # 在根标签<size>下创建一个子标签<width>
        height = SubElement(size_part, 'height')    # 在根标签<size>下创建一个子标签<height>
        depth = SubElement(size_part, 'depth')      # 在根标签<size>下创建一个子标签<depth>
        width.text = str(self.imgSize[1])           # 用self.imgSize[1]的数据填充子标签<width>
        height.text = str(self.imgSize[0])          # 用self.imgSize[0]的数据填充子标签<height>
        if len(self.imgSize) == 3:                  # 如果图片深度为3，则用self.imgSize[2]的数据填充子标签<height>，否则用1填充
            depth.text = str(self.imgSize[2])
        else:
            depth.text = '1'

        segmented = SubElement(top, 'segmented')
        segmented.text = '0'
        return top

    def addBndBox(self, xmin, ymin, xmax, ymax, name):
        '''
        将检测对象框坐标及其对象类别作为一个字典加入到self.boxlist中
        params:
          xmin -- 检测框的左上角的x坐标
          ymin -- 检测框的左上角的y坐标
          xmax -- 检测框的右下角的x坐标
          ymax -- 检测框的右下角的y坐标
          name -- 检测框内的对象类别名
        '''
        bndbox = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
        bndbox['name'] = name
        self.boxlist.append(bndbox)

    def appendObjects(self, top):
        '''
        在xml文件中加入检测框的坐标及其对象类别名
        params:
          top -- xml的根标签，以<annotation>开始
        '''
        for each_object in self.boxlist:
            object_item = SubElement(top, 'object')
            name = SubElement(object_item, 'name')
            name.text = str(each_object['name'])
            pose = SubElement(object_item, 'pose')
            pose.text = "Unspecified"
            truncated = SubElement(object_item, 'truncated')
            truncated.text = "0"
            difficult = SubElement(object_item, 'Difficult')
            difficult.text = "0"
            bndbox = SubElement(object_item, 'bndbox')
            xmin = SubElement(bndbox, 'xmin')
            xmin.text = str(each_object['xmin'])
            ymin = SubElement(bndbox, 'ymin')
            ymin.text = str(each_object['ymin'])
            xmax = SubElement(bndbox, 'xmax')
            xmax.text = str(each_object['xmax'])
            ymax = SubElement(bndbox, 'ymax')
            ymax.text = str(each_object['ymax'])

    def save(self, name,targetFile=None):
        '''
        以美观输出的xml格式来保存xml文件
        params:
          targetFile -- 存储的xml文件名，不包括.xml部分
        '''
        root = self.genXML()
        self.appendObjects(root)
        out_file = None
        subdir = self.foldername.split('/')[-1]
        if not os.path.isdir(subdir):
            os.mkdir(subdir)
        if targetFile is None:
            temp=gl.get_value(name)+1
            gl.set_value(name,temp)
            # 这里复制黏贴图片
            stra = "./bdd100k/images/100k/train/" + self.filename + ".jpg"
            des = "./bdd100k/Annotations/images/" + name +"_"+str(gl.get_value(name))+"_train" + ".jpg"
            copyfile(stra, des)
            with open(self.foldername+'/'+name +"_"+str(gl.get_value(name))+"_train"+ '.xml', 'w') as out_file:
                prettifyResult = self.prettify(root)
                out_file.write(prettifyResult)
                out_file.close()
        else:
            with open(targetFile, 'w') as out_file:
                prettifyResult = self.prettify(root)
                out_file.write(prettifyResult)
                out_file.close()

        
        


class PascalVocReader:

    def __init__(self, filepath):
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color]
        self.shapes = []
        self.filepath = filepath
        self.parseXML()

    def getShapes(self):
        return self.shapes

    def addShape(self, label, bndbox):
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        points = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        self.shapes.append((label, points, None, None))

    def parseXML(self):
        assert self.filepath.endswith('.xml'), "Unsupport file format"
        parser = etree.XMLParser(encoding='utf-8')
        xmltree = ElementTree.parse(self.filepath, parser=parser).getroot()
        filename = xmltree.find('filename').text

        for object_iter in xmltree.findall('object'):
            bndbox = object_iter.find("bndbox")
            label = object_iter.find('name').text
            self.addShape(label, bndbox)
        return True


# tempParseReader = PascalVocReader('test.xml')
# print tempParseReader.getShapes()
#"""
# Test
#tmp = PascalVocWriter('temp','test', (10,20,3))
#tmp.addBndBox(10,10,20,30,'chair')
#tmp.addBndBox(1,1,600,600,'car')
#tmp.save()
#"""

