import tkinter as tk
import http.client
from xml.etree import ElementTree
import webbrowser
import tkinter.simpledialog
import urllib
from urllib import parse

timer = 5.0
opacity = 1.0

class Logo:
    def __init__(self, master):
        self.master = master
        self.master.attributes('-alpha', opacity)
        # The image must be stored to Tk or it will be garbage collected.
        self.master.image = tk.PhotoImage(file='res/img/logosample0.png')
        self.label = tk.Label(self.master, image=self.master.image, bg='white')
        self.master.overrideredirect(True)
        self.master.geometry("+250+250")
        self.master.lift()
        self.master.wm_attributes("-topmost", True)
        self.master.wm_attributes("-disabled", True)
        self.master.wm_attributes("-transparentcolor", "white")
        self.label.pack()
        self.myTimer()

        self.isConnectionTrying = True
        self.isConnected = True
        # 공공데이터포털 API 접속 확인
        try:
            conn = http.client.HTTPConnection("dev.ndsl.kr")  # openapi.naver.comdev.ndsl.kr/openapi/service
        except:
            self.isConnected = False
        keyword = "서울"
        keyword = urllib.parse.quote(keyword)
        try:
            conn.request("GET",
                         "/openapi/service/SchlsphjrnlLocplcInfoInqireSvc/getRegstSchlshpjrnlInsttListInfo?serviceKey=pucypWLDfbEtC6UjRg%2BTBdXIpC2MNzs5iRuBns3ZhSkMD8JIA5DCkS4fojhfaQWkn%2FRiQz1%2FRphZOqKL7nC5ng%3D%3D&address={0}".format(
                             keyword))
            req = conn.getresponse()
            if (req.status != 200):
                self.isConnected = False
        except:
            self.isConnected = False


        self.isConnectionTrying = False

    def myTimer(self):
        global opacity
        global root
        self.master.attributes('-alpha', opacity)

        if opacity > 0.0 or self.isConnectionTrying == True:
            opacity -= 0.01
            self.master.after(16, self.myTimer)
        else:
            #현재 클래스에서 인스턴스로 새 tk를 만든다, 현재 tk객체는 해제한다
            self.newWindow = tk.Tk()

            if self.isConnected == False:
                self.app = ErrorWindow(self.newWindow)
            else:
            #만약 실패하면 만드는 것을 실행하지 않는다..
                self.app = TopWindow(self.newWindow)
            self.master.destroy()

class ErrorWindow:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.label = tk.Label(self.frame, text="서버연결에 실패하였습니다.")
        self.label.pack()
        self.button = tk.Button(self.frame, text="종료", command = lambda x = self.master : x.destroy() )
        self.button.pack()


class TopWindow:
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

        if not self.keyword == '':
            self.newWindow = tk.Toplevel(self.master)
            self.app = Demo2(self.newWindow, self.keyword)
        else:
