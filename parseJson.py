#!/usr/bin/env python
# -*- coding: utf8 -*-
#parse json，input json filename,output info needed by voc

import json
#这里是我需要的10个类别
categorys = ['car', 'bus', 'person',  'truck', 'motor',  'traffic light']#motor--->moto,traffic light--->light

def parseJson(jsonFile):
    '''
      params:
        jsonFile -- BDD00K数据集的一个json标签文件
      return:
        返回一个列表的列表，存储了一个json文件里面的方框坐标及其所属的类，
        形如：[[325, 342, 376, 384, 'car'], [245, 333, 336, 389, 'car']]
    '''
    objs = []
    obj = []
    f = open(jsonFile)
    info = json.load(f)
    objects = info['frames'][0]['objects']
    for i in objects:
        if(i['category'] in categorys):
            obj.append(int(i['box2d']['x1']))
            obj.append(int(i['box2d']['y1']))
            obj.append(int(i['box2d']['x2']))
            obj.append(int(i['box2d']['y2']))
            #这个地方改一下名字
            strt=i['category']
            if strt=="traffic light":
                strt="light"
            if strt == "motor":
                strt = "moto"
            obj.append(strt)
            objs.append(obj)
            obj = []
    #print("objs",objs)
    return objs

#test
#result = parseJson("/media/xavier/SSD256/global_datasets/BDD00K/bdd100k/labels/100k/val/b1c9c847-3bda4659.json")
#print(len(result))
#print(result)

