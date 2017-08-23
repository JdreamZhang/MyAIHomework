
print "hello"

list =[1,2,3,4,5]
list2=[9,2,0,6,11,8,4,7,1,5,10,3]

"""
for i in list:
    print i
for i in range(0,len(list)-1):
	for j in range (i+1, len(list)):
		print "i: ",i
		print "j:", j
"""

for i in range(0,len(list2)-1):
	for j in range(i+1, len(list2)):
		if list2[i]>list2[j]:
			temp=list2[j]
			list2[j]=list2[i]
			list2[i]=temp
print list2