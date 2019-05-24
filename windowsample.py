import tkinter as tk
import http.client

timer = 5.0
opacity = 1.0

class Logo:
    def __init__(self, master):
        self.master = master
        self.master.attributes('-alpha', opacity)
        # The image must be stored to Tk or it will be garbage collected.
        self.master.image = tk.PhotoImage(file='res\img\logosample0.png')
        self.label = tk.Label(self.master, image=self.master.image, bg='white')
        self.master.overrideredirect(True)
        self.master.geometry("+250+250")
        self.master.lift()
        self.master.wm_attributes("-topmost", True)
        self.master.wm_attributes("-disabled", True)
        self.master.wm_attributes("-transparentcolor", "white")
        self.label.pack()
        self.myTimer()

    def myTimer(self):
        global opacity
        global root
        self.master.attributes('-alpha', opacity)

        if opacity > 0.0:
            opacity -= 0.01
            self.master.after(16, self.myTimer)
        else:
            #현재 클래스에서 인스턴스로 새 tk를 만든다 현재 tk객체는 해제한다
            self.newWindow = tk.Tk()
            self.app = Demo1(self.newWindow)
            #self.app = Demo1(self.master)
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

        self.keyword = self.entry1.get()

        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow, self.keyword)

    def new_window1(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo3(self.newWindow)


class Demo2:
    def __init__(self, master, keyword):
        self.master = master
        self.frame1 = tk.Frame(self.master)

        self.searchResult = tk.Text(self.frame1,width=49,height=27,borderwidth=12)

        server = "openapi.naver.com"
        client_id = "ZuLj_9774MFbh52EAnsz"
        client_secret = "0fgHPxzAdQ"
        conn = http.client.HTTPSConnection(server)
        keyword = keyword.encode("utf-8")
        conn.request("GET", "/v1/search/doc.xml?query={0}&display=10&start=1".format(keyword),
                     None, {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret})
        req = conn.getresponse()
        print(req.status, req.reason)
        cLen = req.getheader("Content-Length")
        data = req.read(int(cLen)).decode('utf-8')
        self.searchResult.insert(tk.INSERT, data)
        self.searchResult.insert(tk.INSERT, "피피")

        self.searchResult.pack()

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
    app = Demo1(root)
    root.mainloop()


if __name__ == '__main__':
    main()