filepath = 'c:\\anil\\python\\input.txt'
with open (filepath, 'r') as file:
     line = file.readline()
     cnt = 1
     while line:
         print ("Line {} : {}". format(cnt,line.strip()))
         line = file.readline()
         cnt += 1


