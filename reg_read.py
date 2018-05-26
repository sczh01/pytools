# coding=utf-8
import os,sys;
import re
import xlrd
import os 
import sys
import ConfigParser 

cmd_7422 = []
cmd_gx_str = []
cmd_gx_cmd=[]
#line_type = [] 
#line_data = []
line_pos = 0
line_use =""

class test_config(object):
    RX_NUM=0
    TX_NUM=0
    START_line=0
    cmd_num=0
    test_cmd = []
    test_dir=""
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.hobbies = ["table tenis"]
    pass

def BOE_to_other( filelist, file_our_src='',out_type=''):
    cmd_num = 0
    for filename in filelist:
        cmd_gx_str=[]
        with open(filename, 'r') as file_to_read:
            while True:
                lines = file_to_read.readline() # 整行读取数据
                if not lines:
                    break
                    pass
                lines=lines.strip()
                if lines =='':
                    continue
                if lines[0]=='#':
                    continue
                #if IsPassLine( lines ) == False:
                    continue
                if lines[0]=='/' and lines[1]=='/':
                    continue
                line_pos = lines.find("REGS.WRITE(0,")

                if line_pos == -1:
                    continue
                line_use = lines[line_pos+13:]
                line_pos = line_use.find(")")
                line_use = line_use[:line_pos]
                line_data=line_use.split(',')
                line_use = line_use.replace(',',' ')

                line_mipi_data_gx_str="mipi.write "+ line_use+'\n'
                cmd_gx_str.append(line_mipi_data_gx_str)   
                cmd_num +=1
            pass

        file_to_read.close()
        with open(file_our_src+"/"+filename.split("/")[-1].split("txt")[-2]+"_Elecs.txt","w") as file_to_write:
            file_to_write.writelines(cmd_gx_str) 
        file_to_write.close()


    return "success"

def gx_to_other( filename, out_type):
    cmd_num = 0
    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
                break
                pass
            lines=lines.strip()
            if lines =='':
                continue
            if lines[0]=='#':
                continue
            #if IsPassLine( lines ) == False:
                continue
            if lines[0]=='/' and lines[1]=='/':
                continue
            line_pos = lines.find("U16")
            if line_pos == -1:
                line_pos = lines.find("u16")  

            if line_pos != -1:
                line_pos=lines.find("]={")
                line_use = lines[line_pos+3:]
            else:
                continue
            line_use=line_use.strip()
            line_pos = line_use.find("}")
            line_use = line_use[:line_pos]
            line_data=line_use.split(',')
            line_use = line_use.replace(',',' ')

            line_mipi_data_gx_str="mipi.write 0x29 "+ line_use+'\n'
            cmd_gx_str.append(line_mipi_data_gx_str)   
            cmd_num +=1
        pass

    file_to_read.close()
    with open(filename+"_E7422.txt","w") as file_to_write:
        file_to_write.writelines(cmd_gx_str) 
    file_to_write.close()
    return "success"
    
def excel_to_jig( filename, out_type ):
    XL_row_start=7
    XL_col_start=5
    XL_con_code=[6,7,8,10]
    cmd_xl_str_1 = []
    cmd_xl_str_2 = []
    cmd_xl_str_3 = []
    cmd_xl_cmd_1 = []
    cmd_xl_cmd_2 = []
    cmd_xl_cmd_3 = []
    data = xlrd.open_workbook(filename)
    table = data.sheets()[3]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    cmd_xl_1 = ''
    cmd_xl_2 = ''
    cmd_xl_3 = ''
    code_type_1 = 'TD4310 default mode'
    code_type_2 = 'TD4310 Split 4p(8p) non-OverLap mode'
    code_type_3 = 'TD4310 Split 4p(8p) OverLap mode'
    for i in xrange(XL_row_start,nrows):
        rowValues= table.row_values(i) #某一行数据
        #for j in XL_con_code:
        #    print rowValues[j]
        if rowValues[XL_con_code[0]] == "CMD":
            if i > XL_row_start:
                if out_type == "GX":
                    cmd_xl_str_1.append("U16 "+cmd_str_1[2:]+'['+str(param_num)+']={'+cmd_xl_1+'}\n')
                    cmd_xl_str_2.append("U16 "+cmd_str_2[2:]+'['+str(param_num)+']={'+cmd_xl_2+'}\n')
                    cmd_xl_str_3.append("U16 "+cmd_str_3[2:]+'['+str(param_num)+']={'+cmd_xl_3+'}\n')
                    cmd_xl_cmd_1.append("Generic_Long_Write_FIFO("+str(param_num)+','+cmd_str_1[2:]+');\n')
                    cmd_xl_cmd_2.append("Generic_Long_Write_FIFO("+str(param_num)+','+cmd_str_2[2:]+');\n')
                    cmd_xl_cmd_3.append("Generic_Long_Write_FIFO("+str(param_num)+','+cmd_str_3[2:]+');\n')
                elif out_type == "E7422":
                    cmd_xl_str_1.append("mipi.write 0x29 "+cmd_xl_1+'\n')
                    cmd_xl_str_2.append("mipi.write 0x29 "+cmd_xl_2+'\n')
                    cmd_xl_str_3.append("mipi.write 0x29 "+cmd_xl_3+'\n')
        
            cmd_str_1=cmd_xl_1="0x"+ rowValues[XL_con_code[1]][3:]
            cmd_str_2=cmd_xl_2="0x"+ rowValues[XL_con_code[2]][3:]
            cmd_str_3=cmd_xl_3="0x"+ rowValues[XL_con_code[3]][3:]
            param_num = 1
        else:
            param_num +=1
            if out_type == "GX":
                cmd_xl_1+=",0x"+ rowValues[XL_con_code[1]][3:]
                cmd_xl_2+=",0x"+ rowValues[XL_con_code[2]][3:]
                cmd_xl_3+=",0x"+ rowValues[XL_con_code[3]][3:]
            elif out_type == "E7422":
                cmd_xl_1+=" 0x"+ rowValues[XL_con_code[1]][3:]
                cmd_xl_2+=" 0x"+ rowValues[XL_con_code[2]][3:]
                cmd_xl_3+=" 0x"+ rowValues[XL_con_code[3]][3:]

    if out_type == "GX":
        filename+=".GX.txt"
    elif out_type == 'E7422':
        filename+=".E7422.txt"

    with open(filename,"w") as file_to_write:
        if out_type == "GX":
            file_to_write.writelines("\n"+code_type_1+ "--------\n\n")
            file_to_write.writelines(cmd_xl_str_1) 
            file_to_write.writelines(cmd_xl_cmd_1)
            file_to_write.writelines("\n"+code_type_2+ "--------\n\n")
            file_to_write.writelines(cmd_xl_str_2)
            file_to_write.writelines(cmd_xl_cmd_2) 
            file_to_write.writelines("\n"+code_type_3+ "--------\n\n")
            file_to_write.writelines(cmd_xl_str_3) 
            file_to_write.writelines(cmd_xl_cmd_3)    
        elif out_type == "E7422":    
            file_to_write.writelines("\n"+code_type_1+ "--------\n\n")
            file_to_write.writelines(cmd_xl_str_1) 
            file_to_write.writelines("\n"+code_type_2+ "--------\n\n")
            file_to_write.writelines(cmd_xl_str_2)
            file_to_write.writelines("\n"+code_type_3+ "--------\n\n") 
            file_to_write.writelines(cmd_xl_str_3) 
                
    file_to_write.close()
    return "success"

