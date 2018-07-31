# coding=utf-8
from PIL import Image  
from PIL import ImageDraw
import shutil  
import os    
import sys
import subprocess
import time
import datetime
from PIL import ImageFont


if sys.version_info < (3, 0):
    import ConfigParser 
else:
    import configparser


class Graphics:  
    infile = 'D:\\myimg.jpg'  
    outfile = 'D:\\adjust_img.jpg'  
    
    @classmethod  
    def fixed_size(cls, filename,ex_type, suffix,width, height):  
        """按照固定尺寸处理图片"""  
        cls.infile = filename
        cls.outfile = filename.split(ex_type)[0]+suffix
        im = Image.open(cls.infile)  
        out = im.resize((width, height),Image.ANTIALIAS)  
        out.save(cls.outfile)  
    
    @classmethod  
    def resize_by_width(cls, filename,ex_type, suffix,w_divide_h):  
        """高度不变，按照宽度进行所需比例缩放"""  
        cls.infile = filename
        cls.outfile = filename.split(ex_type)[0]+suffix
        im = Image.open(cls.infile)  
        (x, y) = im.size   
        x_s = x  
        y_s = x/w_divide_h  
        out = im.resize((x_s, y_s), Image.ANTIALIAS)   
        out.save(cls.outfile)  

    @classmethod  
    def draw_scale(cls,outfile,infile,param=[[400,500,150,350,450,[[225,48]]],16,1440,3120],pic_data=(128,128,128),pic_mode='RGB',isFont=True,customer=[]):

        w,h=param[2],param[3]

        #build the draw list. Ex: 40*40/5 grayscle,and from 16 to 20, step is 4, 
        #the coordinate of list is[[(0,0),(39,0),8,16],[(0,8),(39,8),8,20],[(0,16),(39,16),8,24],[(0,24),(39,24),8,28],[(0,32),(39,32),8,32]]
        newIm = Image.new(pic_mode, (w, h), pic_data)  
        drawIm=ImageDraw.Draw(newIm)
        draw_list=[]
        draw_line=[]
        Scale_100=0
        Scale_10=0
        j=0

        for i in range(99,w,100):
            draw_line.append((i,param[0][2]+param[0][0]))
            draw_line.append((i,param[0][1]+param[0][0]))
            draw_list.append(draw_line)
            draw_line=[]
            j+=1
        Scale_100=j

        for i in range(9,w,10):
            if (i+1)% 100== 0:
                continue

            draw_line.append((i,param[0][3]+param[0][0]))
            draw_line.append((i,param[0][1]+param[0][0]))
            draw_list.append(draw_line)
            draw_line=[]
            j+=1

        Scale_10=j-Scale_100

        for i in range(1,w,2):
            draw_line.append((i,param[0][4]-((i-1)%10)*30+param[0][0]))
            draw_line.append((i,param[0][1]-((i-1)%10)*30+param[0][0]))
            draw_list.append(draw_line)
            draw_line=[]
            j+=1


        for i in range(len(draw_list)):
            drawIm.line((draw_list[i][0],draw_list[i][1]),fill=param[1])

        for j in range(len(param[0][5])):
            drawIm.line(((param[0][5][j][0],0),(param[0][5][j][0],h-1)),fill=(param[0][5][j][1],param[0][5][j][1],param[0][5][j][1]))

        ttFont = ImageFont.truetype("C:\\WINDOWS\\Fonts\\simsun.ttc", param[1]+param[1]/2 )
        for i in range(Scale_100):
            drawIm.text((draw_list[i][0]),str(i+1),(255,0,0),font=ttFont)

        ttFont = ImageFont.truetype("C:\\WINDOWS\\Fonts\\simsun.ttc", param[1]-param[1]/4 )
        for i in range(Scale_10):
            drawIm.text((draw_list[i+Scale_100][0]),str(i%9+1),(255,0,0), font=ttFont)

        newIm.save(outfile)
              
    @classmethod
    def img_file_join(cls, path, unit_size, unit_num, w, h):

        images = [] # 先存储所有的图像的名称
        for root, dirs, files in os.walk(path):     
            for f in files :
                images.append(f)
        total_unit=len(images)/int(unit_num)

        if not os.path.exists(path+'/result/'): 
            os.makedirs(path+'/result/') 

        for i in range(int(total_unit)): # unit_num 个图像为一组
            imagefile = []
            j = 0

            for j in range(unit_num):
                imagefile.append(Image.open(path+'/'+images[i*unit_num+j])) 
            target = Image.new('RGB', (w, h))    
            left = 0
            right = unit_size

            for image in imagefile:     
                target.paste(image, (left, 0, right, h))# 将image复制到target的指定位置中
                left += unit_size # left是左上角的横坐标，依次递增
                right += unit_size # right是右下的横坐标，依次递增
            quality_value = 100 # quality来指定生成图片的质量，范围是0～100

            target.save(path+'/result/'+os.path.splitext(images[i*unit_size+j])[0]+'.bmp', quality = quality_value)
            imagefile = []      

    @classmethod  
    def splitimage(cls, src, rownum, colnum, limit_w=0,limit_h=0,dstpath=""):
        img = Image.open(src)
        w, h = img.size

        if (limit_h!=0 and rownum*limit_h != h) or (limit_w!=0 and colnum*limit_w !=w):
            print('Original image info: %sx%s, %s, %s' % (w, h, img.format, img.mode))
            print('size is not match')
            return False

        if rownum <= h and colnum <= w:
            print('Original image info: %sx%s, %s, %s' % (w, h, img.format, img.mode))
            print('开始处理图片切割, 请稍候...')

        s = os.path.split(src)
        if dstpath == '':
            dstpath = s[0]
            fn = s[1].split('.')
            basename = fn[0]
            ext = fn[-1]

            num = 0
            rowheight = h // rownum
            colwidth = w // colnum
            for r in range(rownum):
                for c in range(colnum):
                    box = (c * colwidth, r * rowheight, (c + 1) * colwidth, (r + 1) * rowheight)
                    img.crop(box).save(os.path.join(dstpath, basename + '_' + str(num) + '.' + ext), ext)
                    num = num + 1

            print('图片切割完毕，共生成 %s 张小图片。' % num)
            return True
        else:
            print('不合法的行列切割参数！')
            return False

    @classmethod  
    def draw_gradual(cls,outfile,param=[8,[256,1,0,255],0,1,1440,3120],pic_mode="RGB",pic_data=(0,0,0),isFont=True,customer=[]):

        w,h=param[4],param[5]
        step=param[1][1]                
        start_g=param[1][2]
        end_g=step*int(param[1][3]/step)                
        gray_num=(end_g-start_g)/step+1
        seg_len=int(h/gray_num)
        last=h%gray_num #we hope last=0, but we should consider it's not 0,leave grayscale

        if gray_num*step > param[1][0] or end_g > param[1][0]:
            print('\nError:can\'t draw this gray scale grandual.\n')

        #build the draw list. Ex: 40*40/5 grayscle,and from 16 to 20, step is 4, 
        #the coordinate of list is[[(0,0),(39,0),8,16],[(0,8),(39,8),8,20],[(0,16),(39,16),8,24],[(0,24),(39,24),8,28],[(0,32),(39,32),8,32]]
        newIm = Image.new(pic_mode, (w, h), pic_data)  
        drawIm=ImageDraw.Draw(newIm)
        draw_list=[]
        draw_line=[]
        j=0
        if param[3] == 0: #Leave gray same to last grayscale
            for i in range(start_g,eng_g+1,step):
                draw_line.append((0,seg_len*j))
                draw_line.append((w-1,seg_len*j))
                draw_line.append([seg_len,i])
                draw_list.append(draw_line)
                draw_line=[]
                j+=1
            if last:
                draw_line.append((0,seg_len*j))
                draw_line.append((w-1,seg_len*j))
                draw_line.append([last,i])
                draw_list.append(draw_line)
        elif param[3] == 1: #leave gray divide to very grayscle averagely
            for i in range(start_g,end_g+1-last*step,step):
                draw_line.append((0,seg_len*j))
                draw_line.append((w-1,seg_len*j))
                draw_line.append([seg_len,i])
                draw_list.append(draw_line)
                draw_line=[]
                j+=1
            start_2nd=seg_len*j
            seg_len+=1
            j=0
            for i in range(end_g+step-last*step,end_g+1,step):     
                draw_line.append((0,start_2nd+seg_len*j))
                draw_line.append((w-1,start_2nd+seg_len*j))
                draw_line.append([seg_len,i])
                draw_list.append(draw_line)
                draw_line=[]
                j+=1

        FontSize = draw_list[0][2][0]
        if FontSize<12:
            FontSize = 20
        elif FontSize>32:
            FontSize = 32

        ttFont = ImageFont.truetype("C:\\WINDOWS\\Fonts\\simsun.ttc", FontSize )
        for i in range(len(draw_list)):
            for j in range(draw_list[i][2][0]):
                drawIm.line(((draw_list[i][0][0],draw_list[i][0][1]+j),(draw_list[i][1][0],draw_list[i][1][1]+j)),(draw_list[i][2][1],draw_list[i][2][1],draw_list[i][2][1]))
            
            if FontSize >= 12 and isFont:
                drawIm.text((draw_list[i][0][0]+(i%2)*200,draw_list[i][0][1]),"gray_"+str(draw_list[i][2][1]),(255,0,0),font=ttFont)
            else:
                print('\nMessage:Font is samll or disable Font.\n')

        newIm.save(outfile)
        
    @classmethod  
    def draw_pic(cls,filename, outfile,w,h,op_mode,sub_op_mode,param=[8,[256,1,0,255],0,1],pic_mode="RGB",pic_data=(0,0,0)):
        cls.infile = filename
        cls.outfile = outfile
        #im = Image.open(cls.infile) 
        #param[bitmode,grayscale_number[256,step,start,end],RGB_Mode/RGB,R00,RG0,R0B,0G0,0GB,00B/,op for leave line]
        newIm = Image.new(pic_mode, (w, h), pic_data)  
        if op_mode == "grayscale":
            if sub_op_mode == "gradual":
                drawIm=ImageDraw.Draw(newIm)

                step=param[1][1]                
                start_g=param[1][2]
                end_g=step*int(param[1][3]/step)                
                gray_num=(end_g-start_g)/step+1
                seg_len=int(h/gray_num)
                last=h%gray_num #we hope last=0, but we should consider it's not 0,leave grayscale

                if gray_num*step > param[1][0] or end_g > param[1][0]:
                    print('\nError:can\'t draw this gray scale grandual.\n')


                if param[3] == 0: #Leave gray same to last grayscale
                    for i in range(start_g,eng_g+1,step):
                        for j in range(seg_len):
                            if param[2]==0: #RGB, what's fill data
                                drawIm.line(((0,(i-start_g)*seg_len+j),(w-1,(i-start_g)*seg_len+j)),(i,i,i))
                        drawIm.text((0,(i-start_g)*seg_len),"gray_"+str(i),(255,0,0))

                    if last:
                        for j in range(last):
                            if param[2]==0: #RGB
                                drawIm.line(((0,(i-start_g)*seg_len+j),(w-1,(i-start_g)*seg_len+j)),(0,0,0))

                elif param[3] == 1: #leave gray divide to very grayscle averagely
                    for i in range(start_g,end_g+1-last*step,step):
                        for j in range(seg_len):
                            if param[2]==0: #RGB
                                drawIm.line(((0,(i-start_g)*seg_len/step+j),(w-1,(i-start_g)*seg_len/step+j)),(i,i,i))

                        if i/step%2 !=1 :
                            drawIm.text((0+(i/step%4)*200,(i-start_g)*seg_len/step),"gray_"+str(i),(255,0,0),font=ttFont)

                    start_i=gray_num-last
                    start_y=seg_len*start_i              
                    seg_len+=1   
                    for i in range(end_g-last*step+step,end_g+1,step):  
                        for j in range(seg_len):
                            if param[2]==0: #RGB
                                drawIm.line(((0,(i-(end_g-last*step+step))*seg_len/step+j+start_y),(w-1,((i-(end_g-last*step+step))*seg_len/step+j+start_y))),(i,i,i))
                        if i/step%2 !=1:                        
                            drawIm.text((0+(i/step%4)*200,(i-(end_g-last*step+step))*seg_len/step+start_y),"gray_"+str(i),(255,0,0),font=ttFont)
                         
                newIm.save(outfile)


    @classmethod  
    def resize_by_height(cls,filename, outfile,w,h):  
        """宽度不变，按照高度进行所需比例缩放"""  
        cls.infile = filename
        cls.outfile = outfile
        im = Image.open(cls.infile)  
        (x, y) = im.size   
        if x>y:
            out=im.transpose(Image.ROTATE_90)
            out.save(cls.outfile)
            im = Image.open(cls.outfile) 
            out = im.resize((y, h), Image.ANTIALIAS)   
        else:
            out = im.resize((x, h), Image.ANTIALIAS)   

        out.save(cls.outfile)  
    
    @classmethod  
    def resize_by_size(cls, filename,ex_type, suffix, size):  
        """按照生成图片文件大小进行处理(单位KB)"""  
        cls.infile = filename
        cls.outfile = filename.split(ex_type)[0]+suffix
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
    def cut_by_ratio(cls,filename, ex_type, suffix, width, height):  
        """按照图片长宽比进行分割"""  
        cls.infile = filename
        cls.outfile = filename.split(ex_type)[0]+ suffix
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
'''
<How to use>

1.	Write PPM PATH to test_list.txt
2.	Check & Edit config.ini
3.	Run dsc11_enc_wqhd.exe
4.	Extract PPS information

1.	Write PPM PATH to test_list.txt
This tool only read PPM image. So, please prepare the PPM file.
If you have only BMP file, you can convert BMP to PPM using convert.exe in bin folder.
<Example>
convert.exe –depth 8 in.bmp out.ppm

2.	Check & Edit config.ini
MODE
•	10bit 1/3 : 10bpc10bpp
•	10bit 1/3.75: 10bpc8bpp
•	8bit 1/3: 8bpc8bpp
        PICT_HEIGHT
               3120 fixed
        SLICE_WIDTH
                 720 fixed
        SLICE_HEIGHT
                 I recommend 30
        BLOCK_PRED_ENABLE
                 I recommend 1

3.	Run dsc11_enc_wqhd.exe
Some outputs will be generated.
*_dsc.bmp: compressed bmp. 
*.dsc: this file is used at next step. (input of extract_pps_gui.exe)

4.	Extract PPS information
Run extract_pps_gui.exe
And Drag & Drop *.dsc file to window. after that *_pps.txt file will be generated. 
Please write PPS information to register.

    if os.path.exists('./ks_accumulate.csv'):
        if os.path.getsize('./ks_accumulate.csv'):
            print('文件存在且不为空')
            ks_temp.to_csv('./ks_accumulate.csv', mode='a', header=False, index=False)
        else:
            print('文件存在且为空')
            ks_temp.to_csv('./ks_accumulate.csv', mode='a', index=False)
    else:
        print('文件不存在')
        ks_temp.to_csv('./ks_accumulate.csv', mode='a', index=False)
'''    
def image_operation( inifile='',bypass=''): 
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
    FILE_TYPE=ReadIni(IniPath,PyName,'FILE_TYPE')
    DSC_TOOL_Path=ReadIni(IniPath,PyName,'DSC_TOOL_Path')
    TOOL_CONVERT=DSC_TOOL_Path+"/"+ReadIni(IniPath,PyName,'TOOL_CONVERT')
    TOOL_DSC=DSC_TOOL_Path+"/"+ReadIni(IniPath,PyName,'TOOL_DSC')
    TOOL_PPS=DSC_TOOL_Path+"/"+ReadIni(IniPath,PyName,'TOOL_PPS')
    LIST_FILE=DSC_TOOL_Path+"/"+ReadIni(IniPath,PyName,'LIST_FILE')
    MID_FILE_FORMAT=ReadIni(IniPath,PyName,"MID_FILE_FORMAT")
    SUFFIX=ReadIni(IniPath,PyName,"SUFFIX")
    IMG_HEGHT=ReadIni(IniPath,PyName,"IMG_HEGHT")
    IMG_WIDTH=ReadIni(IniPath,PyName,"IMG_WIDTH")
    CONVERT_PARAM=ReadIni(IniPath,PyName,"CONVERT_PARAM")
    IS_SPLIT=ReadIni(IniPath,PyName,"IS_SPLIT")
    SPLIT_COL=ReadIni(IniPath,PyName,"SPLIT_COL")
    SPLIT_ROW=ReadIni(IniPath,PyName,"SPLIT_ROW")
    SPLIT_FILE_WITH=ReadIni(IniPath,PyName,"SPLIT_FILE_WITH")
    SPLIT_FILE_HEIGHT=ReadIni(IniPath,PyName,"SPLIT_FILE_HEIGHT")
    #如果目的文件夹不存在，创建之 
    if not os.path.exists(DescPath): 
        os.makedirs(DescPath) 

    FileList=[] 
    FileListDSC=[]
    FileListMID=[]
    if op_type == "dir":  
        for root, dirs, files in os.walk(SrcPath): 
            for FileName in files: 
                if FileName.split('.')[-1] == FILE_TYPE: 
                    fileout=FileName #DescPath+"\\"+
                    FileName = SrcPath+"\\"+FileName
                    pos = FileName.find(SUFFIX)
                    if pos != -1 :
                        continue

                    FileList.append(FileName) 
                    newfile=fileout.split("."+FILE_TYPE)[0]+SUFFIX
                    FileListDSC.append(DescPath+"/"+newfile.split("."+FILE_TYPE)[0]+"."+MID_FILE_FORMAT)
            break
    elif op_type == "file":
        FileList.append(SrcPath)

    with open(LIST_FILE,"w") as file_to_write: #write file list for dsc
        for file in FileListDSC:
            file_to_write.writelines(file) 
            file_to_write.writelines("\n")
    file_to_write.close()

    for file in FileList: #
        if bypass=='yes':
            newfile=file.split("."+FILE_TYPE)[0]+SUFFIX
            FileListMID.append(newfile)
            if os.path.exists(newfile):
                continue
            Graphics.resize_by_height(file,newfile, int(IMG_WIDTH),int(IMG_HEGHT))
        elif bypass=='no' or bypass=='':
            FileListMID.append(file)

    for i in range(len(FileListMID)):
        file=FileListMID[i]
        dscfile=FileListDSC[i]
        program=TOOL_CONVERT+" "+ CONVERT_PARAM+" "+file+" "+dscfile
        if os.path.exists(dscfile):
            continue
        #os.popen(program)
        sub=subprocess.Popen(program,shell=True,stdout=subprocess.PIPE,cwd=DSC_TOOL_Path)
        time.sleep(5)
        sub.wait()
        #print(sub.read())  

    #os.poepn(TOOL_DSC)
    sub=subprocess.Popen(TOOL_DSC,shell=True,stdout=subprocess.PIPE,cwd=DSC_TOOL_Path)
    sub.wait()

    sub=subprocess.Popen("copy ./*.dsc " + DescPath,shell=True,stdout=subprocess.PIPE,cwd=DSC_TOOL_Path)
    sub.wait()

    sub=subprocess.Popen(TOOL_PPS+" "+FileListDSC[0].split(".ppm")[0]+".dsc",shell=True,stdout=subprocess.PIPE,cwd=DescPath)
    sub.wait()

