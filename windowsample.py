import tkinter as tk
import http.client
from xml.etree import ElementTree

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
            #현재 클래스에서 인스턴스로 새 tk를 만든다, 현재 tk객체는 해제한다
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
        #부모 tk를 저장합니다
        self.master = master

        #새 프레임을 등록합니다
        self.frame1 = tk.Frame(self.master)
        self.page = 1

        #검색창을 보일 박스입니다
        self.searchResult = tk.Listbox(self.frame1)
        self.searchResult.bind("<Double-Button-1>", self.create_info_window)


        server = "openapi.naver.com"
        self.conn = http.client.HTTPSConnection(server)
        self.keyword = keyword.encode("utf-8")

        self.root = self.getXmlStartWithNthPage(self.conn, self.keyword, self.page)

        self.show_resultBox(self.root, self.searchResult)

        self.searchResult.pack()
##
        self.label = tk.Label(self.frame1, text = '온라인 자료창')
        self.label.pack(side=tk.LEFT)

        self.frame1.pack()

        self.frame = tk.Frame(self.master)

        tk.Button(self.frame1, text = '다음자료', command = self.nextPage).pack()
        tk.Button(self.frame1, text = '이전자료', command = self.prevPage).pack()
        self.quitButton = tk.Button(self.frame1, text = '닫기', command = self.close_windows)
        self.quitButton.pack(side=tk.RIGHT)
        self.frame.pack()

    def nextPage(self):
        self.page += 10

        self.root = self.getXmlStartWithNthPage(self.conn, self.keyword, self.page)

        self.show_resultBox(self.root, self.searchResult)


    def prevPage(self):
        pass


    def getXmlStartWithNthPage(self, conn, keyword, nPageNum):
        client_id = "ZuLj_9774MFbh52EAnsz"
        client_secret = "0fgHPxzAdQ"
        conn.request("GET", ("/v1/search/doc.xml?query={0}&display=10&start="+str(nPageNum)).format(keyword),
                     None, {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret})
        req = conn.getresponse()
        print(req.status, req.reason)
        cLen = req.getheader("Content-Length")
        data = req.read(int(cLen)).decode('utf-8')
        return ElementTree.fromstring(data)


    def show_resultBox(self, root, resultBox):
        resultBox.delete(0,resultBox.size())
        channelElements = root.getiterator("channel")
        for things in channelElements:
            itemElements = things.getiterator("item")
            nIndex = 0
            for item in itemElements:
                title = item.find("title").text
                title = title.replace('<b>', '')
                title = title.replace('</b>', '')
                resultBox.insert(nIndex, title)
                nIndex += 1

#        resultBox.insert(tk.INSERT, root[0][0].text)
#        resultBox.insert(tk.INSERT, '\n')
#        resultBox.insert(tk.INSERT, root[0][1].text)
#        resultBox.insert(tk.INSERT, '\n')
#        resultBox.insert(tk.INSERT, root[0][2].text)
#        resultBox.insert(tk.INSERT, '\n')
#        resultBox.insert(tk.INSERT, root[0][3].text)
#        resultBox.insert(tk.INSERT, '\n')
#        resultBox.insert(tk.INSERT, root[0][4].text)
#        resultBox.insert(tk.INSERT, '\n')
#        resultBox.insert(tk.INSERT, root[0][5].text)
#        resultBox.insert(tk.INSERT, '\n')
#        resultBox.insert(tk.INSERT, root[0][6].text)
#        if not root[0][4].text == '0':
#            resultBox.insert(tk.INSERT, '\n')
#            resultBox.insert(tk.INSERT, root[0][7].find("title").text)
#        else:
#            resultBox.insert(tk.INSERT, '\n검색결과 없음')

    def close_windows(self):
        self.master.destroy()


    def create_info_window(self, event):
        #
        # self.keyword = self.entry1.get()
        #
        nIndex = event.widget.curselection()
        self.newWindow = tk.Toplevel(self.master)
        self.app = info_window(self.newWindow, self.root , nIndex)
        pass


class info_window:
    def __init__(self, master, XmlTree, nListBoxIndex):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        channelElements = XmlTree.getiterator("channel")
        for things in channelElements:
            itemElements = things.getiterator("item")
            nIndex = 0
            for item in itemElements:
                if nIndex == int(nListBoxIndex[0]):
                    title = item.find("title").text
                    title = title.replace('<b>', '')
                    title = title.replace('</b>', '')
                    tk.Label(self.frame, text = title).pack()
                    nIndex += 1



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