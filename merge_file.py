filelists = ('file1.txt','file2.txt')
with open ('file3.txt', 'w') as outfile:
     for name in filelists:
              with open (name) as infile:
                  outfile.write(infile.read())
              outfile.write("\n")