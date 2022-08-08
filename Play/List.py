import tkinter

root = tkinter.Tk()

sc = tkinter.Scrollbar(root)
sc.pack(side=tkinter.RIGHT, fill=tkinter.Y)

# 列表動，滾動條跟着動
lb = tkinter.Listbox(root, yscrollcommand=sc.set)
for i in range(50):
    lb.insert(tkinter.END, "列表 " + str(i))
lb.pack(side=tkinter.LEFT, expand=True)
# 滾動條動，列表跟着動
sc.config(command=lb.yview)

root.mainloop()