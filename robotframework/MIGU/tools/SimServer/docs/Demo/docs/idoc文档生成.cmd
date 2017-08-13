rem idoc实际上是nodejs的module, 参考：https://github.com/jaywcjlove/idoc
rem idoc init rem 这个不需要了，因为package.json已经生成
del /S /Q md
rmdir md
mkdir md
copy readme.md md\readme.md
idoc -b
start index.html