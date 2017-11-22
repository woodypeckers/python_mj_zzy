#!/usr/bin/env python
# encoding:utf-8

"""
filter,reduce,map 的例子
"""
list1 = [1, 2, 3, 4, 5, 6]
list2 = reduce(lambda x, y: x+y, list1)
print list1, list2
#filter 相当于列表推导,list comprehension
#filter(fun,iterable)

#reduce(fun,sequence[,initial_val])
"""reduce函数有三个参数，第一个参数就是作用函数，第二个函数就是可迭代的对象，第三个是迭代初始值。 
reduce函数有三个参数，第一个参数就是作用函数，第二个函数就是可迭代的对象，第三个是迭代初始值。
如果存在第三个参数，也就是有初始迭代对象，那么 initial_val作为fun函数的第一个参数， sequence 的第一个元素作为fun的第二个参数，得到返回结果的作为下一次函数的第一个参数，sequence的第二个参数作为下一次迭代过程中的第二个参数，以此类推。
如果不存在第三个参数，那么sequence的第一个参数作为fun函数的第一个参数，sequence的第二个参数作为fun函数第二个参数，以此类推。"""
str="an apple a banana three apple a desk"
list_a=str.split(' ')
def fun(x,y):
    if y in x:
        x[y]=x[y]+1
    else:
        x[y]=1
    return x
result=reduce(fun,list_a,{})
#输出结果是{'a': 2, 'apple': 2, 'three': 1, 'an': 1, 'desk': 1, 'banana': 1}


"""filter
filter 函数会对指定序列执行过滤操作，filter(function or None, sequence) -> filter object (list, tuple, or string in 2.x)
filter 函数会对序列参数 sequence 中的每个元素调用 function 函数，最后返回的结果包含调用结果为True的元素"""
def is_Even(i):
	if (i%2)==0:
		return True
	else:
		return False
		
l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
l = filter(is_Even,l)
print type(l)
print(l)                                    # 3.x版本 返回的是对象 filter object
#ll = list(l)                               # 3.x版本 须做类型转换                    
#print 'll:', ll                  

la = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
la = list(filter(lambda x : x%2==0, la))    # 结合lambda
print 'la :',la

"""map 函数会对指定序列做映射操作，map(function or None, sequence) ->  map object (list, tuple, or string in 2.x)
map 函数会对序列参数 sequence 中的每个元素调用 function 函数，返回的结果为每一个元素调用function函数的返回值"""            
def sqr(i):
	return i**2
lc = [1,2,3]
lc = map(sqr,lc)
print(lc)   # 3.x版本返回的是对象 map object

ld = [1,2,3]
ld = list(map(lambda x : x**2,ld))# 结合lambda
print(ld)
	


