#-*- coding:utf8 -*-
'''
1.此脚本主要用于在执行pabot并行执行后，如果有失败的案例，则针对失败的案例进行重试。
2.适用于jenkins运行时，在pabot或者pybot后面一步执行
3.参数上除了默认采用了report目录作为output的输出目录，其余参数与pybot的参数一致即可。
'''
import os,shutil,sys
from robot import rebot

def retry(*args):
    #处理参数中，目录文件中的空格问题
    new_arg_list = []
    for li in sys.argv[1:]:
        if li.find(' ') != -1:
            new_arg_list.append('"%s"' % li)
        else:
            new_arg_list.append(li)
    arg_str = ' '.join(new_arg_list)
    #print arg_str
    try:
        tmp_str = open('report/output.xml','r+').read()
    except Exception:
        print 'report/output.xml not find!   ...... so exit'
        return 1
    if tmp_str.find('<status status="FAIL"') != -1:
        #所有输出文件都move到report/firstrun目录，包括js和png文件
        robotfiles = ['output.xml','log.html', 'report.html']
        for li in os.listdir('report'):
            if li.endswith('.js') or li.endswith('.png'):
                robotfiles.append(li)
        os.makedirs('report/firstrun')
        for filename in robotfiles:
            print 'move robotfile %s to firstrun/%s'  % (filename,filename)
            shutil.move('report/%s' % filename,'report/firstrun/%s' % filename)
        #对report/firstrun下面的出错的case重新运行，结果写入report/rerun目录
        print 'retry pybot for failed case......'
        os.makedirs('report/rerun')
        os.system("pybot -R report/firstrun/output.xml -d report/rerun -o output.xml %s" % arg_str)
        os.system(r"copy /Y report\firstrun\*.png report")
        os.system(r"copy /Y report\rerun\*.png report")
        print 'rebot recreate new output.xml,log.html and report.html'
        #rerunmerge换为建议的merge参数，--splitlog把log.html拆成一堆小js文件方便浏览器装载
        sys.exit(rebot('report/firstrun/output.xml','report/rerun/output.xml',output='output.xml',outputdir='./report',merge=True, splitlog=True))
    else:
        print "all case run PASS!   No retry!"
        return 0


if __name__=="__main__":
    retry()
