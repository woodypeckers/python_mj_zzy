#!/usr/bin/env python
# encoding:utf-8
# author:mj
import unittest
from selenium import webdriver

def Bugfree_Login(driver, admin, passwd):
    driver.find_element_by_id("LoginForm_username").clear
    driver.find_element_by_id("LoginForm_username").send_keys(admin)
    driver.find_element_by_id("LoginForm_username").clear
    driver.find_element_by_id("LoginForm_password").send_keys(passwd)
    driver.find_element_by_id("SubmitLoginBTN").click()

