#coding=UTF-8 
class TestClass:  
    def sub(self,a,b):  
        return a-b  
    def add(self,a,b):  
        return a+b  
    def chen(self,a,b):  
        return a*b  

class TestClassA:  
    def sub(self,a,b):  
        return a-b  
    def add(self,a,b):  
        return a+b  
    def chen(self,a,b):  
        return a*b  

class TestClassB:  
    def sub(self,a,b):  
        return a-b  
    def add(self,a,b):  
        return a+b  
    def chen(self,a,b):  
        return a*b  


sys_config={}  
sys_config["01"]=['mytest','TestClassA','add']  
sys_config["02"]=['mytest','TestClassA','sub']  
sys_config["03"]=['mytest','TestClassA','chen']  
sys_config["04"]=['mytest','TestClassB','add']  
sys_config["05"]=['mytest','TestClassB','sub']  
sys_config["06"]=['mytest','TestClassB','chen']  

def main():
    class_name = "TestClass" #类名  
    module_name = "mytest"   #模块名  
    method = "chen"          #方法名  

    module = __import__(module_name) # import module  
    print "#module:",module  
    c = getattr(module,class_name)    
    print "#c:",c  
    obj = c() # new class  
    print "#obj:",obj  
    print(obj)  
    obj.chen(2,3)  
    mtd = getattr(obj,method)  
    print "#mtd:",mtd  
    print mtd(2,3) # call def  

    mtd_add = getattr(obj,"add")  
    t=mtd_add(1,2)  
    print "#t:",t  

    mtd_sub = getattr(obj,"sub")  
    print mtd_sub(2,1)  


    ywdm='02'  

    my_module_name=sys_config[ywdm][0]  
    my_class_name=sys_config[ywdm][1]  
    my_method_name=sys_config[ywdm][2]  

    my_module = __import__(my_module_name)  
    my_class = getattr(my_module,my_class_name)   
    my_obj = my_class()   
    my_method = getattr(my_obj,my_method_name)  

    print my_method(5,2)  
if __name__ == '__main__': 
    main()  