# -*- codeing: utf-8 -*-
# @Time :2022/7/5 8:22
# @Author :shilingming
# @Site :
# @File :auto_send_weixin_message.py
# @Software: PyCharm

import tkinter
# 导入消息对话框子模块
import tkinter.messagebox   
import main 
import eventlet  # 导入eventlet这个模块
# 弹出询问窗口
def show_message(root): 
    
    
    # 弹出对话框
    # 返回值为True或者False
    #主窗口隐藏
    # root.withdraw() 		 #****实现主窗口隐藏 
    result = tkinter.messagebox.askokcancel(title = '汇率',message='是否启动')
    return result
 #弹出完成提示窗口
def show_message_ok(root):
    
    tkinter.messagebox.showinfo(title = '汇率',message='任务完成')
#  #弹出错误提示窗口
# def show_message_error():
#     tkinter.Tk().withdraw() 		 #****实现主窗口隐藏
#     tkinter.messagebox.showerror(title = '汇率',message='启动失败')
#  #弹出警告提示窗口
# def show_message_warning():
#     tkinter.Tk().withdraw() 		 #****实现主窗口隐藏
#     tkinter.messagebox.showwarning(title = '汇率',message='启动警告')
#  #弹出询问窗口
# def show_message_question():
#     tkinter.Tk().withdraw() 		 #****实现主窗口隐藏
#     result = tkinter.messagebox.askquestion(title = '汇率',message='是否启动')
#     return result 
 
if __name__ == '__main__':
    # 创建主窗口
    #窗口置顶
    root = tkinter.Tk()
    root.wm_attributes('-topmost', 1) 
    root.withdraw() 		 #****实现主窗口隐藏
    # result = show_message(root) 
    # if result == True:
    #     main.run()
    #     show_message_ok(root) # 弹出完成提示窗口
    main.run()
    show_message_ok(root)