'readTextFile.py -- read and display text file '

#get file name
fname = raw_input('enter file name:')
print
#attempt to open file for reading
try:
    fobj = open(fname,'r')
except IOError,e:
    print '*** file open error:',e
else:
    #display contents to the screen
    for line in fobj:
        print line
    fobj.close()
