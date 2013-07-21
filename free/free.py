'''
Created on Apr 12, 2013

@author: hill
'''



possibilities=[18,21,36]

for i in range(11,100):
    temp_poss=[]
    result=[]
    for j in range(0,i):
        tmp=int(float(j)/float(i) * 100)
        
        #print tmp,j,i
        for k in possibilities:
            if k == tmp:
                result.append(j)
                temp_poss.append((float(j)/float(i)))       
                         
    if len(result) == 3:
        print i
        print result
        print temp_poss
    else:
        result=[] 
        temp_poss=[]
