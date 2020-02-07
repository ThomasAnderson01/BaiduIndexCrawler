import selenium
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import COOKIES
from urllib.parse import quote
import datetime
import time

cookies = [{'name': cookie.split('=')[0],
            'value': cookie.split('=')[1]}
           for cookie in COOKIES.replace(' ', '').split(';')]

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(chrome_options=chrome_options)

def init_browser():
    """
        initialize browser
    """
# =============================================================================
#     browser.get('https://index.baidu.com/#/')
#     browser.set_window_size(1500, 900)
#     browser.delete_all_cookies()
#     for cookie in cookies:
#         browser.add_cookie(cookie)
# =============================================================================
    global browser

    # https://passport.baidu.com/v2/?login
    url = "https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F"
    # 打开谷歌浏览器
    # Firefox()
    # Chrome()
    browser = webdriver.Chrome()
    # 输入网址
    browser.get(url)
    # 打开浏览器时间
    # print("等待10秒打开浏览器...")
    # time.sleep(10)
    
    browser.find_element_by_xpath('//*[@id="TANGRAM__PSP_3__footerULoginBtn"]').click()
    # 找到id="TANGRAM__PSP_3__userName"的对话框
    # 清空输入框
    browser.find_element_by_id("TANGRAM__PSP_3__userName").clear()
    browser.find_element_by_id("TANGRAM__PSP_3__password").clear()

    # 输入账号密码
    # 输入账号密码
    account = []
    try:
        fileaccount = open("account.txt", encoding='UTF-8')
        accounts = fileaccount.readlines()
        for acc in accounts:
            account.append(acc.strip())
        fileaccount.close()
    except Exception as err:
        print(err)
        input("请正确在account.txt里面写入账号密码")
        exit()
    browser.find_element_by_id("TANGRAM__PSP_3__userName").send_keys(account[0])
    browser.find_element_by_id("TANGRAM__PSP_3__password").send_keys(account[1])

    # 点击登陆登陆
    # id="TANGRAM__PSP_3__submit"
    browser.find_element_by_id("TANGRAM__PSP_3__submit").click()

    # 等待登陆10秒
    # print('等待登陆10秒...')
    # time.sleep(10)
    print("等待网址加载完毕...")

    select = input("请观察浏览器网站是否已经登陆(y/n)：")
    while 1:
        if select == "y" or select == "Y":
            print("登陆成功！")
            print("准备打开新的窗口...")
            # time.sleep(1)
            # browser.quit()
            break

        elif select == "n" or select == "N":
            selectno = input("账号密码错误请按0，验证码出现请按1...")
            # 账号密码错误则重新输入
            if selectno == "0":

                # 找到id="TANGRAM__PSP_3__userName"的对话框
                # 清空输入框
                browser.find_element_by_id("TANGRAM__PSP_3__userName").clear()
                browser.find_element_by_id("TANGRAM__PSP_3__password").clear()

                # 输入账号密码
                account = []
                try:
                    fileaccount = open("../baidu/account.txt", encoding='UTF-8')
                    accounts = fileaccount.readlines()
                    for acc in accounts:
                        account.append(acc.strip())
                    fileaccount.close()
                except Exception as err:
                    print(err)
                    input("请正确在account.txt里面写入账号密码")
                    exit()

                browser.find_element_by_id("TANGRAM__PSP_3__userName").send_keys(account[0])
                browser.find_element_by_id("TANGRAM__PSP_3__password").send_keys(account[1])
                # 点击登陆sign in
                # id="TANGRAM__PSP_3__submit"
                browser.find_element_by_id("TANGRAM__PSP_3__submit").click()

            elif selectno == "1":
                # 验证码的id为id="ap_captcha_guess"的对话框
                input("请在浏览器中输入验证码并登陆...")
                select = input("请观察浏览器网站是否已经登陆(y/n)：")
        else:
            print("请输入“y”或者“n”！")
            select = input("请观察浏览器网站是否已经登陆(y/n)：")

def get_into_page(keyword):
    """
        get baiduIndex page
    """
    # 这里开始进入百度指数
    # 新开一个窗口，通过执行js来新开一个窗口
    js = 'window.open("http://index.baidu.com");'
    browser.execute_script(js)
    # 新窗口句柄切换，进入百度指数
    # 获得当前打开所有窗口的句柄handles
    # handles为一个数组
    handles = browser.window_handles
    # print(handles)
    # 切换到当前最新打开的窗口
    browser.switch_to_window(handles[-1])
    # 在新窗口里面输入网址百度指数
    # 清空输入框
    time.sleep(5)
    #browser.find_element_by_id("search-input-form").clear()
    browser.find_element_by_xpath('//*[@id="search-input-form"]/input[3]').clear()
    # 写入需要搜索的百度指数
    #browser.find_element_by_id("search-input-form").send_keys(keyword)
    browser.find_element_by_xpath('//*[@id="search-input-form"]/input[3]').send_keys(keyword)
    # 点击搜索
    # <input type="submit" value="" id="searchWords" onclick="searchDemoWords()">
    browser.find_element_by_xpath('//*[@id="home"]/div[2]/div[2]/div/div[1]/div/div[2]/div/span').click()
    time.sleep(5)
    # 最大化窗口
    browser.maximize_window()
    
    
    
    

