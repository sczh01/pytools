import datetime 

def anagramSolution1(s1,s2):
    if len(s1) != len(s2):
        return False

    alist = list(s2)
    pos1 = 0
    stillOK = True
    while pos1 < len(s1) and stillOK:
        pos2 = 0
        found = False
        while pos2 < len(alist) and not found:
            if s1[pos1] == alist[pos2]:
                found = True
            else:
                pos2 = pos2 + 1
        if found:
            alist[pos2] = None
        else:
            stillOK = False
            break

        pos1 = pos1 + 1
    return stillOK

#print(anagramSolution1('abcd','dcba'))
def anagramSolution2(s1,s2):

    if len(s1) != len(s2):
        return False

    alist1 = list(s1)
    alist2 = list(s2)

    alist1.sort()
    alist2.sort()

    pos = 0
    matches = True

    while pos < len(s1) and matches:
        if alist1[pos]==alist2[pos]:
            pos = pos + 1
        else:
            matches = False
            break

    return matches

#print(anagramSolution2('abcde','edcba'))

def anagramSolution3(s1,s2):
    c1 = [0]*26
    c2 = [0]*26

    for i in range(len(s1)):
        pos = ord(s1[i])-ord('a')
        c1[pos] = c1[pos] + 1

    for i in range(len(s2)):
        pos = ord(s2[i])-ord('a')
        c2[pos] = c2[pos] + 1

    j = 0
    stillOK = True
    while j<26 and stillOK:
        if c1[j]==c2[j]:
            j = j + 1
        else:
            stillOK = False
            break

    return stillOK

def anagramSolution4(s1,s2):
    cnt1=cnt2=1
    
    for i in range(len(s1)):
        cnt1 *= (ord(s1[i])-90)
        cnt2 *= (ord(s2[i])-90)

    return cnt1 == cnt2


def time_1(s1,s2,cnt): 
    begin = datetime.datetime.now() 
    sum = 0
    for i in range(cnt): 
        anagramSolution1(s1,s2)
    end = datetime.datetime.now() 
    return end-begin

def time_2(s1,s2,cnt): 
    begin = datetime.datetime.now() 
    sum = 0 
    for i in range(cnt):
        anagramSolution2(s1,s2)
    end = datetime.datetime.now() 
    return end-begin

def time_3(s1,s2,cnt): 
    begin = datetime.datetime.now() 
    sum = 0 
    for i in range(cnt): 
        anagramSolution3(s1,s2)
    end = datetime.datetime.now() 
    return end-begin

def time_4(s1,s2,cnt): 
    begin = datetime.datetime.now() 
    sum = 0 
    for i in range(cnt): 
        anagramSolution4(s1,s2)
    end = datetime.datetime.now() 
    return end-begin

if __name__ == '__main__':
    print(time_1("anagramSolutioanagramSolutio","anagramSolutioanagramSolutio",1000))
    print(time_2("anagramSolutioanagramSolutio","anagramSolutioanagramSolutio",1000))
    print(time_3("anagramSolutioanagramSolutio","anagramSolutioanagramSolutio",1000))
    print(time_4("anagramSolutioanagramSolutio","anagramSolutioanagramSolutio",1000))
#import cProfile 
#cProfile.run('time_1()')