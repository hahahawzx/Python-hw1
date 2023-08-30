def get_url(num:int):
    flag = 0
    time = 1693065600 + 86400
    day = 28
    month = 8
    page = 1
    url_list_2 = set()
    while len(url_list_2)<num:
        day = day - 1
        time = time - 86400
        if day == 0:
            month = month - 1
            if month ==7 or month == 5 or month ==3 or month ==1:
                day = 31
            elif month == 6 or month ==4:
                day =30
            elif month ==2:
                day = 28
            else:
                print("2023一年的过完了")
                break
        page = 0
        print(f"正在爬2023-0{month}-{day}的消息")
        while True:
            page = page+1
            url_data = f"https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2515&etime={time - 86400}&stime={time}&ctime={time}&date=2023-0{month}-{day}&k=&num=50&page=1&r=0.28122078933743455&callback=jQuery1112020761369332467994_1693206645292&_=1693206645293"
            print(url_data)
            response=requests.get(url_data,headers_1)
            if response.status_code == 200: 
                patterns = r'"url":"(https:\\\/\\\/finance.sina.com.cn\\\/tech\\\/[^"]+\.shtml)"'
                matches = re.findall(patterns, response.text)
                for match in matches:
                    match=match.replace("\\","")
                    url_list_2.add(match)
            else:
                print("there is wrong")
                break
            if flag == len(url_list_2):
                print("没有爬取到新东西")
                break
            else:
                flag = len(url_list_2)
                print(flag)
    return url_list_2            
url =  get_url(6000)   
with open('url_tech.txt', 'w') as file:
    for item in url:
        file.write(str(item) + '\n')   