if __name__ == '__main__':
    argv_num=len(sys.argv)

    if argv_num == 2:
        if sys.argv[1] == "DSC":
            image_operation()
        else:
            print("Don't support this command!\n")  
    elif argv_num >2:
        if sys.argv[1] == "SPLIT":
            #Graphics.splitimage("1.bmp",1,2,1080,2480)
            Graphics.splitimage(sys.argv[2], int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]))
        elif sys.argv[1] == "JOIN":
            #Graphics.img_file_join("D:\\tony\\tools\\pytools\\syna\\DSC\\join", 1080,2,2160,2480 )
            Graphics.img_file_join(sys.argv[2], int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]) )
        elif sys.argv[1] == "JOIN":
            #Graphics.img_file_join("D:\\tony\\tools\\pytools\\syna\\DSC\\join", 1080,2,2160,2480 )
            Graphics.img_file_join(sys.argv[2], int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]) )
        else:
            print("Don't support this command!\n")  
    else:
        print("Import parameter is error!")    

    #draw_pic(cls,filename, outfile,w,h,op_mode,sub_op_mode,param=[8,256,"RGB"],pic_mode="RGB",pic_data=(0,0,0)): 
    #Graphics.draw_pic("","red.bmp",1440,3120,"grayscale","gradual",[8,[256,1,0,255],0,1])
    #Graphics.draw_gradual("red.bmp",[0,1,1440,3120])
    #Graphics.draw_scale("scale_1440_3_darker_line_S-13-1.bmp","",[[1400,500,150,350,450,[[1305,128],[440,128],[1315,128],[450,128]]],20,1440,3120],(32,32,32))
    #Graphics.draw_scale("scale_1440_normal_00.bmp","",[[1400,500,150,200,440,[]],20,1440,3120],(00,00,00))
