#-*- coding:utf8 -*-
'''
1.有部分prm的案例，由于某种原因failed_retry_for_prm.py失败，需要第二次retry
2.适用于jenkins运行时，在failed_second_retry_for_prm.py后面一步执行
3.参数上除了默认采用了report目录作为output的输出目录，其余参数与pybot的参数一致即可。
'''
import os,shutil,sys
from robot import rebot

def retry(*args):
    arg_str = ' '.join(sys.argv[1:])
    curdir = os.path.abspath(os.curdir)
    try:
        tmp_str = open('report/output.xml','r+').read()
    except Exception:
        print 'report/output.xml not find!   ...... so exit'
        return 1
    if tmp_str.find('<status status="FAIL"') != -1:
        robotfiles = ['output.xml','log.html', 'report.html']
        for filename in robotfiles:
            print ' copy robotfile %s to secondrun_%s'  % (filename,filename)
            shutil.copy('report/%s' % filename,'report/secondrun_%s' % filename)
        print 'retry pybot for failed case......'
        os.system("pybot -R report/secondrun_output.xml -d report/rerun -o rerun.xml %s" % arg_str)
        os.chdir('report')
        os.system(r"copy /Y rerun\*.png .")
        print 'rebot recreate new output.xml,log.html and report.html'
        #return os.system("rebot --rerunmerge -o output.xml secondrun_output.xml rerun/rerun.xml")
        sys.exit(rebot('secondrun_output.xml','rerun/rerun.xml',output='output.xml',outputdir='.',rerunmerge=True))
    else:
        print "all case run PASS!   No retry!"
        return 0


if __name__=="__main__":
    retry()
