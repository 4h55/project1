import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import schedule
import time
import xlwt
print(''' 
          模式1:按每？分钟执行一次爬取
          模式2：按每？小时执行一次爬取
          模式3：按每天的？点？分执行一次爬取
          模式4：每？小时运行，？点后停止
          ''')
#网址名
url1="https://www.bkjx.sdu.edu.cn/index/gztz.htm"
url2="https://www.bkjx.sdu.edu.cn/"
url3="http://www.youth.sdu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1004"
url4="http://www.youth.sdu.edu.cn/"
#基本的提取网页内容
def creat(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }
    request = urllib.request.Request(url=url, headers=headers, method="POST")
    response = urllib.request.urlopen(request)
    html = response.read().decode("utf-8")
    soup1 = BeautifulSoup(html, "html.parser")
    return soup1


# 提取出大致的html内容
def extract1(way):
    soup = creat(url1)
    for var in soup.find_all("div", style="float:left"):
        var = str(var)
    a = re.compile(way)
    var_s = re.findall(a, var)
    return var_s

def extract2(ways):
    soup = creat(url3)
    for vars1 in soup.find_all("div", class_="ny-right"):
        vars1 = str(vars1)
    a = re.compile(ways)
    var_ss = re.findall(a, vars1)
    return var_ss


#
def job():
    print("I'm working...")


#创建excel表
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('山大要闻', cell_overwrite_ok=True)
    worksheet1=workbook.add_sheet('山大日记', cell_overwrite_ok=True)



    #官网1
    col=('通知链接','通知发布时间','通知标题','通知内容')
    for i in range(0,len(col)):
        worksheet.write(0,i,col[i])
        worksheet1.write(0,i,col[i])
    #正则规则
    way_uurl=r'<a href="(.*)" target="_blank" title='
    way_time=r'">[(.*)]</div>'
    way_title=r'title="(.*)">'
    way_content=r'mso-font-kerning: 0.0pt;">(.*)</span>'
    #保存网址
    for i in range(0,len(extract1(way_uurl))):
        worksheet.write(i+1,0,extract1(way_uurl)[i])
    #保存时间
    for i in range(0,len(extract1(way_time))):
        worksheet.write(i+1,1,extract1(way_time)[i])
    #保存标题
    for i in range(0,len(extract1(way_title))):
        worksheet.write(i+1,2,extract1(way_title)[i])
    #提取文章内容
    list1=extract1(way_uurl)
    list1=[item for item in list1 if "ipo" not in item]
    i=0
    for j in list1:
        b=url2+j
        soup=creat(b)
        for content in soup.find_all("div",class_="Scetion1"):
            content=str(content)
        a=re.compile(way_content)
        contents=re.findall(a,content)
        contentss=re.sub(r'<[^>]+>',"",str(contents))
                    #保存内容
        worksheet.write(i+1,3,contentss)
        i+=1

    #官网2
    #正则规则
    way1_uurl = r'<a href="(.*)" target="_blank"'
    way1_time=r'<span>(.*)</span>'
    way1_title = r'target="_blank">(.*)</a>'
    way1_content=r';">(.*)</span>'
    # 保存时间
    for i in range(0,len(extract2(way1_uurl))):
        worksheet1.write(i+1,0,extract2(way1_uurl)[i])
    # 保存标题
    for i in range(0,len(extract2(way1_time))):
        worksheet1.write(i+1,1,extract2(way1_time)[i])

   # 保存网址
    for i in range(0,len(extract2(way1_title))):
        worksheet1.write(i+1,2,extract2(way1_title)[i])
    j=0
    list2=extract2(way1_uurl)

    # 提取文章内容
    for i in list2:
        b=url4+i
        soup=creat(b)
        for content1 in soup.find_all("div",class_="v_news_content"):
            content1=str(content1)
        print(content1)
        a=re.compile(way1_content)
        contents=re.findall(a,content1)
        contentss=re.sub(r'\s+\w+="[^"]*"', '',str(contents))
        # 保存内容
        worksheet1.write(j+1,3,contentss)
        j+=1

    workbook.save('山东大学官网1.xls')
#设定的若干定时爬取的模式
moudule=input("请输入你需要模式几")
if moudule == "1":
    schedule.every(int(input("请输入分钟数"))).minutes.do(job)
if moudule == "2":
    schedule.every(int(input("请输入小时数"))).hour.do(job)
if moudule == "3":
    schedule.every().day.at("11:25").do(job)
if moudule == "4":
    schedule.every(int(input("请输入小时数"))).hours.until("input('请输入：小时：分钟，如13：15代表13点15分，需要输入冒号')").do(job)

while True:
     schedule.run_pending()
     time.sleep(1)