def excel_to_jig_ex( filename, out_type, op_param="none" ):
    XL_row_start=13
    XL_col_start=7
    XL_con_code=[6,7,10,12]
    cmd_xl_str_1 = []
    cmd_xl_str_2 = []
    cmd_xl_str_3 = []
    cmd_xl_cmd_1 = []
    cmd_xl_cmd_2 = []
    cmd_xl_cmd_3 = []
    data = xlrd.open_workbook(filename)
    table = data.sheets()[3]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    cmd_xl_1 = ''
    cmd_xl_2 = ''
    cmd_xl_3 = ''
    code_type_1 = 'TD4130 default mode'
    code_type_2 = 'TD4130 LHB none 0C'
    code_type_3 = 'TD4130 LHB 0C'
    for i in xrange(XL_row_start,nrows):
        rowValues= table.row_values(i) #某一行数据
        #for j in XL_con_code:
        #    print rowValues[j]
        if rowValues[XL_con_code[0]] == "CMD":
            if i > XL_row_start:
                if out_type == "GX":
                    cmd_xl_str_1.append("U16 "+cmd_str_1[2:]+'['+str(param_num)+']={'+cmd_xl_1+'}\n')
                    cmd_xl_str_2.append("U16 "+cmd_str_2[2:]+'['+str(param_num)+']={'+cmd_xl_2+'}\n')
                    cmd_xl_str_3.append("U16 "+cmd_str_3[2:]+'['+str(param_num)+']={'+cmd_xl_3+'}\n')
                    cmd_xl_cmd_1.append("Generic_Long_Write_FIFO("+str(param_num)+','+cmd_str_1[2:]+');\n')
                    cmd_xl_cmd_2.append("Generic_Long_Write_FIFO("+str(param_num)+','+cmd_str_2[2:]+');\n')
                    cmd_xl_cmd_3.append("Generic_Long_Write_FIFO("+str(param_num)+','+cmd_str_3[2:]+');\n')
                elif out_type == "E7422":
                    cmd_xl_str_1.append("mipi.write 0x29 "+cmd_xl_1+'\n')
                    cmd_xl_str_2.append("mipi.write 0x29 "+cmd_xl_2+'\n')
                    cmd_xl_str_3.append("mipi.write 0x29 "+cmd_xl_3+'\n')
        
            cmd_str_1=cmd_xl_1="0x"+ rowValues[XL_con_code[1]][3:]
            if rowValues[XL_con_code[2]]== u'initial value':
                cmd_str_2=cmd_xl_2=cmd_str_1
            else:
                cmd_str_2=cmd_xl_2="0x"+ rowValues[XL_con_code[2]][3:]
            
            if rowValues[XL_con_code[3]]== "initial value":
                cmd_str3=cmd_xl_3=cmd_str_1
            else:
                cmd_str_3=cmd_xl_3="0x"+ rowValues[XL_con_code[3]][3:]

            param_num = 1
        else:
            param_num +=1
            if out_type == "GX":
                cmd_xl_1+=",0x"+ rowValues[XL_con_code[1]][3:]                
                if rowValues[XL_con_code[2]]== u'initial value':
                    cmd_xl_2+=",0x"+ rowValues[XL_con_code[1]][3:]
                else:
                    cmd_xl_2+=",0x"+ rowValues[XL_con_code[2]][3:]

                if rowValues[XL_con_code[3]]== "initial value":
                    cmd_xl_3+=",0x"+ rowValues[XL_con_code[1]][3:]
                else:
                    cmd_xl_3+=",0x"+ rowValues[XL_con_code[3]][3:]
            elif out_type == "E7422":
                cmd_xl_1+=" 0x"+ rowValues[XL_con_code[1]][3:]
                if rowValues[XL_con_code[2]]== "initial value":
                    cmd_xl_2+=" 0x"+ rowValues[XL_con_code[1]][3:]
                else:
                    cmd_xl_2+=" 0x"+ rowValues[XL_con_code[2]][3:]

                if rowValues[XL_con_code[3]]== "initial value":
                    cmd_xl_3+=" 0x"+ rowValues[XL_con_code[1]][3:]
                else:
                    cmd_xl_3+=" 0x"+ rowValues[XL_con_code[3]][3:]

                    
    if out_type == "GX":
        filename+=".GX.txt"
    elif out_type == 'E7422':
        filename+=".E7422.txt"

    with open(filename,"w") as file_to_write:
        if out_type == "GX":
            file_to_write.writelines("\n"+code_type_1+ "--------\n\n")
            file_to_write.writelines(cmd_xl_str_1) 
            file_to_write.writelines(cmd_xl_cmd_1)
            file_to_write.writelines("\n"+code_type_2+ "--------\n\n")
            file_to_write.writelines(cmd_xl_str_2)
            file_to_write.writelines(cmd_xl_cmd_2) 
            file_to_write.writelines("\n"+code_type_3+ "--------\n\n")
            file_to_write.writelines(cmd_xl_str_3) 
            file_to_write.writelines(cmd_xl_cmd_3)    
        elif out_type == "E7422":    
            file_to_write.writelines("\n"+code_type_1+ "--------\n\n")
            file_to_write.writelines(cmd_xl_str_1) 
            file_to_write.writelines("\n"+code_type_2+ "--------\n\n")
            file_to_write.writelines(cmd_xl_str_2)
            file_to_write.writelines("\n"+code_type_3+ "--------\n\n") 
            file_to_write.writelines(cmd_xl_str_3) 
                
    file_to_write.close()
    return "success"

def truly_to_gx( filename ):
    cmd_num = 0
    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
                break
                pass
            lines=lines.strip()
            if lines =='':
                continue
            if lines[0]=='#':
                continue
            line_pos = lines.find("{0x29")
            if line_pos == -1:
                line_pos = lines.find("{0X29")  

            if line_pos != -1:
                line_use = lines[len("{0X29,0,0,0,0,2")+1:]
            else:
                continue
            line_use=line_use.strip()
            line_data=line_use.split()
            #U16 B3[4]={0xB3,0x31,0x00,0x06};
            #Generic_Long_Write_FIFO(4,B3);//0xB3
            line_mipi_num = lines[len("{0X29,0,0,0,0,"):len("{0X29,0,0,0,0,")+2]
            if line_mipi_num[1]==',':
                line_mipi_num=line_mipi_num[0]
            else:
                line_use=line_use[1:]

            line_mipi_data = line_use[:len(line_use)-2] #[int(i) for i in lines.split()]
        
            cmd_7422.append(line_mipi_data)
            line_mipi_data_gx_str="U16 "+str(cmd_num)+'['+line_mipi_num+']='+line_mipi_data+';\n'
            line_mipi_data_gx_cmd_str="Generic_Long_Write_FIFO("+line_mipi_num+','+str(cmd_num)+');\n'
            cmd_gx_str.append(line_mipi_data_gx_str)   
            cmd_gx_cmd.append(line_mipi_data_gx_cmd_str)
            cmd_num +=1

        # pos.append(p_tmp)  # 添加新读取的数据
        # Efield.append(E_tmp)
        pass
    file_to_read.close()
    with open(filename+".txt","w") as file_to_write:
        file_to_write.writelines(cmd_gx_str) 
        file_to_write.writelines(cmd_gx_cmd)
    file_to_write.close()
    return "success"

def Compare_E7422( file_list, reg_name="" ):
    line_data_file={}
    file_compare={}
    different_line=[]
    #ine_data_file.fromkeys((file_list),[])
    i = 0
    for file_name in file_list:
        line_data_file[i]=[]
        line_data_file
        with open(file_name, 'r') as file_to_read:
            while True:
                CF_Count =0
                D7_Count =0
                lines = file_to_read.readline() # 整行读取数据
                if not lines:
                    break
                    pass
                lines=lines.strip()
                if lines =='':
                    continue
                if lines[0]=='#':
                    continue
                line_pos = lines.find("#")
                if line_pos != -1:
                    lines = lines[:line_pos]
                
                line_pos = lines.find("mipi.write")
                if line_pos != -1:
                    line_use = lines[len("mipi.write")+1:]
                else:
                    continue
                line_use=line_use.strip()
                line_data=line_use.split()

                line_mipi_type,line_mipi_data = line_use[:len(line_data[0])],line_use[len(line_data[0])+1:] #[int(i) for i in lines.split()]
                tmp_str=re.compile(' ')
                line_mipi_data_sub=tmp_str.sub(',',line_mipi_data)

                if line_mipi_type == "0x29" or  line_mipi_type == "0x39" or  line_mipi_type == "0x15" :
                    line_data_file[i].append(line_mipi_data)
                    continue
            pass
            file_to_read.close()
        i+=1
    i = 0
    for j in range(len(line_data_file[0])):
        if line_data_file[0][j] != line_data_file[1][j]:
            file_compare[i] = []
            file_compare[i].append(line_data_file[0][j])
            file_compare[i].append(line_data_file[1][j])
            i+=1
    #if len( line_data_file[1]) > 0
        
    return "success"

def Elecs_to( filename, out_type='' ):
    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
                break
                pass
            lines=lines.strip()
            if lines =='':
                continue
            if lines[0]=='#':
                continue
            line_pos = lines.find("#")
            if line_pos != -1:
                lines = lines[:line_pos]
            
            line_pos = lines.find("mipi.write")
            if line_pos != -1:
                line_use = lines[len("mipi.write")+1:]
            else:
                continue
            line_use=line_use.strip()
            line_data=line_use.split()
            #U16 B3[4]={0xB3,0x31,0x00,0x06};
            #Generic_Long_Write_FIFO(4,B3);//0xB3
            line_mipi_type,line_mipi_data = line_use[:len(line_data[0])],line_use[len(line_data[0])+1:] #[int(i) for i in lines.split()]
            tmp_str=re.compile(' ')
            line_mipi_data_sub=tmp_str.sub(',',line_mipi_data)

            if line_mipi_type == "0x29":
                cmd_7422.append(line_mipi_data)
                line_mipi_data_gx_str='W_COM('+line_mipi_data_sub+');\n'
                #line_mipi_data_gx_cmd_str="Generic_Long_Write_FIFO("+str(len(line_data)-1)+','+line_data[1][2:]+');\n'
                cmd_gx_str.append(line_mipi_data_gx_str)   
                #cmd_gx_cmd.append(line_mipi_data_gx_cmd_str)
        # pos.append(p_tmp)  # 添加新读取的数据
        # Efield.append(E_tmp)
        pass
    file_to_read.close()
    with open(filename+"_elecs.txt","w") as file_to_write:
        file_to_write.writelines(cmd_gx_str) 
        #file_to_write.writelines(cmd_gx_cmd)
    file_to_write.close()
    return "success"

def usage_E7422_to_BOE():
    print("\nError, no input file.\nUsage: syna2cus.exe filename\n")

def E7422_to_BOE( filename="", mode="BOE_W7", cmd_head="REGS.WRITE" ):
    if filename == '':
        usage_E7422_to_BOE()
        return "Fail"
    line_mipi_data_gx_str = ""
    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
                break
                pass
            lines=lines.strip()
            if lines =='':
                continue
            if lines[0]=='#':
                continue
            line_pos = lines.find("#")
            if line_pos != -1:
                lines = lines[:line_pos]
            
            line_pos = lines.find("mipi.write")
            if line_pos != -1:
                line_use = lines[len("mipi.write")+1:]
            else :
                line_pos = lines.find("delay")
                if line_pos != -1 :
                    if line_mipi_data_gx_str == "" or line_mipi_data_gx_str.find("REGS") == -1:
                        continue

                    line_mipi_data_gx_str='TIME.DELAY('+lines.split()[1]+')\n'
                    cmd_gx_str.append(line_mipi_data_gx_str)   
                    continue
                else:
                    continue

            line_use=line_use.strip()
            line_data=line_use.split()
            #U16 B3[4]={0xB3,0x31,0x00,0x06};
            #Generic_Long_Write_FIFO(4,B3);//0xB3
            line_mipi_type,line_mipi_data = line_use[:len(line_data[0])],line_use[len(line_data[0])+1:] #[int(i) for i in lines.split()]
            tmp_str=re.compile(' ')
            line_elecs_data_sub=tmp_str.sub(',',line_use)
            tmp_str=re.compile(' ')
            line_mipi_data_sub=tmp_str.sub(',',line_mipi_data)

            if line_mipi_type == "0x29" or line_mipi_type == "0x39" or line_mipi_type == "0x15" or line_mipi_type == "0x05":
                cmd_7422.append(line_mipi_data)
                if mode == "BOE_W7":
                    line_mipi_data_gx_str=cmd_head+'(0,'+line_elecs_data_sub+')\n'
                elif mode == "SYNA_FHD":
                    line_mipi_data_gx_str=cmd_head+'('+line_mipi_data_sub+');\n'

                #line_mipi_data_gx_cmd_str="Generic_Long_Write_FIFO("+str(len(line_data)-1)+','+line_data[1][2:]+');\n'
                cmd_gx_str.append(line_mipi_data_gx_str)   
                #cmd_gx_cmd.append(line_mipi_data_gx_cmd_str)
        # pos.append(p_tmp)  # 添加新读取的数据
        # Efield.append(E_tmp)
        pass
    file_to_read.close()
    with open(filename.split('.txt')[0]+"_Syna2"+mode+".txt","w") as file_to_write:
        file_to_write.writelines(cmd_gx_str) 
        #file_to_write.writelines(cmd_gx_cmd)
    file_to_write.close()
    return "success"

