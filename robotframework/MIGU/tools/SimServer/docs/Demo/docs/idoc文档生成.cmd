rem idocʵ������nodejs��module, �ο���https://github.com/jaywcjlove/idoc
rem idoc init rem �������Ҫ�ˣ���Ϊpackage.json�Ѿ�����
del /S /Q md
rmdir md
mkdir md
copy readme.md md\readme.md
idoc -b
start index.html