import json
import re
import random
import requests                 #接口

list=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
listcard=[['*2','*3','*4','*5','*6','*7','*8','*9','*10','*J','*Q','*K','*A'],
          ['#2','#3','#4','#5','#6','#7','#8','#9','#10','#J','#Q','#K','#A'],
          ['$2','$3','$4','$5','$6','$7','$8','$9','$10','$J','$Q','$K','$A'],
          ['&2','&3','&4','&5','&6','&7','&8','&9','&10','&J','&Q','&K','&A']]


def change(s):  #拆出每张牌
    pattern='[*#$&][0-9a-zA-Z]{1,2}'
    string=re.findall(pattern,s)
    return string
    
def put_list(card): #将牌存入list
    for item in card:
        pattern='[*#$&]|[0-9a-zA-Z]{1,2}'
        string=re.findall(pattern,item) #将花色与数字拆开
        if string[0]=='*':      #根据牌将list对应位置的值加1
            if string[1]=='A':
                list[0][13]+=1
                list[1][13]+=1
            elif string[1]=='J':
                list[0][10]+=1
                list[1][10]+=1
            elif string[1]=='Q':
                list[0][11]+=1
                list[1][11]+=1
            elif string[1]=='K':
                list[0][12]+=1
                list[1][12]+=1
            else:
                list[0][int(string[1])-1]+=1
                list[1][int(string[1])-1]+=1
            list[1][0]+=1
        
        if string[0]=='#':      #根据牌将list对应位置的值加1
            if string[1]=='A':
                list[0][13]+=1
                list[2][13]+=1
            elif string[1]=='J':
                list[0][10]+=1
                list[2][10]+=1
            elif string[1]=='Q':
                list[0][11]+=1
                list[2][11]+=1
            elif string[1]=='K':
                list[0][12]+=1
                list[2][12]+=1
            else:
                list[0][int(string[1])-1]+=1
                list[2][int(string[1])-1]+=1
            list[2][0]+=1
            
        if string[0]=='$':      #根据牌将list对应位置的值加1
            if string[1]=='A':
                list[0][13]+=1
                list[3][13]+=1
            elif string[1]=='J':
                list[0][10]+=1
                list[3][10]+=1
            elif string[1]=='Q':
                list[0][11]+=1
                list[3][11]+=1
            elif string[1]=='K':
                list[0][12]+=1
                list[3][12]+=1
            else:
                list[0][int(string[1])-1]+=1
                list[3][int(string[1])-1]+=1
            list[3][0]+=1
            
        if string[0]=='&':      #根据牌将list对应位置的值加1
            if string[1]=='A':
                list[0][13]+=1
                list[4][13]+=1
            elif string[1]=='J':
                list[0][10]+=1
                list[4][10]+=1
            elif string[1]=='Q':
                list[0][11]+=1
                list[4][11]+=1
            elif string[1]=='K':
                list[0][12]+=1
                list[4][12]+=1
            else:
                list[0][int(string[1])-1]+=1
                list[4][int(string[1])-1]+=1
            list[4][0]+=1
            
def checkFlush():       #判断同花顺
    str = []
    for i in range(1,len(list)):
        if list[i][0]>=5:
            count=0     #计算连续牌数
            t=0     #标记同花顺开始位置
            for j in range(len(list[i])-1,0,-1):
                if list[i][j]==1:
                    count+=1
                else:
                    if count>=5:
                        t=j+1
                        break
                    count=0
            if count>=5:        #存在同花顺
                if count==5:
                    for n in range(t,t+5):
                        str.append(listcard[i-1][n-1])#str为同花顺
                        list[i][n]=0
                        list[i][0] -= 1
                        list[0][n] -= 1
                else:               #同花顺大于5张时
                    m=0
                    for k in range(t+5,t+count):#避免拆炸弹、葫芦、对子
                        if list[0][k]>1:
                            m=k
                            break
                    for n in range(m-5,m):
                        str.append(listcard[i - 1][n - 1])
                        list[i][n] = 0
                        list[i][0] -= 1
                        list[0][n] -= 1
                    return str
    return str
    
def checkBomb():        #判断炸弹
    str = []
    for i in range(len(list[0])-1,0,-1):
        if list[0][i]==4:           #存在炸弹
            for n in range(1,5):
                str.append(listcard[n-1][i-1])
                list[n][i]=0
                list[n][0]-=1
                list[0][i]-=1
    return str

def check_gourd():       #判断葫芦
    str = []
    for i in range(len(list[0])-1,0,-1):
        if list[0][i]==3:           #存在三条
            str.append(i)
            break
    return str

