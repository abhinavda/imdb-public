from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time,bs4,requests,re,sys,os
from youtubesearch import youtube_search

## for docker container
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
driver = os.path.join("/usr/local/bin/chromedriver")
browser = webdriver.Chrome(executable_path=driver,chrome_options=chrome_options)

broswer_url="https://www.imdb.com/user/"+str(sys.argv[2])+"/watchlist"
# for command line
#browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(broswer_url)
time.sleep(3)


def click_if_button_exists():
    try :
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        python_button=browser.find_element_by_xpath("//*[@id='center-1-react']/div/div[3]/div[2]/button/span[2]")
        python_button.click()
        return True
    except NoSuchElementException:
        return False


count = 2
while click_if_button_exists():
    time.sleep(2)
    count_value = str(9000*count)
    execute_script_browser="window.scrollTo(document.body.scrollHeight,"+count_value+");"
    browser.execute_script(str(execute_script_browser))
    count+=1

html = browser.page_source
soup = bs4.BeautifulSoup(html,"html.parser")
cont = soup.find_all('div')

titles= re.split(r'("titles":)',str(cont))[2]
titlearr=[]

title1 = re.split(r'ref_=wl_li_tt">',str(titles)[1:])
for x in range(len(title1))[1:] :
    y = title1[x].split("</a>")
    year_1=re.split(r'\$\=10\"\>',y[1]) ##retrieving year
    year_2 = re.split(r'</span><span', year_1[1])[0]  ##retreiving year
    movie = y[0]
    if year_2[-1]=="-" :
        year=year_2[:-1]
    else :
        year = year_2
    final_key=movie+" "+year
    titlearr.append(final_key)
browser.close()
print "browser is closed."
# for yy in titlearr :
#     print yy
#print len(titlearr)
### Calling Youtube API here
video_ids=""
count=0   ##divide by 50

results=[]
#for x in range(len(titlearr)) : ##selecting next 50  ##Only 50 videos allowed by youtube per play_list ? :|
for x in range(10):
    print titlearr[x]
    if count%50==0 and count!=0: ## 0%50 gives 0
        results.append(video_ids)
        video_ids=""
    id = youtube_search(titlearr[x],sys.argv[1]) ## Using YT API to get video_id
    video_ids = str(video_ids) + str(id) + ","
    # if x == len(titlearr)-1 :  ## On the last video, just append it to final resulst array
    if x == 9 :
        print "hello !!"
        results.append(video_ids)
    count+=1
for yy in results :
    print "http://www.youtube.com/watch_videos?video_ids="+yy[:-1]
