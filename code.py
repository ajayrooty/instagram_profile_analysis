from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import time
import os
import datetime
from webdriver_manager.chrome import ChromeDriverManager

account_name=input("enter the account name you want to scan")

count = 100
account = account_name
page=["followers","following"]

yourusername = input("enter your username") #your Instagram username
yourpassword = input("enter your password")  #your Instagram password


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57"')

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get('https://www.instagram.com/accounts/login/')
sleep(3)
username_input = driver.find_element_by_css_selector("input[name='username']")
password_input = driver.find_element_by_css_selector("input[name='password']")
username_input.send_keys(yourusername)
password_input.send_keys(yourpassword)
login_button = driver.find_element_by_xpath("//button[@type='submit']")
login_button.click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Not Now')]"))).click()
sleep(3)

driver.get('https://www.instagram.com/%s' % account)
sleep(2)

for running_method in page:
    print(running_method)

    driver.find_element_by_xpath('//a[contains(@href, "%s")]' % running_method).click()
    if(running_method=="followers"):
        method_count=driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span')
    elif(running_method=="following"):
        method_count=driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span')

    if(running_method=="followers"):
        scr2 = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
    elif(running_method=="following"):
        scr2 = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a')

    sleep(2)
    text1 = scr2.text
    no1=method_count.text
    print(text1)
    x = datetime.datetime.now()
    print(x)
    no_of_people=int(no1)
    if(running_method=="followers"):
        no_of_followers=no_of_people
    elif(running_method=="following"):
        no_of_following=no_of_people

    for i in range(1,no_of_people+1):
        scr1 = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/ul/div/li[%s]' % i)
        driver.execute_script("arguments[0].scrollIntoView();", scr1)
        sleep(1)
        text = scr1.text
        list = text.encode('utf-8').split()
        dirname = os.path.dirname(os.path.abspath(__file__))
        csvfilename = os.path.join(dirname, account + "-" + running_method + ".txt")
        file_exists = os.path.isfile(csvfilename)
        f = open(csvfilename,'a')
        string_literal=list[0]
        convert_string_literal=string_literal.decode('utf-8')
        f.write(convert_string_literal + "\r\n")
        f.close()
        if(i==no_of_people):
            close_it=driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button")
            close_it.click()

print("DONE EXTRACTING THE FOLLOWERS AND FOLLOWING")

""" NOW WE GONNA SEE WHO FOLLOWED YOU AND DIDN'T FOLLOW BACK  """

followers_list=[]
following_list=[]

with open(f"{account}-following.txt") as read_following:
    for j in range(1,no_of_following):
        for k in read_following:
            following_list.append(k.rstrip('\n'))
    read_following.close()

with open(f"{account}-followers.txt","r") as read_followers:
    for j in range(1,no_of_followers):
        for k in read_followers:
            followers_list.append(k.rstrip('\n'))
    read_followers.close()

def common_member(a, b): 
    a_set = set(a) 
    b_set = set(b) 
  
    if (a_set & b_set): 
        print(a_set & b_set) 
    else: 
        print("No common members")


not_followed_you_back_list = following_list.copy()


def not_followed_you(a,b):
    for i in following_list:
        for j in followers_list:
            if(i==j):
                not_followed_you_back_list.remove(i)
    return not_followed_you_back_list

not_followed_you_back_list=not_followed_you(followers_list,following_list)

notfollowedbackdetails = open("notfollowedbacklist.txt", "w")
for i in not_followed_you_back_list:
    notfollowedbackdetails.write(f"{i}\n")
notfollowedbackdetails.close()