def E7422_to_gx( filename, reg_name,device="66451" ):
    with open(filename, 'r') as file_to_read:
        CF_Count =0
        D7_Count =0
        GM_66451_Count={}
        GM_66451_Count["0xC6"] =0
        GM_66451_Count["0xC7"] =0
        GM_66451_Count["0xC8"] =0
        GM_66451_Count["0xC9"] =0
        GM_66451_Count["0xCA"] =0
        GM_66451_Count["0xCB"] =0
        GM_66455_Count={}
        GM_66455_Count["0xCC"] =0
        GM_66455_Count["0xC7"] =0
        GM_66455_Count["0xC8"] =0
        GM_66455_Count["0xC9"] =0
        GM_66455_Count["0xCA"] =0
        GM_66455_Count["0xCB"] =0        
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
                break
                pass
            lines=lines.strip()
            if lines =='':
                continue
            if lines[0]=='#':
                continue
            line_pos = lines.find("#")
            if line_pos != -1:
                lines = lines[:line_pos]
            
            line_pos = lines.find("mipi.write")
            if line_pos != -1:
                line_use = lines[len("mipi.write")+1:]
            else:
                continue
            line_use=line_use.strip()
            line_data=line_use.split()

            line_mipi_type,line_mipi_data = line_use[:len(line_data[0])],line_use[len(line_data[0])+1:] #[int(i) for i in lines.split()]
            tmp_str=re.compile(' ')
            line_mipi_data_sub=tmp_str.sub(',',line_mipi_data)

            if line_mipi_type == "0x29":

                #for reg_name_str in reg_name:
                #    if line_data[1] == reg_name_str:
                #        process_analzye(filename,reg_name_str,line_data)
                if line_data[1] =="0xCF":
                    reg_process_0xCF(filename.split('.txt')[0]+str(CF_Count),line_data)
                    CF_Count += 1
                if line_data[1] =="0xD7":
                    reg_process_0xD7(filename.split('.txt')[0]+str(D7_Count),line_data)   
                    D7_Count += 1
                if line_data[1] =="0xC6":
                    if device == "66451":
                        reg_process_0xCX(filename.split('.txt')[0]+'-'+line_data[1]+'-'+str(GM_66451_Count[line_data[1]]),line_data)
                        GM_66451_Count[line_data[1]] +=1
                if line_data[1] =="0xC7":
                    if device == "66451":
                        reg_process_0xCX(filename.split('.txt')[0]+'-'+line_data[1]+'-'+str(GM_66451_Count[line_data[1]]),line_data)
                        GM_66451_Count[line_data[1]] +=1
                if line_data[1] =="0xC8":
                    if device == "66451":
                        reg_process_0xCX(filename.split('.txt')[0]+'-'+line_data[1]+'-'+str(GM_66451_Count[line_data[1]]),line_data)
                        GM_66451_Count[line_data[1]] +=1
                if line_data[1] =="0xC9":
                    if device == "66451":
                        reg_process_0xCX(filename.split('.txt')[0]+'-'+line_data[1]+'-'+str(GM_66451_Count[line_data[1]]),line_data)
                        GM_66451_Count[line_data[1]] +=1
                if line_data[1] =="0xCA":
                    if device == "66451":
                        reg_process_0xCX(filename.split('.txt')[0]+'-'+line_data[1]+'-'+str(GM_66451_Count[line_data[1]]),line_data)
                        GM_66451_Count[line_data[1]] +=1
                if line_data[1] =="0xCB":
                    if device == "66451":
                        reg_process_0xCX(filename.split('.txt')[0]+'-'+line_data[1]+'-'+str(GM_66451_Count[line_data[1]]),line_data)
                        GM_66451_Count[line_data[1]] +=1
                continue
        pass
    file_to_read.close()
    return "success"

def reg_process_0xCF( filename, reg_data ):
    with open(filename+"_CF(BRC).txt","w") as file_to_write:
        write_str =     "             BRC ON:\t"+ str(True if int(reg_data[3],16)&0x02==0x02 else False)
        file_to_write.writelines(write_str)         
        write_str =     "\n           BRC Run:\t"+ "Normal Mode" if int(reg_data[3],16)&0x01==0x01 else "Temperature Mode"
        file_to_write.writelines(write_str)         
        write_str =     "\n   High temprature:\t"+str(int(reg_data[2],16))+"\t"+reg_data[2]
        file_to_write.writelines(write_str) 
        write_str =     "\n    Low temprature:\t"+str(int(reg_data[134],16))+"\t"+reg_data[134]
        file_to_write.writelines(write_str)

        Start_0XCF_index=4
        for i in range(5):
            write_str = "\n         DBV_THRESH"+str(i)+":\t"+ str(int(reg_data[Start_0XCF_index+i*2],16)*256+int(reg_data[Start_0XCF_index+1+i*2],16))+"\t"+reg_data[Start_0XCF_index+i*2]+reg_data[Start_0XCF_index+1+i*2][2:]
            file_to_write.writelines(write_str)  

        Start_0XCF_index=14       
        for i in range(6):
            write_str = "\n       GAMMA_TBL"+str(i)+"S/E:\t"+ str(int(reg_data[Start_0XCF_index+2*i],16))+"\t"+str(int(reg_data[Start_0XCF_index+1+2*i],16)) +"\t"+reg_data[Start_0XCF_index+2*i]+"\t"+reg_data[Start_0XCF_index+1+2*i]
            file_to_write.writelines(write_str) 

        Start_0XCF_index=26   
        for i in range(6):
            write_str = "\nGAMMA_TOP_RT_TBL"+str(i)+"S/E:\t"+ str(int(reg_data[Start_0XCF_index+i*4],16)*256+int(reg_data[Start_0XCF_index+1+i*4],16))+"\t"+str(int(reg_data[Start_0XCF_index+2+i*4],16)*256+int(reg_data[Start_0XCF_index+3+i*4],16)) +"\t"+\
                                                            reg_data[Start_0XCF_index+i*4]+reg_data[Start_0XCF_index+1+i*4][2:]+"\t"+reg_data[Start_0XCF_index+2+i*4]+reg_data[Start_0XCF_index+3+i*4][2:]
            file_to_write.writelines(write_str) 

        Start_0XCF_index=50        
        for i in range(6):
            write_str = "\nGAMMA_TOP_HT_TBL"+str(i)+"S/E:\t"+ str(int(reg_data[Start_0XCF_index+i*4],16)*256+int(reg_data[Start_0XCF_index+1+i*4],16))+"\t"+str(int(reg_data[Start_0XCF_index+2+i*4],16)*256+int(reg_data[Start_0XCF_index+3+i*4],16)) +"\t"+ \
                                                            reg_data[Start_0XCF_index+i*4]+reg_data[Start_0XCF_index+1+i*4][2:]+"\t"+reg_data[Start_0XCF_index+2+i*4]+reg_data[Start_0XCF_index+3+i*4][2:]
            file_to_write.writelines(write_str) 

        Start_0XCF_index=74        
        for i in range(6):
            write_str = "\n        VTOP_TBL"+str(i)+"S/E:\t"+ str(int(reg_data[Start_0XCF_index+i*4],16)*256+int(reg_data[Start_0XCF_index+1+i*4],16))+"\t"+str(int(reg_data[Start_0XCF_index+2+i*4],16)*256+int(reg_data[Start_0XCF_index+3+i*4],16)) +"\t"+\
                                                    reg_data[Start_0XCF_index+i*4]+reg_data[Start_0XCF_index+1+i*4][2:]+"\t"+reg_data[Start_0XCF_index+2+i*4]+reg_data[Start_0XCF_index+3+i*4][2:]
            file_to_write.writelines(write_str) 

        Start_0XCF_index=98       
        for i in range(6):
            write_str = "\n       ELVSS_TBL"+str(i)+"S/E:\t"+ str(int(reg_data[Start_0XCF_index+i],16))+"\t"+str(int(reg_data[Start_0XCF_index+1+i],16)) +"\t"+\
                                                    reg_data[Start_0XCF_index+i]+"\t"+reg_data[Start_0XCF_index+1+i]
            file_to_write.writelines(write_str) 

        Start_0XCF_index=110        
        for i in range(6):
            write_str = "\n    EMISSION_TBL"+str(i)+"S/E:\t"+ str(int(reg_data[Start_0XCF_index+i*4],16)*256+int(reg_data[Start_0XCF_index+1+i*4],16))+"\t"+str(int(reg_data[Start_0XCF_index+2+i*4],16)*256+int(reg_data[Start_0XCF_index+3+i*4],16)) +"\t"+\
                                                    reg_data[Start_0XCF_index+i*4]+reg_data[Start_0XCF_index+1+i*4][2:]+"\t"+reg_data[Start_0XCF_index+2+i*4]+reg_data[Start_0XCF_index+3+i*4][2:]
            file_to_write.writelines(write_str)         
        Start_0XCF_index=98       

        file_to_write.close()  