def checkSameflower(ch):      #判断同花
    x=0
    str=[]
    for i in range(1,len(list)):
        if list[i][0]>=5:       #存在同花
            list1=[]
            if list[i][0]==5:
                for j in range(1,len(list[0])):
                    if list[i][j]==1:
                        list1.append(j)
                        if list[0][j]>1:
                             x+=1
                if x!=list[0].count(2)+list[0].count(3) or ch==0:#拆的对子、三条不等于总数，或者后墩不是葫芦
                    for item in list1:
                        str.append(listcard[i-1][item-1])   #str为同花
                        list[i][item]=0
                        list[i][0]-=1
                        list[0][item]-=1
                    return str
            else:
                count=0
                list1=[]            #存同种花色的所有牌
                for j in range(1,len(list[0])):
                    if list[i][j]==1:
                        list1.append(j)
                        count+=1
                    if count>5:
                        if list[0][j]>1:
                            break
                t = 0
                for j in range(1, 5):
                    if list[0][j] >= 5:
                        if list[0][j] >= 10:
                            for item in list1:
                                str.append(listcard[i - 1][item - 1])  # str为同花
                                list[i][item] = 0
                                list[i][0] -= 1
                                list[0][item] -= 1
                            return str
                        t += 1
                if t == 1:
                    l = len(list1) - 1
                    for x in range(l, -1, -1):
                        if list[i][list1[x]] > 1:
                            pop.list()
                        if len(list1)==5:
                            break
                else:
                    tag=0
                    for y in range(i,5):
                        if list[y][0]>=5 and y!=i:
                            for z in rangr(13,0,-1):
                                if z>list1[len(list)-1]:
                                    tag=y
                                    break
                    if tag!=0:
                        q=0
                        for y in range(13,0,-1):
                            if list[tag][y]==1:
                                str.append(listcard[tag-1][y - 1])  # str为同花
                                list[tag][y] = 0
                                list[tag][0] -= 1
                                list[0][y] -= 1
                                q+=1
                            if q==5:
                                break
                        return str

                while True:         #将同花牌数减到5张
                    if len(list1)==5:
                        break
                    list1.pop(0)
                for j in range(0,5):
                    if list[0][list1[j]] > 1:
                        x += 1

                if x<list[0].count(2)+list[0].count(3) or ch==0:#拆的对子、三条不等于总数，或者后墩不是葫芦
                    for item in list1:
                        str.append(listcard[i-1][item-1])   #str为同花
                        list[i][item]=0
                        list[i][0]-=1
                        list[0][item]-=1
                    return str
    return str

def check_order(ch):         #判断顺子
    count=0     #计算连续牌数
    t=1     #标记顺子开始位置
    str=[]
    for i in range(len(list[0])-1,0,-1):
        if list[0][i]>=1:
            count+=1
        else:
            if count>=5:
                t=i+1
                break
            count=0
    if count>=5:    #存在顺子
        if count==5:
            x=0
            for j in range(t,t+5):
                if list[0][j] > 1:
                    x += 1
            if x != list[0].count(2) + list[0].count(3) or ch == 0:  # 拆的对子、三条不等于总数，或者后墩不是葫芦
                for j in range(t,t+5):
                    for k in range(1,len(list)):
                        if list[k][j]==1:
                            str.append(listcard[k-1][j-1])  #str为顺子
                            list[k][j]=0
                            list[k][0]-=1
                            list[0][j]-=1
                            break
            return str

        else:
            x=0
            m=t+count
            for j in range(t+5,t+count):#避免拆葫芦、对子
                if list[0][j]>1:
                    m=j
                    break
            for j in range(m-5,m):
                if list[0][j] > 1:
                    x += 1
            if t+count-m>=5:
                m=t+count
            if x != list[0].count(2) + list[0].count(3) or ch == 0:  # 拆的对子、三条不等于总数，或者后墩不是葫芦
                for k in range(m-5,m):
                    for n in range(1,len(list)):
                        if list[n][k]==1:
                            str.append(listcard[n-1][k-1])
                            list[n][k]=0
                            list[n][0]-=1
                            list[0][k]-=1
                            break
            return str
    return str

def even_pair():            #判断连对
    count=0
    for i in range(13,0,-1):
        if list[0][i]==2:
            count+=1
        else:
            count=0
        if count==2:
           for j in range(1,5):
               if list[j][i+1]==1:
                   str.append(listcard[j - 1][i])
                   list[j][i+1] = 0
                   list[j][0] -= 1
                   list[0][i+1] -= 1
           for j in range(1, 5):
               if list[j][i] == 1:
                   str.append(listcard[j - 1][i - 1])
                   list[j][i] = 0
                   list[j][0] -= 1
                   list[0][i] -= 1
           return str

