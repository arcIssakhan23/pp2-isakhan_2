from datetime import datetime, timedelta



#1
print("==================================================================")
current = datetime.today()
fivedaysago = (current - timedelta(days=5)).date()
print(fivedaysago)



#2
current = datetime.today()
today = current.date()
tommorow = (current + timedelta(days=1)).date()
yesterday = (current - timedelta(days=1)).date()
print("==================================================================")
print(yesterday)
print(today)
print(tommorow)
print("==================================================================")




#3
cur = datetime.now()
withoutmicrosec = cur.replace(microsecond=0)
print(withoutmicrosec)



#4
print("==================================================================")

date1 = datetime.strptime(input(), "%Y-%m-%d %H:%M:%S")
date2 = datetime.strptime(input(), "%Y-%m-%d %H:%M:%S")

print((date2 - date1).total_seconds())


#for example: 
# 2024-01-01 12:00:00
# 2024-01-01 12:00:30
# output:
# 30.0