def reg_process_0xD7( filename, reg_data ):
    with open( filename +"_D7(LTPS_timing).txt","w") as file_to_write:
        write_str=""
        temp_data=0
        for i in range(16):
            write_str += "\nLFP"+str(i)+"_HI:\t"+ str(int(reg_data[i*16+2],16)*256+int(reg_data[3+i*16],16)/16)+"\t"+reg_data[i*16+2]+reg_data[3+i*16][2]
            write_str += "\nLFP"+str(i)+"_PER:\t"+ str((int(reg_data[i*16+3],16)%16)*256+int(reg_data[4+i*16],16))+"\t0x"+reg_data[i*16+3][3]+reg_data[4+i*16][2:]
            write_str += "\nLFP"+str(i)+"_SL:\t"+ str(int(reg_data[i*16+5],16)*256+int(reg_data[6+i*16],16)/16)+"\t"+reg_data[i*16+5]+reg_data[6+i*16][2]
            write_str += "\nLFP"+str(i)+"_EL:\t"+ str((int(reg_data[i*16+6],16)%16)*256+int(reg_data[7+i*16],16))+"\t0x"+reg_data[i*16+6][3]+reg_data[7+i*16][2:]
            write_str += "\nLFP"+str(i)+"_RE:\t"+ str(int(reg_data[i*16+8],16)*256+int(reg_data[9+i*16],16)/16)+"\t"+reg_data[i*16+8]+reg_data[9+i*16][2]
            write_str += "\nLFP"+str(i)+"_FE:\t"+ str((int(reg_data[i*16+9],16)%16)*256+int(reg_data[10+i*16],16))+"\t0x"+reg_data[i*16+9][3]+reg_data[10+i*16][2:]
            write_str += "\nLFP"+str(i)+"_LO:\t"+ str((int(reg_data[i*16+12],16)%16)*256+int(reg_data[13+i*16],16))+"\t0x"+reg_data[i*16+12][3]+reg_data[13+i*16][2:]
            write_str += "\nLFP"+str(i)+"_PL:\t"+ str(True if int(reg_data[i*16+11],16)&0x80==0x80 else False)
            write_str += "\nLFP"+str(i)+"_STOP_VAL:\t"+ str(True if int(reg_data[i*16+12],16)&0x80==0x80 else False)
            temp_data=(int(reg_data[i*16+11],16)&0x7c)/4
            write_str += "\nLFP"+str(i)+"_EL_SEL:\t"+ str(temp_data)+"\t"+hex(temp_data)
            temp_data=(int(reg_data[i*16+12],16)&0x70)/16
            write_str += "\nLFP"+str(i)+"_MODE:\t"+ str(temp_data)+"\t"+hex(temp_data)+"\n"
    
        file_to_write.writelines(write_str)  
        file_to_write.close()  

def reg_process_0xCX( filename, reg_data ):
    with open( filename +"_(Gamma).txt","w") as file_to_write:
        write_str="\tR(dec)\t(hex)\tG(dec)\t(hex)\tB(dec)\t(hex)"
        temp_data=0
        i=0

        for j in range(1,11,2):
            write_str += "\n"+str(j+1)+"X:\t"+str(int(reg_data[0*48+4*j+4],16)*256+int(reg_data[0*48+4*j+5],16))+"\t"+reg_data[0*48+4*j+4]+reg_data[0*48+4*j+5][2:]
            write_str += "\t"+str(int(reg_data[1*48+4*j+4],16)*256+int(reg_data[1*48+4*j+5],16))+"\t"+reg_data[1*48+4*j+4]+reg_data[1*48+4*j+5][2:]
            write_str += "\t"+str(int(reg_data[2*48+4*j+4],16)*256+int(reg_data[2*48+4*j+5],16))+"\t"+reg_data[2*48+4*j+4]+reg_data[2*48+4*j+5][2:]
        for j in range(0,11,2):
            write_str += "\n"+str(j+1)+"X:\t"+str(int(reg_data[0*48+4*j+4],16)*256+int(reg_data[0*48+4*j+5],16))+"\t"+reg_data[0*48+4*j+4]+reg_data[0*48+4*j+5][2:]
            write_str += "\t"+str(int(reg_data[1*48+4*j+4],16)*256+int(reg_data[1*48+4*j+5],16))+"\t"+reg_data[1*48+4*j+4]+reg_data[1*48+4*j+5][2:]
            write_str += "\t"+str(int(reg_data[2*48+4*j+4],16)*256+int(reg_data[2*48+4*j+5],16))+"\t"+reg_data[2*48+4*j+4]+reg_data[2*48+4*j+5][2:]
        for j in range(0,12,2):
            write_str += "\n"+str(j)+"Y:\t"+str(int(reg_data[0*48+4*j+2],16)*256+int(reg_data[0*48+4*j+3],16))+"\t"+reg_data[0*48+4*j+2]+reg_data[0*48+4*j+3][2:]
            write_str += "\t"+str(int(reg_data[1*48+4*j+2],16)*256+int(reg_data[1*48+4*j+3],16))+"\t"+reg_data[1*48+4*j+2]+reg_data[1*48+4*j+3][2:]
            write_str += "\t"+str(int(reg_data[2*48+4*j+2],16)*256+int(reg_data[2*48+4*j+3],16))+"\t"+reg_data[2*48+4*j+2]+reg_data[2*48+4*j+3][2:]
       
        write_str += "\n"+str(12)+"Y:\t"+str(int(reg_data[0*48+46+2],16)*256+int(reg_data[0*48+46+3],16))+"\t"+reg_data[i*48+46+2]+reg_data[i*48+46+3][2:]
        write_str += "\t"+str(int(reg_data[1*48+46+2],16)*256+int(reg_data[1*48+46+3],16))+"\t"+reg_data[1*48+46+2]+reg_data[1*48+46+3][2:]
        write_str += "\t"+str(int(reg_data[2*48+46+2],16)*256+int(reg_data[2*48+46+3],16))+"\t"+reg_data[2*48+46+2]+reg_data[2*48+46+3][2:]

        for j in range(1,11,2):
            write_str += "\n"+str(j)+"Y:\t"+str(int(reg_data[0*48+4*j+2],16)*256+int(reg_data[0*48+4*j+3],16))+"\t"+reg_data[0*48+4*j+2]+reg_data[0*48+4*j+3][2:]
            write_str += "\t"+str(int(reg_data[1*48+4*j+2],16)*256+int(reg_data[1*48+4*j+3],16))+"\t"+reg_data[1*48+4*j+2]+reg_data[1*48+4*j+3][2:]
            write_str += "\t"+str(int(reg_data[2*48+4*j+2],16)*256+int(reg_data[2*48+4*j+3],16))+"\t"+reg_data[2*48+4*j+2]+reg_data[2*48+4*j+3][2:]      
#----just for different output format 
        write_str+="\n\tR(dec)\tG(dec)\tB(dec)"
        write_str+="\n0X(fixed)\t00\t00\t00"
        for j in range(1,11,2):
            write_str += "\n"+str(j+1)+"X:\t"+str(int(reg_data[0*48+4*j+4],16)*256+int(reg_data[0*48+4*j+5],16))
            write_str += "\t"+str(int(reg_data[1*48+4*j+4],16)*256+int(reg_data[1*48+4*j+5],16))
            write_str += "\t"+str(int(reg_data[2*48+4*j+4],16)*256+int(reg_data[2*48+4*j+5],16))
        write_str+="\nX(fixed)\t1023\t1023\t1023"
        for j in range(0,11,2):
            write_str += "\n"+str(j+1)+"X:\t"+str(int(reg_data[0*48+4*j+4],16)*256+int(reg_data[0*48+4*j+5],16))
            write_str += "\t"+str(int(reg_data[1*48+4*j+4],16)*256+int(reg_data[1*48+4*j+5],16))
            write_str += "\t"+str(int(reg_data[2*48+4*j+4],16)*256+int(reg_data[2*48+4*j+5],16))
        for j in range(0,12,2):
            write_str += "\n"+str(j)+"Y:\t"+str(int(reg_data[0*48+4*j+2],16)*256+int(reg_data[0*48+4*j+3],16))
            write_str += "\t"+str(int(reg_data[1*48+4*j+2],16)*256+int(reg_data[1*48+4*j+3],16))
            write_str += "\t"+str(int(reg_data[2*48+4*j+2],16)*256+int(reg_data[2*48+4*j+3],16))
       
        write_str += "\n"+str(12)+"Y:\t"+str(int(reg_data[0*48+46+2],16)*256+int(reg_data[0*48+46+3],16))
        write_str += "\t"+str(int(reg_data[1*48+46+2],16)*256+int(reg_data[1*48+46+3],16))
        write_str += "\t"+str(int(reg_data[2*48+46+2],16)*256+int(reg_data[2*48+46+3],16))

        for j in range(1,11,2):
            write_str += "\n"+str(j)+"Y:\t"+str(int(reg_data[0*48+4*j+2],16)*256+int(reg_data[0*48+4*j+3],16))
            write_str += "\t"+str(int(reg_data[1*48+4*j+2],16)*256+int(reg_data[1*48+4*j+3],16))
            write_str += "\t"+str(int(reg_data[2*48+4*j+2],16)*256+int(reg_data[2*48+4*j+3],16))   

#----just for different output format 
        write_str+="\n\tR(dec)\tG(dec)\tB(dec)"
        write_str+="\n0X(fixed)\t00\t00\t00"
        for j in range(0,11,1):
            write_str += "\n"+str(j+1)+"X:\t"+str(int(reg_data[0*48+4*j+4],16)*256+int(reg_data[0*48+4*j+5],16))
            write_str += "\t"+str(int(reg_data[1*48+4*j+4],16)*256+int(reg_data[1*48+4*j+5],16))
            write_str += "\t"+str(int(reg_data[2*48+4*j+4],16)*256+int(reg_data[2*48+4*j+5],16))
        write_str+="\nX(fixed)\t1023\t1023\t1023"

        for j in range(0,12,1):
            write_str += "\n"+str(j)+"Y:\t"+str(int(reg_data[0*48+4*j+2],16)*256+int(reg_data[0*48+4*j+3],16))
            write_str += "\t"+str(int(reg_data[1*48+4*j+2],16)*256+int(reg_data[1*48+4*j+3],16))
            write_str += "\t"+str(int(reg_data[2*48+4*j+2],16)*256+int(reg_data[2*48+4*j+3],16))
       
        write_str += "\n"+str(12)+"Y:\t"+str(int(reg_data[0*48+46+2],16)*256+int(reg_data[0*48+46+3],16))
        write_str += "\t"+str(int(reg_data[1*48+46+2],16)*256+int(reg_data[1*48+46+3],16))
        write_str += "\t"+str(int(reg_data[2*48+46+2],16)*256+int(reg_data[2*48+46+3],16))

           
