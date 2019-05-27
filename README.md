# bdd100ktoxml
bdd100k数据集转xml
选了一门机器学习课，要求每个人标注300张，7大类图片。大概算了一下，找图片，搜索保存改名字，10秒一张，标注7个类至少3分钟一张，一共16小时左右。艹，突然想到这种东西肯定有现成的数据集吧，找到了bdd100k,分为10各类，可以覆盖7个中的6个，还有一个三轮车手动一下好了。这套代码包含json解析，xml生成，全局变量上的重命名等，做个备份。
参考https://blog.csdn.net/qq583083658/article/details/86496563这位老哥，谢谢老哥！！！！

主要修改了如下功能：

1.根据需要的类型挑选出需要的图片，并转换对应xml

2.找到对应的图片，把图片复制出来

3.改名字，这里添加了一个blobalvar.py用于记录跨包的全局变量

BDD00K所有图片的下载地址：
https://archive.org/download/bdd100k/bdd100k_labels.zip

BDD00K所有图片标签的下载地址：
https://archive.org/download/bdd100k/bdd100k_images.zip