def double_pair():   #判断双对
    count=0     #满足两对返回
    str=[]
    for i in range(len(list[0])-1,0,-1):
        if list[0][i]==2:
            for j in range(1,5):
                if list[j][i]==1:
                    str.append(listcard[j-1][i-1])
                    list[j][i]=0
                    list[j][0]-=1
                    list[0][i]-=1
            count+=1
        if count==2:
            break
    return str
                
def simple_pair():   #判断一对
    str=[]
    for i in  range(13,0,-1):
        if list[0][i]==2:
            for j in range(1,5):
                if list[j][i]==1:
                    str.append(listcard[j-1][i-1])
                    list[j][i]=0
                    list[j][0]-=1
                    list[0][i]-=1
            return  str
    return str

def put5card(ch):          #确定中后墩
    t=-1
    str=[]
    s=[]    #判断是否存在三条
    str=checkFlush()    #判断同花顺
    if str:
        return str
    str=checkBomb()       #判断炸弹
    if str:
        return str
    str=check_gourd()      #判断葫芦
    if str:
        t=str[0]      #得到三条位置
        str=[]
        if list[0].count(2)>0 or list[0].count(3)>1:
            for n in range(1,5):
                if list[n][t]==1:
                    str.append(listcard[n - 1][t - 1])
                    list[n][t] = 0
                    list[n][0] -= 1
                    list[0][t] -= 1
            if list[0].count(2)==1:
                m=list[0].index(2)
                for i in range(1,5):
                    if list[i][m]==1:
                        str.append(listcard[i-1][m-1])
                        list[i][m]=0
                        list[i][0]-=1
                        list[0][m]-=1
            return str
    str=checkSameflower(ch)     #判断同花
    if str:
        return str
    str=check_order(ch)         #判断顺子
    if str:
        return str
    if t>=0:                #判断三条
        for i in range(1, 5):
            if list[i][t] == 1:
                str.append(listcard[i - 1][t - 1])
                list[i][t] = 0
                list[i][0] -= 1
                list[0][t] -= 1
        if len(str)==3:
            return str
        else:
            str=[]
    if str:
        return str
    if list[0].count(2)>=1:

        if list[0].count(2)>2+ch:
            str=double_pair()   #判断双对
        else:
            str=simple_pair()   #判断一对
    return str

def sort_list(str):             #将列表排序
    list0=[]
    list1=[]
    for item in str:
        pattern = '[0-9a-zA-Z]{1,2}'
        string=re.findall(pattern, item)
        pattern = '[#$*&]'
        string1=re.findall(pattern, item)
        string = ''.join(string)
        string1=''.join(string1)
        if len(string)==2:
            x='A'+string1
        else:
            if string=='A':
                x='Z'+string1
            elif string=='K':
                x='X'+string1
            else:
                x = string + string1
        list0.append(x)
    dic=dict(zip(list0,str))
    dic = sorted(dic.items(),key=lambda item:item[0])
    str=[]
    for item in dic:
        str.append(item[1])
    return str