#----just for different output format 
        for Color in ["R","G","B"]:
            for j in range(12):
                write_str += "\n"+Color+"_"+str(j)+"Y:\t"+str(int(reg_data[i*48+4*j+2],16)*256+int(reg_data[i*48+4*j+3],16))+"\t"+reg_data[i*48+4*j+2]+reg_data[i*48+4*j+3][2:]
            write_str += "\n"+Color+"_"+str(12)+"Y:\t"+str(int(reg_data[i*48+46+2],16)*256+int(reg_data[i*48+46+3],16))+"\t"+reg_data[i*48+46+2]+reg_data[i*48+46+3][2:]
            for j in range(11):
                write_str += "\n"+Color+"_"+str(j+1)+"X:\t"+str(int(reg_data[i*48+4*j+4],16)*256+int(reg_data[i*48+4*j+5],16))+"\t"+reg_data[i*48+4*j+4]+reg_data[i*48+4*j+5][2:]
            i+=1
    
        file_to_write.writelines(write_str)  
        file_to_write.close()  

def process_analzye(filename, reg_name, reg_data):
    if reg_name=="0xCF":
        reg_process_0xCF(filename,reg_data)
    if reg_name=="0xD7":
        reg_process_0xD7(filename,reg_data)
#class reg_map_1E4(object):
    
class satis_frame(object):
    tx_num = 0
    tx_num = 0
    matrix = [[0 for i in range(48)] for i in range(96)]
    def __init__(self, min, max, TimeStamp,tx_num, rx_num):
        self.min = min
        self.max = max
        self.TimeStamp = TimeStamp
        self.tx_num = tx_num
        self.rx_num = rx_num
        self.data = [[0 for i in range(rx_num)] for i in range(tx_num)]
    pass
def satis_matrix(min_max=[0,0],limit=[0,0]):

    pass

def writeToTxt(list_name,matrix,file_path,start_time_str="",end_time_str="",limit_level=[0,0]):
    try:
        fp = open(file_path,"w")
        item_str=""
        list_str=[]
        list_str.append( "Time:(Hour/Minute/Second/MS):("+str(limit_level[0])+","+str(limit_level[1])+")\t"+start_time_str+"--"+end_time_str +"\n" )

        item_str="TX/RX:"
        for j in range(matrix[1]):
            item_str+="\tR"+str(j)
        list_str.append(item_str+"\n")
        for i in range(matrix[0]):
            item_str="T"+str(i)+":"
            for j in range(matrix[1]):
                item_str+="\t"+str(list_name[i][j])
            list_str.append(item_str+"\n")
            
        fp.writelines(list_str)
        fp.close()
    except IOError:
        print("fail to open file")

def writeRowColToTxt(list_name,matrix,file_path,t1="", t2=""):
    try:
        fp = open(file_path,"w")
        item_str=""
        list_str=[]
        list_str.append( t1+"\n" )
        list_str.append(t2+"\n")
        for i in range(matrix[0]):
            item_str=""
            for j in range(matrix[1]):
                item_str+=str(list_name[i][j])+"\t"
            list_str.append(item_str+"\n")
            
        fp.writelines(list_str)
        fp.close()
    except IOError:
        print("fail to open file")

def write_limit_ToTxt(list_min,list_max,matrix,file_path):
    try:
        fp = open(file_path,"w")
        item_str=""
        list_str=[]
        item_str="TX/RX:"
        for j in range(matrix[1]):
            item_str+="\tR"+str(j)
        list_str.append(item_str+"\n")
        for i in range(matrix[0]):
            item_str="T"+str(i)+":"
            for j in range(matrix[1]):
                item_str+="\t"+str(list_min[i][j])+','+str(list_max[i][j])
            list_str.append(item_str+"\n")
            
        fp.writelines(list_str)
        fp.close()
    except IOError:
        print("fail to open file")

def write_noise_ToTxt(list_min,matrix,file_path):
    try:
        fp = open(file_path,"w")
        item_str=""
        list_str=[]
        for l in range(len(list_min)):
            item_str="TX/RX:"
            for j in range(matrix[1]):
                item_str+="\tR"+str(j)
            list_str.append(item_str+"\n")
            for i in range(matrix[0]):
                item_str="T"+str(i)+":"
                for j in range(matrix[1]):
                    item_str+="\t"+str(list_min[l][i][j])
                list_str.append(item_str+"\n")
            
        fp.writelines(list_str)
        fp.close()
    except IOError:
        print("fail to open file")

def ClearList(list_name,matrix):
    for i in range(matrix[0]):
        for j in range(matrix[1]):  
            list_name[i][j]=0
#tx_rx_log_info: tx_num/rx_num/TimeStamp/data_start/sum_info(min/max data)
#tx_rx_log_info tx/rx/rt2-6 log structure:time/data start min_max line frame_size
def statis_matrix_max_min( filename , limit=[[-40,40],[10,20,40,50],[1,0,0,0]], tx_rx_log_info=[[16,32],[1,4,20,22]] ): 
    line_data_int = []

    frame_data = [[0 for i in range(tx_rx_log_info[0][1])] for i in range(tx_rx_log_info[0][0])]
    frame_data_cnt = [[0 for i in range(tx_rx_log_info[0][1])] for i in range(tx_rx_log_info[0][0])]
    all_frame_data=[]
    all_frame_min_max=[]
    result_min_max_pos=[] #frame No./value/pos_x/pos_y
    start_time_str=""
    end_time_str=""
    all_lines = []    
    with open(filename, 'r') as file_to_read:
        all_lines = file_to_read.readlines()
    file_to_read.close()
    mininum_value=0
    maxum_value=0

    for l in range(len(limit[1])):
    #    writeToTxt(frame_data_cnt,[16,32],filename+str(limit[1][l])+"%_satis.txt",start_time_str,end_time_str)
        try:
            fp = open(filename+str(limit[1][l])+"%_statis_detail.log","w")
        except IOError:
            print("fail to open file")

        for i in range(len(all_lines)/tx_rx_log_info[1][3]):
            start = i*tx_rx_log_info[1][3]+tx_rx_log_info[1][0]
            line_data = re.split(r"[ =\t]",all_lines[start])
            if i == 0:
                start_time_str = line_data[6]
            else:
                end_time_str = line_data[6]

            start = i*tx_rx_log_info[1][3]+tx_rx_log_info[1][2]

            #line_data = all_lines[start].split(':')
            line_data = re.split(r"[ :\t]",all_lines[start])
            Min_str = line_data[2]
            Min_str.strip()
            Min_int = int(Min_str)

            Max_str = line_data[5]
            Max_str.strip()
            Max_int = int(Max_str)
            temp = limit[0][0]*(1-limit[1][l]/100.0)
            if (Min_int > limit[0][0]*(1-limit[1][l]/100.0)) and (Max_int < limit[0][1]*(1-limit[1][l]/100.0)):
                continue
            
            if mininum_value > Min_int or maxum_value < Max_int:
                pass
            
            #fp.writelines( "Frame No:"+str(i)+"\t"+all_lines[start])
            frame_count = 0
            frame_head = "Frame No:"+str(i)+"\t"
            frame_statis = all_lines[start][:-1-1]
            frame_spike =""
            start = i*tx_rx_log_info[1][3]+tx_rx_log_info[1][1]
            frame_row = 0
            frame_list_temp=[]
            temp_line="TX/RX"  
            for k in range(tx_rx_log_info[0][1]):
                temp_line+="\tR"+str(k)    
            frame_list_temp.append(temp_line+"\n")

            for j in range(start,start+tx_rx_log_info[0][0]):
                temp_line="T"+str(frame_row)+"\t"
                line_data = all_lines[j].split(',')
                for k in range(tx_rx_log_info[0][1]):
                    ADC_str = line_data[k]
                    ADC_str.strip()

                    ADC_int = int(ADC_str)
                    frame_data[j-start][k]=ADC_int
                    if ADC_int < 0:
                        if ADC_int <= limit[0][0]*(1-limit[1][l]/100.0):
                            frame_data_cnt[j-start][k]+=1
                            for min_cnt in range(len(limit[2])):
                                if ADC_int < limit[0][0]*(limit[2][min_cnt]+1):
                                    result_min_max_pos.append([i,ADC_int,j,k])
                            if k == 0:
                                temp_line += ADC_str+"\t"
                                frame_spike += '('+ str(frame_row)+','+str(k)+":"+ADC_str+')'
                            else:
                                temp_line += ADC_str[1:]+"\t" 
                                frame_spike += '('+ str(frame_row)+','+str(k)+":"+ADC_str[1:]+')'
                            #frame_spike += '('+ str(frame_row)+','+str(k)+')'
                            frame_count+=1
                        elif ADC_int <= limit[0][0]*(1-limit[1][l]/100.0)+limit[3][0]:
                            if k == 0:
                                temp_line += ADC_str+"\t"
                                frame_spike += '('+ str(frame_row)+','+str(k)+":"+ADC_str+')'
                            else:
                                temp_line += ADC_str[1:]+"\t"
                                frame_spike += '('+ str(frame_row)+','+str(k)+":"+ADC_str[1:]+')'
                            #frame_spike += '('+ str(frame_row)+','+str(k)+')'
                            frame_count+=1
                        else:
                            temp_line +="0\t"

                    else:
                        if ADC_int >= limit[0][1]*(1-limit[1][l]/100.0):
                            #result_min_max_pos.append([i,ADC_int,j,k]) 
                            frame_data_cnt[j-start][k]+=1
                            frame_count +=1
                            for min_cnt in range(len(limit[2])):
                                if ADC_int > limit[0][1]*(limit[2][min_cnt]+1):
                                    result_min_max_pos.append([i,ADC_int,j,k]) 
                            if k == 0:
                                temp_line += ADC_str+"\t"
                                frame_spike += '('+ str(frame_row)+','+str(k)+":"+ADC_str+')'
                            else:
                                temp_line += ADC_str[1:]+"\t"
                                frame_spike += '('+ str(frame_row)+','+str(k)+":"+ADC_str[1:]+')'
                            #frame_spike += '('+ str(frame_row)+','+str(k)+')'
                            frame_count+=1

                        elif ADC_int >= limit[0][1]*(1-limit[1][l]/100.0)+limit[3][1]:
                            if k == 0:
                                temp_line += ADC_str+"\t"
                                frame_spike += '('+ str(frame_row)+','+str(k)+":"+ADC_str+')'
                            else:
                                temp_line += ADC_str[1:]+"\t"
                                frame_spike += '('+ str(frame_row)+','+str(k)+":"+ADC_str[1:]+')'
                            #frame_spike += '('+ str(frame_row)+','+str(k)+')'
                            frame_count+=1
                        else:
                            temp_line +="0\t"
                pass
                frame_row+=1
                temp_line +="\n"
                #fp.writelines(temp_line)
                frame_list_temp.append(temp_line)
            pass
            frame_head+= frame_statis+ "\tAll spike="+str(frame_count)+":(row,col)"+frame_spike+"\n"
            fp.writelines(frame_head)
            fp.writelines(frame_list_temp)
            #all_frame_data.append(frame_data)
            #all_frame_min_max.append([Min_int,Max_int])
        pass
        fp.close()

        writeToTxt(frame_data_cnt,[16,32],filename+str(limit[1][l])+"%_statis_count.log",start_time_str,end_time_str,[int((1-limit[1][l]/100.0)*limit[0][0]),int((1-limit[1][1]/100.0)*limit[0][1])])
        if len(result_min_max_pos) > 0:
            writeRowColToTxt(result_min_max_pos,[len(result_min_max_pos),4],filename+str(limit[1][l])+"%_spike.log","","F No.\tValue\tRow\tCol\n")
        #del frame_data_cnt[:]
        result_min_max_pos=[]
        for m in range(tx_rx_log_info[0][0]):
            for n in range(tx_rx_log_info[0][1]):  
                frame_data_cnt[m][n]=0
    return "success"

