# coding=utf-8
from PIL import Image  
import shutil  
import os    
import sys

if sys.version_info < (3, 0):
    import ConfigParser 
else:
    import configparser

class Graphics:  
    infile = 'D:\\myimg.jpg'  
    outfile = 'D:\\adjust_img.jpg'  
    
    @classmethod  
    def fixed_size(cls, filename,width, height):  
        """按照固定尺寸处理图片"""  
        im = Image.open(cls.infile)  
        out = im.resize((width, height),Image.ANTIALIAS)  
        out.save(cls.outfile)  
    
    @classmethod  
    def resize_by_width(cls, filename,w_divide_h):  
        """按照宽度进行所需比例缩放"""  
        im = Image.open(cls.infile)  
        (x, y) = im.size   
        x_s = x  
        y_s = x/w_divide_h  
        out = im.resize((x_s, y_s), Image.ANTIALIAS)   
        out.save(cls.outfile)  
    
    @classmethod  
    def resize_by_height(cls,filename, w_divide_h):  
        """按照高度进行所需比例缩放"""  
        im = Image.open(cls.infile)  
        (x, y) = im.size   
        x_s = y*w_divide_h  
        y_s = y  
        out = im.resize((x_s, y_s), Image.ANTIALIAS)   
        out.save(cls.outfile)  
    
    @classmethod  
    def resize_by_size(cls, filename,size):  
        """按照生成图片文件大小进行处理(单位KB)"""  
        size *= 1024  
        im = Image.open(cls.infile)  
        size_tmp = os.path.getsize(cls.infile)  
        q = 100  
        while size_tmp > size and q > 0:  
            print(q)  
            out = im.resize(im.size, Image.ANTIALIAS)  
            out.save(cls.outfile, quality=q)  
            size_tmp = os.path.getsize(cls.outfile)  
            q -= 5  
        if q == 100:  
            shutil.copy(cls.infile, cls.outfile)  
    
    @classmethod  
    def cut_by_ratio(cls,filename, width, height):  
        """按照图片长宽比进行分割"""  
        im = Image.open(cls.infile)  
        width = float(width)  
        height = float(height)  
        (x, y) = im.size  
        if width > height:  
            region = (0, int((y-(y * (height / width)))/2), x, int((y+(y * (height / width)))/2))  
        elif width < height:  
            region = (int((x-(x * (width / height)))/2), 0, int((x+(x * (width / height)))/2), y)  
        else:  
            region = (0, 0, x, y)  
    
        #裁切图片  
        crop_img = im.crop(region)  
        #保存裁切后的图片  
        crop_img.save(cls.outfile)  
def ReadIni(path,section,option):#文件路径，章节，关键词 
    #读取ini
    if sys.version_info < (3, 0):
        cf=ConfigParser.ConfigParser() 
    else:  
        cf=configparser.ConfigParser()  
        
    cf.read(path) 
    value=cf.get(section,option)#如果用getint()则直接读取该数据类型为整数 


    return value 
def image_operation( inifile=''): 
    #从ini获取源文件夹及目标文件夹路径 
    CMD_num=0
    CMD_type_num=0
    CMD_list=[]
    CMD_param=[]
    CMD_name=[]
    CMD_type=[]
    PyName="image_config"
    if inifile=='':
        IniPath=os.getcwd()+'//'+PyName+'.ini'
    else:    
        IniPath = inifile

    SrcPath=ReadIni(IniPath,PyName,'SrcPath')#源文件夹 
    DescPath=ReadIni(IniPath,PyName,'DescPath')#目的文件夹
    op_type =ReadIni(IniPath,PyName,'OP_TYPE')#Operation type 
    CMD_num=int(ReadIni(IniPath,PyName,'TEST_CMD'))
    CMD_type_num = int(ReadIni(IniPath,PyName,'TEST_CMD_TYPE'))

    for i in range(CMD_num):
        CMD_list.append(ReadIni(IniPath,PyName,'TEST_CMD'+str(i)))
        CMD_param.append(ReadIni(IniPath,PyName,'TEST_CMD_PARAM'+str(i)))

    for i in range(CMD_type_num):
        CMD_type.append(ReadIni(IniPath,PyName,'TEST_CMD_NAME'+str(i)))

    #如果目的文件夹不存在，创建之 
    if not os.path.exists(DescPath): 
        os.makedirs(DescPath) 

    FileList=[] 
    if op_type == "dir":  
        for files in os.walk(SrcPath): 
            for FileName in files[2]: 
                if FileName.split('.')[-1]=='txt': 
                    FileName = SrcPath+"\\"+FileName
                    FileList.append(FileName) 

    elif op_type == "file":
        FileList.append(SrcPath)

    for file in FileList:
        Graphics.resize_by_height(file, 1440)

if __name__ == '__main__':
    image_operation()