def Biography(s): #传入传出数据
    card=change(s)
    put_list(card)
    ch=0
    str1=put5card(ch)
    if len(str1)==3:
        ch=1
    str2=put5card(ch)
    if len(str1)==3:                            #补全后墩的葫芦或三条
        count=0

        if 2 in list[0] :        #补全后墩的葫芦
            t=list[0].index(2)
            for i in range(1,5):
                if list[i][t] == 1:
                    count+=1
                    str1.append(listcard[i - 1][t - 1])
                    list[i][t] = 0
                    list[i][0] -= 1
                    list[0][t] -= 1
                if count==2 :
                    break
        elif  3 in list[0]:        #补全后墩的葫芦
            t=list[0].index(3)
            for i in range(1,5):
                if list[i][t] == 1:
                    count+=1
                    str1.append(listcard[i - 1][t - 1])
                    list[i][t] = 0.

                    list[i][0] -= 1
                    list[0][t] -= 1
                if count==2 :
                    break
        else:                                      #补全后墩的三条
            while True:
                t = list[0].index(1)
                for i in range(1, 5):
                    if list[i][t] == 1:
                        count+=1
                        str1.append(listcard[i - 1][t - 1])
                        list[i][t] = 0
                        list[i][0] -= 1
                        list[0][t] -= 1
                        break
                if count == 2:
                    break
    if  len(str1)==4:                           #补全后墩的炸弹或2条
        if 1 not in list[0]:
            for i in range(1,14):
                if list[0][i]>0:
                    for j in range(1,5):
                        if list[j][i]==1:
                            str1.append(listcard[j - 1][i - 1])
                            list[j][i] = 0
                            list[j][0] -= 1
                            list[0][i] -= 1
                            break
                    break
        else:
            t = list[0].index(1)
            for i in range(1, 5):
                if list[i][t] == 1:
                    str1.append(listcard[i - 1][t - 1])
                    list[i][t] = 0
                    list[i][0] -= 1
                    list[0][t] -= 1
                    break
    if  len(str1)==2:                           #补全后墩的1条
        z=0
        while z<3:
            t = list[0].index(1)
            for i in range(1, 5):
                if list[i][t] == 1:
                    str1.append(listcard[i - 1][t - 1])
                    list[i][t] = 0
                    list[i][0] -= 1
                    list[0][t] -= 1
                    break
            z+=1
    if str2:
        if len(str2)==3:                               #补全中墩的葫芦或三条
            count=0
            if 2 in list[0] :            #补全中墩的葫芦
                t=list[0].index(2)
                for i in range(1,5):
                    if list[i][t] == 1:
                        count+=1
                        str2.append(listcard[i - 1][t - 1])
                        list[i][t] = 0
                        list[i][0] -= 1
                        list[0][t] -= 1
                    if count==2 :
                        break
            elif 3 in list[0]:            #补全中墩的葫芦
                t=list[0].index(3)
                for i in range(1,5):
                    if list[i][t] == 1:
                        count+=1
                        str2.append(listcard[i - 1][t - 1])
                        list[i][t] = 0
                        list[i][0] -= 1
                        list[0][t] -= 1
                    if count==2 :
                        break
            else:                                       #补全后墩的三条
                while True:
                    t = list[0].index(1)
                    for i in range(1, 5):
                        if list[i][t] == 1:
                            count+=1
                            str2.append(listcard[i - 1][t - 1])
                            list[i][t] = 0
                            list[i][0] -= 1
                            list[0][t] -= 1
                            break
                    if count == 2:
                        break
        if  len(str2)==4:                       #补全中墩的炸弹或2条
            if 1 not in list[0]:
                for i in range(1, 14):
                    if list[0][i] > 0:
                        for j in range(1, 5):
                            if list[j][i] == 1:
                                str2.append(listcard[j - 1][i - 1])
                                list[j][i] = 0
                                list[j][0] -= 1
                                list[0][i] -= 1
                                break
                        break
            else:
                t = list[0].index(1)
                for i in range(1, 5):
                    if list[i][t] == 1:
                        str2.append(listcard[i - 1][t - 1])
                        list[i][t] = 0
                        list[i][0] -= 1
                        list[0][t] -= 1
                        break
        if  len(str2)==2:                           #补全后墩的1条
            z=0
            while z<3:
                t = list[0].index(1)
                for i in range(1, 5):
                    if list[i][t] == 1:
                        str2.append(listcard[i - 1][t - 1])
                        list[i][t] = 0
                        list[i][0] -= 1
                        list[0][t] -= 1
                        break
                z+=1
    else:
        z = 0
        tag=1
        for t in range(13,0,-1):
            if list[0][t]==1:
                for i in range(1, 5):
                    if list[i][t] == 1:
                        if  len(str2)==1 and tag==1:
                            tag=0
                            continue
                        str2.append(listcard[i - 1][t - 1])
                        list[i][t] = 0
                        list[i][0] -= 1
                        list[0][t] -= 1
                        z += 1
                        break

            if z==5:
                break
    string=set(card)-set(str1)-set(str2)
    str3=[]
    for x in string:
        str3.append(x)
    str1 = sort_list(str1)
    str2 = sort_list(str2)
    str3 = sort_list(str3)
    str1=' '.join(str1)
    str2 = ' '.join(str2)
    str3 = ' '.join(str3)
    str0=[str3,str2,str1]
    return str0
username="fwh"
password="lwfwh19052"
count=0
while count<100:
    list = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    url = "http://api.revth.com/auth/login"
    payload = "{\"username\":\"" + username+ "\",\"password\":\"" + password + "\"}"
    headers = {'content-type': 'application/json'}
    response = requests.request("POST", url, data=payload, headers=headers)
    d=dict(response.json())
    print(d)
    token=d["data"]["token"]
    print(token)
    headers={"X-Auth-Token":token}
    url="http://api.revth.com/game/open"
    response = requests.request("POST", url, headers=headers)
    d=dict(response.json())
    id=d["data"]["id"]
    s=d["data"]["card"]
    print(s)
    s=Biography(s)
    print(list)
    print(s)
    body={"id": id,
      "card": s}
    body=json.dumps(body)
    url="http://api.revth.com/game/submit"
    headers={"X-Auth-Token":token,'content-type': 'application/json'}
    response = requests.request("POST", url, data=str(body), headers=headers)
    d=dict(response.json())
    print(d["status"])
    print(d["data"]["msg"])
    count+=1
    print(count)
