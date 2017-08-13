#-*- coding:utf8 -*-
import random

def get_random_phone_number():
        num_header = "1"+random.choice(["3", "5"]) + str(random.randint(0, 9))
        num_area = str(random.randint(1000, 9999))
        num_tail = str(random.randint(1000, 9999))
        phone_number = num_header + num_area + num_tail
        return phone_number

a = get_random_phone_number()
print a