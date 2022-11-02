import vacatio as v
months = ["January","February","March","April", "May", "June", "July", "August", "September", "October", "November", "December"]
flag = 0
for month in months :
    if month == "June" or month == "July":
       if flag == 0:
        print("now",v.vacation1)
           flag = 1
    elif month == "December":
         print("now", v.vacation2)
    else:
       print("current month is month",month)
       
       