import os
for file in os.scandir("/anil"):
    if file.stat().st_size > 100000000:
       print ("{:<55} {:<15} is file". format(file.name,file.stat().st_size))
