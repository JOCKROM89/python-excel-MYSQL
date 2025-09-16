import tkinter as tk
from tkinter import ttk
from update import update
from check import check
from tkinter import messagebox
import os
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MYSQL数据库查询")
        
        # 创建菜单栏
        menu = tk.Menu(self)
        self.config(menu=menu)
        menu.add_command(label='查询', command=self.show_page1)
        menu.add_command(label='更新', command=self.show_page3)

        self.current_page = None  # 记录当前页面

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # 显示首页
        self.show_page1()

    def show_page1(self):
        if self.current_page is not None:
            self.current_page.destroy()  # 销毁当前页面

        self.geometry("500x280")
        self.current_page = Page1(self)
        self.current_page.grid(row=0, column=0, sticky='nsew')  # 使用 grid 布局

    def show_page2(self, rows):
        if self.current_page is not None:
            self.current_page.destroy()  # 销毁当前页面

        self.geometry("1050x400")
        self.current_page = Page2(self, rows)
        self.current_page.grid(row=0, column=0, sticky='nsew')  # 使用 grid 布局

    def show_page3(self):
        if self.current_page is not None:
            self.current_page.destroy()  # 销毁当前页面

        self.geometry("500x280")
        self.current_page = Page3(self)
        self.current_page.grid(row=0, column=0, sticky='nsew')  # 使用 grid 布局


class Page1(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        
        label1 = tk.Label(self, text="请输入要查询文件地址，例如：D:/2024-10电算mro部品申请.xlsx")
        label1.grid(row=0, column=0, pady=40)  # 使用 grid 布局

        self.entry1 = tk.Entry(self, width=30)
        self.entry1.grid(row=1, column=0, padx=150, pady=10)  # 使用 grid 布局

        button_to_frame2 = tk.Button(self, text="查询", command=self.query)
        button_to_frame2.grid(row=2, column=0, pady=10)  # 使用 grid 布局

    def query(self):
        query = self.entry1.get()
        if len(query)<= 4:
            messagebox.showwarning("输入错误", "请输入文件地址")
        else:
            try:
                if os.path.isfile(query):
                    rows = check(query)
                    self.controller.show_page2(rows)  # Load data into Page2
                else:
                    messagebox.showwarning("错误", "文件不存在")
            except Exception as e:
                    messagebox.showerror("错误", f"查询过程中发生错误: {e}")
            


class Page2(tk.Frame):
    def __init__(self, controller, rows):
        super().__init__(controller)
        self.controller = controller
        self.tree = ttk.Treeview(self, columns=("Column1", "Column2", "Column3", "Column4", "Column5", "Column6", "Column7"), show='headings')
        self.tree.heading("Column1", text="id")
        self.tree.heading("Column2", text="NO")
        self.tree.heading("Column3", text="名称")
        self.tree.heading("Column4", text="类型")
        self.tree.heading("Column5", text="品牌")
        self.tree.heading("Column6", text="单位")
        self.tree.heading("Column7", text="单价")

        # 设置列宽
        for i in range(1, 8):
            self.tree.column(f"Column{i}", width=150)

        self.tree.grid(row=0, column=0, sticky='nsew')  # 使用 grid 布局

        # 将查询结果添加到 Treeview
        for row in rows:
            self.tree.insert("", "end", values=row)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        button_to_frame1 = tk.Button(self, text="返回", command=self.controller.show_page1)
        button_to_frame1.grid(row=1, column=0, pady=10)  # 使用 grid 布局


class Page3(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        
        
        label3 = tk.Label(self, text="请输入需要更新的数据库文件地址：")
        label3.grid(row=0, column=0, padx=40, pady=(50,20))

        self.entry2 = tk.Entry(self, width=30)  # 设置输入框宽度
        self.entry2.grid(row=0, column=1,pady=(32,10))
        

        butn=tk.Button(self,text='更新',width=16,command=self.update)
        butn.grid(row=2,column=0,padx= 160,pady=20, columnspan=2, sticky='e' )


    def update(self):
        query2 = self.entry2.get()
        if len(query2)<= 4:
            messagebox.showwarning("错误", "请输入文件地址")
        elif len(query2)> 4:
            if os.path.isfile(query2):
                try:
                    change = update(query2)
                    if change == "update is over":
                        messagebox.showinfo("提示", "数据更新完成！")
                        self.entry2.delete(0, tk.END)  # 清空输入框
                    else:
                        messagebox.showinfo("警告！", "数据更新失败！")
                except Exception as e:
                    messagebox.showerror("错误", f"更新过程中发生错误: {e}")
            else:
                messagebox.showwarning("错误", "文件不存在")
if __name__ == "__main__":
    app = App()
    app.mainloop()


