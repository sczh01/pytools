import os,sys;

def reportSingleFile(srcfile, basefile, rpt=''):
    src = file(srcfile).read().split(' ')
    base = file(basefile).read().split(' ')
    import difflib
    s = difflib.SequenceMatcher( lambda x: len(x.strip()) == 0, # ignore blank lines
                                        base, src) 
    
    lstres = []
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        print (tag, i1, i2, j1, j2)
        #print lstres
        if tag == 'equal':
            pass
        elif  tag == 'delete' : 
            lstres.append('DELETE (line: %d)' % i1)
            lstres += base[i1:i2]
            lstres.append(' ')
        elif tag == 'insert' :    
            lstres.append('INSERT (line: %d)' % j1)
            lstres += src[j1:j2]
            lstres.append(' ')
        elif tag == 'replace' :    
            lstres.append('REPLACE:')
            lstres.append('Before (line: %d) ' % i1)
            lstres += base[i1:i2]
            lstres.append('After (line: %d) ' % j1)
            lstres += src[j1:j2]
            lstres.append(' ')
        else:
            pass
    print ' '.join(lstres)

if __name__ == '__main__':
    reportSingleFile(sys.argv[2],sys.argv[1])