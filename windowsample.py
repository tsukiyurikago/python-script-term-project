import tkinter as tk

timer = 5.0
opacity = 1.0

class Logo:
    def __init__(self, master):
        self.master = master
        self.master.attributes('-alpha', opacity)
        # The image must be stored to Tk or it will be garbage collected.
        self.master.image = tk.PhotoImage(file='res\img\logosample0.png')
        label = tk.Label(self.master, image=self.master.image, bg='white')
        self.master.overrideredirect(True)
        self.master.geometry("+250+250")
        self.master.lift()
        self.master.wm_attributes("-topmost", True)
        self.master.wm_attributes("-disabled", True)
        self.master.wm_attributes("-transparentcolor", "white")
        label.pack()
        self.myupdate()

    def myupdate(self):
        global opacity
        global root
        self.master.attributes('-alpha', opacity)
        self.master.after(16, self.myupdate)

        if opacity > 0.0:
            opacity -= 0.01
        else:
            self.newWindow = tk.Toplevel(self.master)
            self.app = Demo1(self.master)
            self.master.destroy()


class Demo1:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.entry1 = tk.Entry(self.frame, width = 30)
        self.entry1.pack(side = tk.LEFT)
        self.button1 = tk.Button(self.frame, text = '온라인 자료 검색', width = 15, command = self.new_window)
        self.button1.pack(side = tk.LEFT)
        self.button2 = tk.Button(self.frame, text = '오프라인 자료 검색', width = 15, command = self.new_window1)
        self.button2.pack(side = tk.LEFT)
        self.frame1 = tk.Frame(self.master)
        self.label = tk.Label(self.frame1, text = '검색창', width =15, height = 15)
        self.label.pack(side = tk.LEFT)
        self.frame.pack()
        self.frame1.pack()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)

    def new_window1(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo3(self.newWindow)


class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame1 = tk.Frame(self.master)
        self.label = tk.Label(self.frame1, text = '온라인 자료창', width =60, height = 30)
        self.label.pack(side=tk.LEFT)
        self.frame1.pack()
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = '닫기', width = 15, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()


class Demo3:
    def __init__(self, master):
        self.master = master
        self.frame1 = tk.Frame(self.master)
        self.label = tk.Label(self.frame1, text = '오프라인 자료창', width =60, height = 30)
        self.label.pack(side=tk.LEFT)
        self.frame1.pack()
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = '닫기', width = 15, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()


def main():
    root = tk.Tk()
    app = Logo(root)
    root.mainloop()


if __name__ == '__main__':
    main()