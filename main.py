# -*- coding: utf-8 -*-
# author：gobyto
#20220918fix
import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By #导入by方法

def sort_file():
    # 排序文件
    dir_link = base_path
    dir_lists = list(filter(check_file, os.listdir(dir_link)))
    if len(dir_lists) == 0:
        return ''
    else:
        dir_lists.sort(key=lambda fn: os.path.getmtime(dir_link + os.sep + fn))
        return os.path.join(base_path, dir_lists[-1])


def check_file(filename):
    # 忽略系统文件
    if filename == '.DS_Store' or filename == 'thumbs.db':
        return False
    global base_path
    # 排除文件夹
    return os.path.isfile(os.path.join(base_path, filename))


def download_drivers(url):
    global base_path
    profile = {
        'download.prompt_for_download': False, 'download.default_directory': base_path,
        }
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.prompt_for_download': False, 'download.default_directory': r'F:\ok\0915\drivers', }
    chrome_options.add_experimental_option('prefs', profile)
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': base_path}}
    driver.execute("send_command", params)
    driver.implicitly_wait(10)
    driver.get(url)
    driver_lists = driver.find_elements(By.CLASS_NAME, 'dlist-item')
    for driver_list in driver_lists:
        # 提取中文及英文字母C:\Program Files\Google\Chrome\Application\chrome.exe
        title = ''.join(re.findall(r'[\u4e00-\u9fa5a-zA-Z]+', driver_list.text))
        temp_path = r'F:/ok/0915/drivers/' + title
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)
        driver_list.find_element(By.CLASS_NAME, 'download-center_list_t_icon').click()
        sub_lists = driver_list.find_elements(By.TAG_NAME, 'tr')
        for sub_list in sub_lists:
            try:
                if sub_list.find_element(By.CLASS_NAME, 'download-center_usblist_td01').text == '驱动名称':
                    continue
                else:
                    sub_title = sub_list.find_element(By.CLASS_NAME, 'download-center_usblist_td01').\
                        find_element(By.TAG_NAME, 'a').get_attribute('title').replace('/', '_')
                    print('开始下载:' + sub_title)
                    sub_list.find_element(By.LINK_TEXT, '普通下载').click()
                    # 等待开始下载
                    time.sleep(2)
                    while True:
                        oldname = sort_file()
                        file_type = oldname.split('.')[-1]
                        if oldname != '' and file_type != 'crdownload':
                            print('下载已完成')
                            break
                        else:
                            print("等待下载。。。")
                            time.sleep(10)
                    newnamne = temp_path + os.sep + sub_title + '.' + file_type
                    os.rename(oldname, newnamne)
                    print('归档成功')
            except Exception as e:
                print(e)
                continue
    print('下载结束')
    driver.quit()


if __name__ == '__main__':
    base_path = r'F:\ok\0915\drivers'
    if not os.path.exists(base_path):
        os.mkdir(base_path)
        print('创建drivers文件夹')
    # T470s win10 64bit
    url = "https://think.lenovo.com.cn/support/driver/newdriversdownlist.aspx?categoryid=12832&CODEName=ThinkPad%20T470s&SearchType=1&wherePage=1&SearchNodeCC=ThinkPad%20T470s"
    # T470s win7 64bit
    #url = 'https://think.lenovo.com.cn/support/driver/newdriversdownlist.aspx?categoryid=12832&CODEName=ThinkPad%20T470s&SearchType=1&wherePage=1&SearchNodeCC=ThinkPad%20T470s&osid=26'
    # T460s win10 64bit
    # url = 'https://think.lenovo.com.cn/support/driver/newdriversdownlist.aspx?yt=pt&categoryid=12358&CODEName=ThinkPad%20T460s&SearchType=0&wherePage=2&osid=42'
    # T460s win7 64bit
    # url = 'https://think.lenovo.com.cn/support/driver/newdriversdownlist.aspx?yt=pt&categoryid=12358&CODEName=ThinkPad%20T460s&SearchType=0&wherePage=2&osid=26'
    # T450s win10 64bit
    # url = 'https://think.lenovo.com.cn/support/driver/newdriversdownlist.aspx?yt=pt&categoryid=12002&CODEName=ThinkPad%20T450s&SearchType=0&wherePage=2&osid=42'
    download_drivers(url)