#tx_rx_log_info: tx_num/rx_num/TimeStamp/data_start/sum_info(min/max data)
#tx_rx_log_info tx/rx/rt2-6 log structure:time/data start min_max line frame_size
def statis_raw_cap_type_limit( filename , test_name, limit=[[-40,40,0,0],[20,25,30]], tx_rx_log_info=[[18,30,1,2],[2,3,7,4]] ): 
    line_data_int = []

    frame_data = [[0 for i in range(tx_rx_log_info[0][1])] for i in range(tx_rx_log_info[0][0]+1)]
    frame_data_cnt = [[0 for i in range(tx_rx_log_info[0][1])] for i in range(tx_rx_log_info[0][0]+1)]
    limit_data_min = [[0 for i in range(tx_rx_log_info[0][1])] for i in range(tx_rx_log_info[0][0]+1)]
    limit_data_max = [[0 for i in range(tx_rx_log_info[0][1])] for i in range(tx_rx_log_info[0][0]+1)]
    all_frame_data=[]
    all_frame_min_max=[]
    result_min_max_pos=[] #frame No./value/pos_x/pos_y
    start_time_str=""
    end_time_str=""
    all_lines = []    
    all_good_frame_cnt=0

    for filecnt in range(len(filename)):
        with open(filename[filecnt], 'r') as file_to_read:
            all_lines = file_to_read.readlines()
        file_to_read.close()
        start = 0

        for i in range(len(all_lines)):
            start_pos=all_lines[i].find(test_name)
            if start_pos != -1:
                start=i
                break
            else : continue

        if start == 0:
            continue

        start_pos = all_lines[start+tx_rx_log_info[1][0]].find("Pass")
        if start_pos != -1:   # good sample
            start += tx_rx_log_info[1][2]
            for j in range(start,start+tx_rx_log_info[0][0]):
                line_data = all_lines[j].split(':')[1].split(",")
                for k in range(tx_rx_log_info[0][1]):
                    ADC_str = line_data[k]
                    ADC_str.strip()

                    ADC_int = float(ADC_str)
                    frame_data[j-start][k]+=ADC_int
                    #if ADC_int < 0:
                    #    if ADC_int < limit[0][0]*(1-limit[1][l]/100.0):
                        #result_min_max_pos.append([i,ADC_int,j,k]) 
                    #        frame_data_cnt[j-start][k]+=1

                    #elif ADC_int > limit[0][1]*(1-limit[1][l]/100.0):
                        #result_min_max_pos.append([i,ADC_int,j,k]) 
                    #    frame_data_cnt[j-start][k]+=1
                pass
            pass
            if tx_rx_log_info[0][2] == 1: #handle 0D area
                line_data = all_lines[j+1].split(':')[1].split(",")
                for k in range(tx_rx_log_info[0][3]):
                    ADC_str = line_data[k]
                    ADC_str.strip()
                    ADC_int = float(ADC_str)
                    frame_data[j-start+1][k] += ADC_int
            #all_frame_data.append(frame_data)
            all_good_frame_cnt+=1
            #all_frame_min_max.append([Min_int,Max_int])

            pass
        else:
            pass

    pass

    for m in range(tx_rx_log_info[0][0]):
        for n in range(tx_rx_log_info[0][1]):  
            frame_data[m][n]/=all_good_frame_cnt

    if tx_rx_log_info[0][2] == 1: #handle 0D area
        for n in range(tx_rx_log_info[0][3]):
            frame_data[tx_rx_log_info[0][0]][n]/=all_good_frame_cnt

    for l in range(len(limit[1])):
        for m in range(tx_rx_log_info[0][0]):
            for n in range(tx_rx_log_info[0][1]):  
                limit_data_min[m][n]=frame_data[m][n]*(1-limit[1][l]/100.0)
                limit_data_max[m][n]=frame_data[m][n]*(1+limit[1][l]/100.0)
                #frame_data[m][m]=0       
        if tx_rx_log_info[0][2] == 1: #handle 0D area
            for n in range(tx_rx_log_info[0][3]):  
                limit_data_min[tx_rx_log_info[0][0]][n]=frame_data[tx_rx_log_info[0][0]][n]*(1-limit[1][l]/100.0)
                limit_data_max[tx_rx_log_info[0][0]][n]=frame_data[tx_rx_log_info[0][0]][n]*(1+limit[1][l]/100.0)
        
        #writeToTxt(all_frame_data,limit[1],filename+str(limit[1][l])+"%_raw_image_limit.log")
        write_limit_ToTxt(limit_data_min,limit_data_max,[tx_rx_log_info[0][0]+tx_rx_log_info[0][2],tx_rx_log_info[0][1]], test_name+'-'+str(limit[1][l])+"%_raw_image_limit.log")
        pass
    return "success"

#tx_rx_log_info: tx_num/rx_num/TimeStamp/data_start/sum_info(min/max data)
#tx_rx_log_info tx/rx/rt2-6 log structure:time/data start min_max line frame_size
def statis_noise_type( filename , test_name, limit=[[-40,40,0,0],[20,25,30]], tx_rx_log_info=[[18,30,1,2],[2,3,7,4]] ): 
    line_data_int = []

    frame_data = [[0 for i in range(tx_rx_log_info[0][1])] for i in range(tx_rx_log_info[0][0]+1)]
    frame_data_cnt = [[0 for i in range(tx_rx_log_info[0][1])] for i in range(tx_rx_log_info[0][0]+1)]
    limit_data_min = [[0 for i in range(tx_rx_log_info[0][1])] for i in range(tx_rx_log_info[0][0]+1)]
    limit_data_max = [[0 for i in range(tx_rx_log_info[0][1])] for i in range(tx_rx_log_info[0][0]+1)]
    all_LCM_NG_data=[]
    all_frame_min_max=[]
    result_min_max_pos=[] #frame No./value/pos_x/pos_y
    start_time_str=""
    end_time_str=""
    all_lines = []    
    all_OK_LCM_cnt=0
    all_NG_LCM_cnt=0
    limit_read = False

    for filecnt in range(len(filename)):
        with open(filename[filecnt], 'r') as file_to_read:
            all_lines = file_to_read.readlines()
        file_to_read.close()
        start = 0

        for i in range(len(all_lines)):
            start_pos=all_lines[i].find(test_name)
            if start_pos != -1:
                start=i
                break
            else : continue

        if start == 0:
            continue
        
        #limit_data_min

        start_pos = all_lines[start+tx_rx_log_info[1][0]].find("Fail")
        if start_pos != -1:   
            start_data = start #backup the poistion of test item

            if limit_read == False:# read limit
                start += tx_rx_log_info[1][2]+tx_rx_log_info[0][0]+tx_rx_log_info[1][3]
                for j in range(start,start+tx_rx_log_info[0][0]):
                    line_data = all_lines[j].split(':')[1].split(",")
                    for k in range(tx_rx_log_info[0][1]):
                        ADC_str = line_data[k]
                        ADC_str.strip()

                        ADC_int = int(ADC_str)
                        limit_data_min[j-start][k]+=ADC_int
                    pass
                pass
                limit_read = True
                if tx_rx_log_info[0][2] == 1: #handle 0D area
                    line_data = all_lines[j+1].split(':')[1].split(",")
                    for k in range(tx_rx_log_info[0][3]):
                        ADC_str = line_data[k]
                        ADC_str.strip()
                        ADC_int = int(ADC_str)
                        limit_data_min[j-start+1][k] += ADC_int
            
            start = start_data+tx_rx_log_info[1][2] #statis noise
            for j in range(start,start+tx_rx_log_info[0][0]):
                line_data = all_lines[j].split(':')[1].split(",")
                for k in range(tx_rx_log_info[0][1]):
                    ADC_str = line_data[k]
                    ADC_str.strip()

                    ADC_int = float(ADC_str)
                    if ADC_int > limit_data_min[j-start][k]:
                        frame_data[j-start][k]=ADC_int
                pass
            pass

            if tx_rx_log_info[0][2] == 1: #handle 0D area
                line_data = all_lines[j+1].split(':')[1].split(",")
                for k in range(tx_rx_log_info[0][3]):
                    ADC_str = line_data[k]
                    ADC_str.strip()
                    ADC_int = float(ADC_str)

                    if ADC_int > limit_data_min[j-start+1][k]:
                        frame_data[j-start+1][k] = ADC_int

            all_NG_LCM_cnt+=1
            all_LCM_NG_data.append(frame_data)
            pass
        else:
            all_OK_LCM_cnt+=1
            pass

    pass
        
        #writeToTxt(all_frame_data,limit[1],filename+str(limit[1][l])+"%_raw_image_limit.log")
    write_noise_ToTxt(all_LCM_NG_data,[tx_rx_log_info[0][0]+tx_rx_log_info[0][2],tx_rx_log_info[0][1]], test_name+'-NG.log')
    pass

    return "success"

