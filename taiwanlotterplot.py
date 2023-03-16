"""
爬取台灣彩券上大樂透的開講號碼(靜態)
URL: https://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx
輸出結果為圖表
"""

import requests
from bs4 import BeautifulSoup as Soup
import matplotlib.pyplot as plt
import matplotlib


URL = "https://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx"
htmlfile = requests.get(URL)
bsoup = Soup(htmlfile.text,"lxml")                  #使用BeautifulSoup解析html

result = dict()                                     #儲存期號及開獎號碼的dict
#篩選出各期開獎結果的內容
table = bsoup.find('table',id = 'Lotto649Control_history_dlQuery')\
    .find_all('table',['table_org td_hm','table_gre td_hm'])
#利用for迴圈將各期的期號及開講號碼插入dict裡,即 {期號 : 開講號碼,...}
for i in range(len(table)):
    key = table[i].find('span',id = 'Lotto649Control_history_dlQuery_L649_DrawTerm_'+str(i)).text
    temp = {key:[]}
    for j in range(1,7):
        temp[key].append(int(table[i].find('span',id = 'Lotto649Control_history_dlQuery_SNo'+str(j)+'_'+str(i)).text))
    result.update(temp)
keys = list(result.keys())                          #取得dict裡的所有key並存入list中



pltlist = list()                                    #儲存開獎號碼的list
count = list()                                      #儲存號碼出現次數的list,作為圖表的y軸

for i in range(len(keys)):
    print(f'{keys[i]}期開獎號碼：{result[keys[i]]}')  #印出各期的號碼供檢視
    for j in result[keys[i]]:
        pltlist.append(j)   #將號碼插入list裡面

#使用for迴圈計算各號碼在pltlist裡出現的次數
for i in set(pltlist):  
    count.append(pltlist.count(i))  
pltlist = list(set(pltlist))    #利用set(pltlist)方法來移除重複並進行排序,可作為圖表的x軸

#使用matplotlib繪製plot圖
fig = plt.figure(figsize=(16,9))                        #設定圖表的比例為16:9
plot = plt.plot(pltlist,count,"o-",ms = 8,color = 'cornflowerblue')
plt.title('Taiwan Lotto number count',fontsize = 24)    #圖表標題(fontsize為字體大小)
plt.xlabel('Number',fontsize = 18)                      #x軸標題
plt.ylabel('Time',fontsize = 18)                        #y軸標題
plt.xticks(range(0,51,1))                               #x軸座標範圍及間隔
plt.yticks(range(0,max(count)+2,1))                     #y軸座標範圍及間隔                          
plt.show()                                              #顯示圖表
fig.savefig('plot.png',dpi = 480)                       #儲存圖表為plot.png