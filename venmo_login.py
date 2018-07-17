from time import sleep
from selenium import webdriver

import os

if not 'venmo_username' in os.environ:
    print('venmo_username not set in environment')
    exit()

if not 'venmo_password' in os.environ:
    print('venmo_password not set in environment')
    exit()


def login():
    url = 'https://venmo.com/account/sign-in'
    username = os.environ['venmo_username']
    password = os.environ['venmo_password']

    opts = webdriver.ChromeOptions()
    opts.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=opts)
    
    driver.get(url)
    sleep(1.5)

    username_in = driver.find_element_by_xpath('//*[@id="content"]/div/div/form/fieldset/label/input')
    password_in = driver.find_element_by_xpath('//*[@id="content"]/div/div/form/fieldset/div/label/input')

    username_in.send_keys(username)
    password_in.send_keys(password)
    driver.find_element_by_xpath('//*[@id="content"]/div/div/form/div/button').click()

    sleep(1.5)
    send_code_btn = driver.find_element_by_xpath('//*[@id="content"]/div/div/div/form/button')
    send_code_btn.click()

    sleep(1.5)
    code_in = driver.find_element_by_xpath('//*[@id="content"]/div/div/div/form/fieldset/label/input')

    print('Enter your code: ')
    code = input()
    code_in.send_keys(code)

    sub_code_btn = driver.find_element_by_xpath('//*[@id="content"]/div/div/div/form/div/button')
    sub_code_btn.click()

    sleep(1.5)
    nrem_btn = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div/div/form/div/button[2]')
    nrem_btn.click()

    sleep(2)
    return driver