def satis_adc( filename , op_type, ADC_ERR_CONST, RT_TYPE="RT12", limit=[-9,9], tx_rx=[16,32] ):
    TX_NUM=tx_rx[0]
    RX_NUM=tx_rx[1]
    Frame_start=False
    Frame_cnt=0
    line_data_int = []
    ADC_convert_err = ["Frame\tTX_POS\tRX_POS\tINT()\tHEX()\tErrMatch\n"]
    ADC_convert_err_item=[]
    MIN_RT=0
    MAX_RT=0
    i=0
    j=0
    
    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readlines(4) # 整行读取数据
            if not lines:
                break
                pass
            lines=lines.strip()
            if lines =='':
                continue
            if lines[0]=='#':
                continue
            line_pos = lines.find("Dmax")
            if line_pos != -1:
                TX_NUM=int(lines[line_pos+7:])
                satis_frame.tx_num = TX_NUM
                continue


            line_pos = lines.find("Smax")
            if line_pos != -1:
                RX_NUM=int(lines[line_pos+7:])
                satis_frame.rx_num = RX_NUM
                continue

            line_pos = lines.find("TimeStamp")
            if line_pos != -1:
                line_data = lines.split()
                TimeStamp = line_data[4]
                continue

            line_pos = lines.find("Min")
            if line_pos != -1:
                line_data = lines.split('\t')
                MIN_RT=int(line_data[1])
                MAX_RT=int(line_data[3])
                satis_matrix([MIN_RT,MAX_RT],limit)
                continue

            line_pos = lines.find("END")
            if line_pos != -1:
                Frame_start=False
                continue 
            line_pos = lines.find("BEGIN")
            if line_pos != -1:
                Frame_start=True
                Frame_cnt+=1
                j=0
                continue   
        
            if Frame_start==True:
                line_data=lines.split(',')
                i=0

                for ADC_str in line_data:
                    ADC_str.strip()
                    if ADC_str=='':
                        continue
                    ADC_int = int(ADC_str)
                    satis_frame.matrix[j][i] = float(ADC_str)
                    #line_data_int.append(ADC_int)
                    if RT_TYPE == "RT12":
                        for ADC_CONST in ADC_ERR_CONST:
                            if ADC_int&ADC_CONST == ADC_CONST:
                                ADC_convert_err.append(str(Frame_cnt)+'\t'+str(j)+'\t'+str(i)+'\t'+str(ADC_int)+'\t'+hex(ADC_int)+'\t'+hex(ADC_CONST)+"\n")
                                break
                    i+=1
                j+=1
                if j==TX_NUM:
                    Frame_start=False
        # pos.append(p_tmp)  # 添加新读取的数据
        # Efield.append(E_tmp)
        pass
    file_to_read.close()
    with open(filename+"satis.txt","w") as file_to_write:
        file_to_write.writelines(ADC_convert_err) 
    file_to_write.close()
    return "success"

def ReadIni(path,section,option):#文件路径，章节，关键词 
    #读取ini
    cf=ConfigParser.ConfigParser() 
    cf.read(path) 
    value=cf.get(section,option)#如果用getint()则直接读取该数据类型为整数 
    return value 

def IsPassLine(strLine): 
    #是否是可以忽略的行 
    #可忽略行的正则表达式列表 
    RegularExpressions=["""/"/"/""","""/'.*#.*/'""","""/".*#.*/""","""/'/'/'.*#.*/'/'/'""","""/"/"/".*#.*/"/"/"""]
    for One in RegularExpressions: 
        zz=re.compile(One) 
        if re.search(zz,strLine)==None: 
            continue
        else: 
            return True#有匹配 则忽略 
    return False

def ReadFile(FileName): 
    #读取并处理文件 
    fobj=open(FileName,'r') 
    AllLines=fobj.readlines() 
    fobj.close() 
    nline=0
    for eachiline in AllLines: 
        index=eachiline.find('#')#获取带注释句‘#'的位置索引 
        nline+=1
    return NewStr,LogStr 

def calc_test_log(SrcPath,DescPath,FileList, op_type):
    fLog=open(DescPath+'//'+'CleanNoteLog.txt','w') 
    for File in FileList: 
        curStr,LogStr=ReadFile(SrcPath+'//'+File) 
        fNew=open(DescPath+'//'+File,'w') 
        fNew.write(curStr) 
        fNew.close() 
        fLog.write(LogStr) 
    fLog.close() 

def calc_raw_image( dir_path='', op_type='' ): 
    #从ini获取源文件夹及目标文件夹路径 
    PyName="config"
    if dir_path =='':
        IniPath=os.getcwd()+'//'+PyName+'.ini'
        SrcPath=ReadIni(IniPath,PyName,'SrcPath')#源文件夹 
        DescPath=ReadIni(IniPath,PyName,'DescPath')#目的文件夹
        op_type =ReadIni(IniPath,PyName,'OP_TYPE')#Operation type 
    #如果目的文件夹不存在，创建之 
        if not os.path.exists(DescPath): 
            os.makedirs(DescPath) 
    else:
        SrcPath=dir_path
        DescPath=dir_path+'//out'
        os.makedirs(DescPath)
        if op_type=='':
            op_type="TDDI_4322_RT3"

    FileList=[] 
    for files in os.walk(SrcPath): 
        for FileName in files[2]: 
            if FileName.split('.')[-1]=='txt': 
                FileList.append(FileName) 
    calc_test_log(SrcPath,DescPath,FileList, op_type) 

def get_src_file( inifile='',file_type='txt'):
    #从ini获取源文件夹及目标文件夹路径 
    CMD_num=0
    CMD_type_num=0
    DIR_HIERARCH=0
    CMD_list=[]
    CMD_param=[]
    CMD_name=[]
    CMD_type=[]
    PyName="cfg_register"
    if inifile=='':
        IniPath=os.getcwd()+'//'+PyName+'.ini'
    else:    
        IniPath = inifile

    SrcPath=ReadIni(IniPath,PyName,'SrcPath')#源文件夹 
    DescPath=ReadIni(IniPath,PyName,'DescPath')#目的文件夹
    op_type =ReadIni(IniPath,PyName,'OP_TYPE')#Operation type 
    CMD_num=int(ReadIni(IniPath,PyName,'TEST_CMD'))
    CMD_type_num = int(ReadIni(IniPath,PyName,'TEST_CMD_TYPE'))
    DIR_HIERARCH=int(ReadIni(IniPath,PyName,'DIR_HIERARCH'))

    for i in range(CMD_num):
        CMD_list.append(ReadIni(IniPath,PyName,'TEST_CMD'+str(i)))
        CMD_param.append(ReadIni(IniPath,PyName,'TEST_CMD_PARAM'+str(i)))

        #CMD_name.append(ReadIni(IniPath,PyName,'TEST_CMD_NAME'+str(i)))
    for i in range(CMD_type_num):
        CMD_type.append(ReadIni(IniPath,PyName,'TEST_CMD_NAME'+str(i)))

    #如果目的文件夹不存在，创建之 
    if not os.path.exists(DescPath): 
        os.makedirs(DescPath) 

    FileList=[] 
    if op_type == "dir":  
        for files in os.walk(SrcPath): 
            for FileName in files[2]: 
                if FileName.split('.')[-1]==file_type: 
                    FileName = SrcPath+"/"+FileName
                    FileList.append(FileName) 
            if DIR_HIERARCH==1:
                break

    elif op_type == "file":
        FileList.append(SrcPath)

    return FileList,DescPath

def reg_analyze( inifile=''): 
    #从ini获取源文件夹及目标文件夹路径 
    CMD_num=0
    CMD_type_num=0
    CMD_list=[]
    CMD_param=[]
    CMD_name=[]
    CMD_type=[]
    PyName="cfg_register"
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

        #CMD_name.append(ReadIni(IniPath,PyName,'TEST_CMD_NAME'+str(i)))
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
        E7422_to_gx(file, ["0xCF","0xD7"])


