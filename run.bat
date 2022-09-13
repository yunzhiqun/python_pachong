@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:begin
REM
c:/workspace/pythonProject/zhonghang_yingbaing_huilv_pachong/car/Scripts/python.exe c:/workspace/pythonProject/zhonghang_yingbaing_huilv_pachong/auto_send_weixin_message.py