#            tkinter.messagebox.showinfo("오류","검색 내용이 비었습니다.")
            pass


    def new_window1(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo3(self.newWindow)


class Demo2:
    def __init__(self, master, keyword):
        #현재 검색중인 페이지
        self.page = 1

        #부모 tk를 저장합니다
        self.master = master

        #검색결과목록과 결과목록 순회와 관련된 내용을 넣을 프레임입니다
        self.frameForResult = tk.Frame(self.master)

        #검색결과목록을 보일 박스입니다
        self.searchResult = tk.Listbox(self.frameForResult, width = 100)
        self.searchResult.bind('<Double-Button-1>', self.create_info_window)

        #검색결과 내용을 넣을 프레임입니다
        self.frameForSelect = tk.Frame(self.master)
        self.frameForSelect.pack(side=tk.BOTTOM)
        #검색창에서 선택한 항목의 정보를 표시할 박스입니다
        self.infoLabel = tk.Label(self.frameForSelect, text = "any")
        self.infoLabel.pack()

        server = "openapi.naver.com"
        self.conn = http.client.HTTPSConnection(server)
        self.keyword = keyword.encode("utf-8")

        self.getXmlStartWithNthPage(self.conn, self.keyword, self.page)

        self.searchResult.pack(side=tk.BOTTOM)
##
        self.label = tk.Label(self.frameForResult, text ='온라인 자료 검색 결과')
        self.label.pack(side=tk.BOTTOM)

        self.frameForResult.pack(side=tk.BOTTOM)

        tk.Button(self.frameForResult, text ='다음자료', command = self.nextPage).pack()
        tk.Button(self.frameForResult, text ='이전자료', command = self.prevPage).pack()
        self.quitButton = tk.Button(self.frameForResult, text ='닫기', command = self.close_windows)
        self.quitButton.pack(side=tk.BOTTOM)

    def nextPage(self):
        self.page += 10

        self.getXmlStartWithNthPage(self.conn, self.keyword, self.page)


    def prevPage(self):
        pass


    def getXmlStartWithNthPage(self, conn, keyword, nPageNum):
        client_id = "ZuLj_9774MFbh52EAnsz"
        client_secret = "0fgHPxzAdQ"
        conn.request("GET", ("/v1/search/doc.xml?query={0}&display=10&start="+str(nPageNum)).format(keyword),
                     None, {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret})
        req = conn.getresponse()

        if req.status == 200:
            print(req.status, req.reason)
            cLen = req.getheader("Content-Length")
            data = req.read(int(cLen)).decode('utf-8')
            self.root = ElementTree.fromstring(data)
            self.show_resultBox(self.root, self.searchResult)
        else:
            tkinter.messagebox.showinfo("오류","정보를 받아올 수 없음")


    def show_resultBox(self, root, resultBox):
        resultBox.delete(0,resultBox.size())
        channelElements = root.getiterator("channel")
        for things in channelElements:
            itemElements = things.getiterator("item")
            for item in itemElements:
                title = item.find("title").text
                title = title.replace('<b>', '')
                title = title.replace('</b>', '')
                resultBox.insert(tk.END, title)

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


    def openWebBrowserFunc(self, event):
        webbrowser.open_new(event.widget.cget("text"))


    def create_info_window(self, event):
        #
        # self.keyword = self.entry1.get()
        #

        nIndex = event.widget.curselection()
        if len(nIndex) == 1:
            # self.newWindow = tk.Toplevel(self.master)
            # self.app = info_window(self.newWindow, self.root , nIndex)

            channelElements = self.root.getiterator("channel")
            for things in channelElements:
                i = 0
                for item in things.iter("item"):
                    if i == nIndex[0]:
                        ##
                        ## 프레임 안에 자식 위젯을 전부 없앤다
                        _list = self.frameForSelect.winfo_children()
                        for child in _list:
                            child.destroy()
                        ##

                        tk.Label(self.frameForSelect, text= "학술지 이름").pack()
                        title = item.find("title").text
                        title = title.replace('<b>', '')
                        title = title.replace('</b>', '')
                        text = tk.Text(self.frameForSelect,height=1, width = 100)
                        text.pack()
                        text.insert(tk.INSERT,title)

                        tk.Label(self.frameForSelect, text="네이버 링크").pack()
                        title = item.find("link").text
                        title = title.replace('<b>', '')
                        title = title.replace('</b>', '')
                        label = tk.Label(self.frameForSelect, text = title, fg="blue",cursor="hand2")
                        label.pack()
                        label.bind("<Button-1>", self.openWebBrowserFunc)
                        title = item.find("description").text
                        if title is not None:
                            tk.Label(self.frameForSelect, text = "-문서 설명-").pack()
                            title = title.replace('<b>', '')
                            title = title.replace('</b>', '')
                            tk.Label(self.frameForSelect, text = title).pack()
                        else:
                            tk.Label(self.frameForSelect, text = "문서 설명이 존재하지 않습니다..").pack()
                    i += 1


    def show_selected_info(self):
        pass


class info_window:
    def __init__(self, master, XmlTree, nListBoxIndex):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        channelElements = XmlTree.getiterator("channel")
        for things in channelElements:
            print(nListBoxIndex[0])
            nIndex = 0
            for item in things.iter("item"):
                if nIndex == nListBoxIndex[0]:
                    title = item.find("title").text
                    title = title.replace('<b>', '')
                    title = title.replace('</b>', '')
                    tk.Label(self.frame, text = title).pack()
                    title = item.find("link").text
                    title = title.replace('<b>', '')
                    title = title.replace('</b>', '')
                    tk.Label(self.frame, text = title).pack()
                    title = item.find("description").text
                    if title is not None:
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

        conn = http.client.HTTPConnection("dev.ndsl.kr")  # openapi.naver.comdev.ndsl.kr/openapi/service
        keyword = "서울"
        keyword = parse.quote(keyword)
        # keyword = keyword.encode("utf-8")
        conn.request("GET",
                     "/openapi/service/SchlsphjrnlLocplcInfoInqireSvc/getRegstSchlshpjrnlInsttListInfo?serviceKey=pucypWLDfbEtC6UjRg%2BTBdXIpC2MNzs5iRuBns3ZhSkMD8JIA5DCkS4fojhfaQWkn%2FRiQz1%2FRphZOqKL7nC5ng%3D%3D&address={0}".format(
                         keyword))
        req = conn.getresponse()
        print(req.status, req.reason)
        print(req.read().decode('utf-8'))

    def close_windows(self):
        self.master.destroy()


def main():
    root = tk.Tk()
    app = Logo(root)
    root.mainloop()


if __name__ == '__main__':
    main()