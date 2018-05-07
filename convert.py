import numpy as np
import re

pos = []
Efield = []
line_pos = 0
line_use =""
def open_file( filename ):
    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
                break
                pass
            lines=lines.strip()
            if lines[0]=='#':
                continue
            line_pos = lines.find("mipi.write")
            if line_pos != -1:
                line_use = lines[line_pos:]
            else:
                continue

            p_tmp, E_tmp = [int(i) for i in lines.split()] # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
            pos.append(p_tmp)  # 添加新读取的数据
            Efield.append(E_tmp)
            pass
        pos = np.array(pos) # 将数据从list类型转换为array类型。
        Efield = np.array(Efield)
        pass

if __name__ == '__main__':
    import sys
    import getopt
    open_file(sys.argv[1])