#!/usr/bin/env python
# encoding:utf-8
"""
lambda匿名函数,列表推导的一些例子
"""
class Lambda(object):

    def list1(self):
        list1 = range(1, 11)
        self.list1 =list1
        print "list1:", list1

    def list2(self):
        """通过append去实现list1的列表推导"""
        list2 = []
        list1 = self.list1
        # list1 = range(1, 11)
        for x in list1:
            list2.append(x * x)
        print "list2:", list2

    def list4(self):
        list3 = ["APPLE", 'Banana', 'Orange', 122]
        """#判断实例类型为string,实现转换"""
        list4 = [s.lower() for s in list3 if isinstance(s, str)]
        print list4
        return list4

    def list5(self):
        list1 =self.list1
        """map()是 Python 内置的高阶函数，它接收一个函数 f 和一个 list，并通过把函数 f
        依次作用在 list 的每个元素上，得到一个新的 list 并返回。可见如下地址：
        http://blog.csdn.net/seetheworld518/article/details/46959871"""
        list5 = map(str, list1)
        print "map() is list5:", list5

    def list6(self):
        """效果其实就是map()"""
        lista = range(1, 11)
        print "lista:", lista


        def f(x):
            return x*x
        print "f:", f

        res = []
        for s in lista:
            res.append(f(s))
        print "lista --> f():", res
        """lambda, 对每个lista中的元素进行 f(x),map()接受函数见29行"""
        print "map is lambda: ", map(lambda x: x*x, lista)

if __name__ == '__main__':
    obj = Lambda()
    obj.list1()
    obj.list2()
    obj.list4()
    obj.list5()
    obj.list6()
