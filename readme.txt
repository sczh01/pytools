Convert tools target:

mipi.write 0x29 0xB3 0x31 0x00 0x06           ==> U16 B3[4]={0xB3,0x31,0x00,0x06};
mipi.write 0x29 0xB4 0x31 0x00 0x06 0x09 0x09 ==> U16 B4[6]={0xB3,0x31,0x00,0x06,0x09,0x09};
||
^^
Generic_Long_Write_FIFO(4,B3);//0xB3
Generic_Long_Write_FIFO(6,B4);//0xB4


Create a new repository
git clone http://gujmVM/sczh01/py2.7.git
cd py2.7
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master



Existing folder
cd existing_folder
git init
git remote add origin http://gujmVM/sczh01/py2.7.git
git add .
git commit -m "Initial commit"
git push -u origin master



Existing Git repository
cd existing_repo
git remote add origin http://gujmVM/sczh01/py2.7.git
git push -u origin --all
git push -u origin --tags