def factory_test( inifile=''): 
    #从ini获取源文件夹及目标文件夹路径 
    CMD_num=0
    CMD_type_num=0
    CMD_list=[]
    CMD_param=[]
    CMD_name=[]
    CMD_type=[]
    PyName="cfg_register"
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

        #CMD_name.append(ReadIni(IniPath,PyName,'TEST_CMD_NAME'+str(i)))
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

    for j in range(len(CMD_list)):
        cmd_line=CMD_list[j].split(',')
        param_line=CMD_param[j].split(',')
        if cmd_line[0] == '07':
            limit = [[int(cmd_line[16]),int(cmd_line[17])],[int(param_line[i]) for i in range(len(param_line))]]
            tx_rx_log_struct = [[int(cmd_line[i]) for i in range(1,5)],[int(cmd_line[i]) for i in range(5,10)]]
            statis_raw_cap_type_limit(FileList,CMD_type[7],limit, tx_rx_log_struct)
        if cmd_line[0] == '04':
            limit = [[int(cmd_line[16]),int(cmd_line[17])],[int(param_line[i]) for i in range(len(param_line))]]
            tx_rx_log_struct = [[int(cmd_line[i]) for i in range(1,5)],[int(cmd_line[i]) for i in range(5,10)]]
            statis_raw_cap_type_limit(FileList,CMD_type[4],limit, tx_rx_log_struct)
        if cmd_line[0] == '05':
            limit = [[int(cmd_line[16]),int(cmd_line[17])],[int(param_line[i]) for i in range(len(param_line))]]
            tx_rx_log_struct = [[int(cmd_line[i]) for i in range(1,5)],[int(cmd_line[i]) for i in range(5,10)]]
            statis_noise_type(FileList,CMD_type[5],limit,tx_rx_log_struct)
        if cmd_line[0] == '06':
            limit = [[int(cmd_line[16]),int(cmd_line[17])],[int(param_line[i]) for i in range(len(param_line))],[int(cmd_line[i]) for i in range(18,18+len(param_line))],[int(cmd_line[i]) for i in range(18+len(param_line),18+len(param_line)+2)]]
            tx_rx_log_struct = [[int(cmd_line[i]) for i in range(1,5)],[int(cmd_line[i]) for i in range(5,10)]]
            for i in range(len(FileList)):
                statis_matrix_max_min(FileList[i],limit,tx_rx_log_struct)    #for i in range(len(FileList)):

class reg_file(object):
    device_name="Rxxxx"
    reg_map={}
    reg_filename=""

    def __init__(self, device_name, reg_filename ):
        self.device_name = device_name
        self.reg_filename = reg_filename
        for i in range(512):
            id_str = "0x"+hex(i)[2:].upper()
            self.reg_map[id_str]=[]
        pass

    def add_reg_to_map(self,reg_name,sub_reg_name,start_B,end_B,SB_s_b,SB_e_b, EB_s_b,EB_e_b):
        self.reg_map[reg_name].append([sub_reg_name,start_B,end_B,SB_s_b,SB_e_b, EB_s_b,EB_e_b])
    '''
    read reg structure file that's similar with R66451/R66455 etc.
    example file struct as below:
    REG-0x0CF:
    High Temp Value:0 0 0 7 0 7
    BRC Run_Mode: 1 1 0 0 0 0
    BRC_On:1 1 1 1 1 1
    PVSS_POL:1 1 3 3 3 3
    TEMP IP_SEL: 1 1 4 4 4 4
    DBV_THRESH1: 2 3 0 3 0 7
    DBV_THRESH2: 4 5 0 3 0 7
    DBV_THRESH3: 6 7 0 3 0 7
    DBV_THRESH4: 8 9 0 3 0 7
    DBV_THRESH5: 10 11 0 3 0 7
    Gamma_TBL0: 12 13 0 7 0 7
    Gamma_TBL1: 14 15 0 7 0 7
    Gamma_TBL2: 16 17 0 7 0 7
    Gamma_TBL3: 18 19 0 7 0 7
    Gamma_TBL4: 20 21 0 7 0 7
    Gamma_TBL5: 22 23 0 7 0 7
    GAMMA_TOP_RT_TBL0:24 25 0 1 0 7
    GAMMA_TOP_RT_TBL1:26 27 0 1 0 7
    GAMMA_TOP_RT_TBL2:28 29 0 1 0 7
    GAMMA_TOP_RT_TBL3:30 31 0 1 0 7
    GAMMA_TOP_RT_TBL4:32 33 0 1 0 7
    GAMMA_TOP_RT_TBL5:34 35 0 1 0 7
    GAMMA_TOP_RT_TBL6:36 37 0 1 0 7
    GAMMA_TOP_RT_TBL7:38 39 0 1 0 7
    GAMMA_TOP_RT_TBL8:40 41 0 1 0 7
    GAMMA_TOP_RT_TBL9:42 43 0 1 0 7
    GAMMA_TOP_RT_TBL10:44 45 0 1 0 7
    GAMMA_TOP_RT_TBL11:46 47 0 1 0 7
    GAMMA_TOP_HT_TBL0:48 49 0 1 0 7
    GAMMA_TOP_HT_TBL1:50 51 0 1 0 7
    GAMMA_TOP_HT_TBL2:52 53 0 1 0 7
    GAMMA_TOP_HT_TBL3:54 55 0 1 0 7
    GAMMA_TOP_HT_TBL4:56 57 0 1 0 7
    GAMMA_TOP_HT_TBL5:58 59 0 1 0 7
    GAMMA_TOP_HT_TBL6:60 61 0 1 0 7
    GAMMA_TOP_HT_TBL7:62 63 0 1 0 7
    GAMMA_TOP_HT_TBL8:64 65 0 1 0 7
    GAMMA_TOP_HT_TBL9:66 67 0 1 0 7
    GAMMA_TOP_HT_TBL10:68 69 0 1 0 7
    GAMMA_TOP_HT_TBL11:70 71 0 1 0 7
    VTOP_TBL0:72 73 0 0 0 7
    VTOP_TBL1:74 75 0 0 0 7
    VTOP_TBL2:76 77 0 0 0 7
    VTOP_TBL3:78 79 0 0 0 7
    VTOP_TBL4:80 81 0 0 0 7
    VTOP_TBL5:82 83 0 0 0 7
    VTOP_TBL6:84 85 0 0 0 7
    VTOP_TBL7:86 87 0 0 0 7
    VTOP_TBL8:88 89 0 0 0 7
    VTOP_TBL9:90 91 0 0 0 7
    VTOP_TBL10:92 93 0 0 0 7
    VTOP_TBL11:94 95 0 0 0 7
    ELVSS_TBL0:96 96 0 0 0 7
    ELVSS_TBL1:97 97 0 7 0 7
    ELVSS_TBL2:98 98 0 7 0 7
    ELVSS_TBL3:99 99 0 7 0 7
    ELVSS_TBL4:100 100 0 7 0 7
    ELVSS_TBL5:101 101 0 7 0 7
    ELVSS_TBL6:102 102 0 7 0 7
    ELVSS_TBL7:103 103 0 7 0 7
    ELVSS_TBL8:104 104 0 7 0 7
    ELVSS_TBL9:105 105 0 7 0 7
    ELVSS_TBL10:106 106 0 7 0 7
    ELVSS_TBL11:107 107 0 7 0 7
    EMISSION_TBL0:108 109 0 3 0 7
    EMISSION_TBL1:110 111 0 3 0 7
    EMISSION_TBL2:112 113 0 3 0 7
    EMISSION_TBL3:114 115 0 3 0 7
    EMISSION_TBL4:116 117 0 3 0 7
    EMISSION_TBL5:118 119 0 3 0 7
    EMISSION_TBL6:120 121 0 3 0 7
    EMISSION_TBL7:122 123 0 3 0 7
    EMISSION_TBL8:124 125 0 3 0 7
    EMISSION_TBL9:126 127 0 3 0 7
    EMISSION_TBL10:128 129 0 3 0 7
    EMISSION_TBL11:130 131 0 3 0 7
    Low Temp Value:132 132 0 7 0 7    
    '''
    def read_reg_struc_file(self, reg_struc_file ):
        REG_addr=""
        SUB_REG_name=""
        SUB_REG_name_addr=""
        with open(reg_struc_file, 'r') as file_to_read:
            while True:
                lines = file_to_read.readline() # 整行读取数据
                if not lines:
                    break
                    pass
                lines=lines.strip()
                if lines =='':
                    continue
                if lines[0]=='#':
                    continue
                if lines[0]=='/' and lines[1]=='/':
                    continue

                line_pos = lines.find("REG")
                if line_pos != -1:
                    REG_addr=lines.split('-')[1].split(':')[0]
                    continue

                if REG_addr=="":
                    continue

                SUB_REG_name,SUB_REG_name_addr=lines.split(':')[0],lines.split(':')[1]

                start_B=SUB_REG_name_addr.split()[0]
                end_B  =SUB_REG_name_addr.split()[1]
                SB_s_b =SUB_REG_name_addr.split()[2]
                SB_e_b =SUB_REG_name_addr.split()[3]
                EB_s_b =SUB_REG_name_addr.split()[4]
                EB_e_b =SUB_REG_name_addr.split()[5]

                self.reg_map[REG_addr].append([SUB_REG_name,start_B,end_B,SB_s_b,SB_e_b, EB_s_b,EB_e_b])
        pass
            

    #read code file that's similar with elecs board
    def read_reg_file( self, reg_file ):
        pass
    

if __name__ == '__main__':
    #Elecs_to(sys.argv[1])
    #p1,p2=get_src_file()
    #Compare_E7422( p1, p2 )
    #BOE_to_other(p1,p2)
    #reg_analyze()
    #factory_test()
    
    #compare the some register
    #reg_data=E7422_to_gx(sys.argv[1], ["0xCF","0xD7"])

    #r66451=reg_file("R66451","./reg_map_R66451.txt")
    #r66451.read_reg_struc_file("./reg_map_R66451.txt")
    #'''for convert Elecs to BOE
    if len(sys.argv)!=1:
        E7422_to_BOE(sys.argv[1],sys.argv[2],sys.argv[3])
    else:
        usage_E7422_to_BOE()
    #'''
    #reg_process_0xCF(reg_data)
    #reg_data=E7422_to_gx(sys.argv[1], "0xD7")
    #reg_process_0xD7(reg_data)
    #excel_to_jig_ex(sys.argv[1],"E7422") #out_type: E7422 GX
    #truly_to_gx(sys.argv[1]) #out_type: E7422 GX
    #calc_raw_image()
    #gx_to_other(sys.argv[1],"E7422")
    #satis_matrix_max_min(sys.argv[3])
    #satis_adc(sys.argv[2],"ADC",[511,255,127,63,31]) #satis_adc( filename , op_type, ADC_ERR_CONST, RT_TYPE="RT12", limit=[-9,9], tx_rx=[16,32] ):