def get_time_range_list(startdate, enddate):
    """
    max 6 months
    """
    date_range_list = []
    startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    while 1:
        tempdate = startdate + datetime.timedelta(days=300)
        if tempdate >= enddate:
            all_days = (enddate-startdate).days
            date_range_list.append((startdate, enddate, all_days+1))
            return date_range_list
        date_range_list.append((startdate, tempdate, 301))
        startdate = tempdate + datetime.timedelta(days=1)

    

def adjust_time_range(startdate, enddate, kind):
    """
        ...
    """
    time.sleep(2)
    #browser.find_elements_by_xpath('//*[@class="index-date-range-picker"]')[kind].click()
    
    browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div/div[1]').click()
    base_node = browser.find_element_by_xpath('//*[contains(@class, "index-date-range-picker-overlay-box") and \
        contains(@class, "tether-enabled")]')
    select_date(base_node, startdate)
    end_date_button = base_node.find_elements_by_xpath('.//*[@class="date-panel-wrapper"]')[1]
    end_date_button.click()
    select_date(base_node, enddate)

    base_node.find_element_by_xpath('.//*[@class="primary"]').click()
    time.sleep(1)

def select_date(base_node, date):
    """
        select date
    """
    time.sleep(2.5)
    base_node = base_node.find_element_by_xpath('.//*[@class="right-wrapper" and not(contains(@style, "none"))]')
    next_year = base_node.find_element_by_xpath('.//*[@aria-label="下一年"]')
    pre_year = base_node.find_element_by_xpath('.//*[@aria-label="上一年"]')
    next_month = base_node.find_element_by_xpath('.//*[@aria-label="下个月"]')
    pre_month = base_node.find_element_by_xpath('.//*[@aria-label="上个月"]')
    cur_year = base_node.find_element_by_xpath('.//*[@class="veui-calendar-left"]//b').text
    cur_month = base_node.find_element_by_xpath('.//*[@class="veui-calendar-right"]//b').text
    diff_year = int(cur_year) - date.year
    diff_month = int(cur_month) - date.month
    if diff_year > 0:
        for _ in range(abs(diff_year)):
            pre_year.click()
    elif diff_year < 0:
        for _ in range(abs(diff_year)):
            next_year.click()

    if diff_month > 0:
        for _ in range(abs(diff_month)):
            pre_month.click()
    elif diff_month <0:
        for _ in range(abs(diff_month)):
            next_month.click()

    time.sleep(1)
    base_node.find_elements_by_xpath('.//table//*[contains(@class, "veui-calendar-day")]')[date.day-1].click()

def loop_move(all_days, keyword, kind):
    """
        to get the index by moving mouse
    """
    time.sleep(1)
    chart = browser.find_elements_by_xpath('//*[@class="index-trend-chart"]')[kind]
    chart_size = chart.size
    move_step = all_days - 1
    step_px = chart_size['width'] / move_step
    cur_offset = {
        'x': step_px,
        'y': chart_size['height'] - 50
    }

    webdriver.ActionChains(browser).move_to_element_with_offset(
        chart, 1, cur_offset['y']).perform()
    yield get_index(keyword, chart)

    for _ in range(all_days-1):
        time.sleep(0.05)
        webdriver.ActionChains(browser).move_to_element_with_offset(
            chart, int(cur_offset['x']), cur_offset['y']).perform()
        cur_offset['x'] += step_px
        yield get_index(keyword, chart)

def get_index(keyword, base_node):
    """
        get index datas by html
    """
    date = base_node.find_element_by_xpath('./div[2]/div[1]').text
    date = date.split(' ')[0]
    index = base_node.find_element_by_xpath('./div[2]/div[2]/div[2]').text
    index = index.replace(',', '').strip(' ')
    result = {
        'keyword': keyword,
        'date': date,
        'index': index,
    }
    return result

def main(keyword, startdate, enddate, kind=0):
    """
        搜索指数最早的数据日期为2011-01-01
    """
    init_browser()
    get_into_page(keyword)
    if kind == 1:
        ignore_baidu_index_bug()

    date_range_list = get_time_range_list(startdate, enddate)
    for startdate, enddate, all_days in date_range_list:
        adjust_time_range(startdate, enddate, kind)
        for data in loop_move(all_days, keyword, kind):
            yield data
    browser.quit()


