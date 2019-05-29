import tkinter as tk
import http.client
from xml.etree import ElementTree
import webbrowser
import tkinter.simpledialog
import urllib
from urllib import parse
import gmail

##googlemap
def Parsing_KAKAOMAP_Address(search_address):
    # 카카오 요청, 다른 예시는 https://developers.kakao.com/docs/restapi/local 참고
    server = "dapi.kakao.com"  # 서버
    headers = {'Authorization': 'KakaoAK cdb3b880191792500cb20af4a46a8edc'}  # 인증 키
    hangul_utf = urllib.parse.quote(search_address)
    url = "/v2/local/search/address.xml?query=%s" %hangul_utf # 좌표값 url str화
    conn = http.client.HTTPSConnection(server)  # 서버 연결
    conn.request("GET", url, None, headers)
    req = conn.getresponse()
    data = req.read()  # 데이터 저장
    tree = ElementTree.fromstring(data)  # ElementTree로 string화
    itemElements = tree.getiterator("documents")  # documents 이터레이터 생성

    result = []
    for item in itemElements:
        addr = []
        addr.append(item.find("y"))
        addr.append(item.find("x"))
        result.append((float(addr[1].text), float(addr[0].text)))
    return result


def make_googlemap_url(center, zoom=16, maptype='roadmap'):
    key = 'AIzaSyA9gjC63ldBuHDwYM6flkFJDbTq6vQhFdg'
    point = str(center[1]) + ',' + str(center[0])
    size = (500, 500)

    url = "http://maps.google.com/maps/api/staticmap?"
    url += "center=%s&" % point
    url += "zoom=%i&" % zoom
    url += 'scale=1&'
    url += "size=" + str(size[0]) + 'x' + str(size[1]) + '&'
    url += 'maptype=' + maptype + '&'
    url += '&markers=color:red%7Clabel:C%7C' + point + '&'
    url += 'key=' + key

    return url
##

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
            if req.status != 200:
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
        self.button2 = tk.Button(self.frame, text = '학술지 소재지 위치 검색', width = 15, command = self.new_window1)
        self.button2.pack(side = tk.LEFT)
        self.frame1 = tk.Frame(self.master)
        self.label = tk.Label(self.frame1, text = '검색 결과 총량 빈도수')
        self.label.pack(side = tk.LEFT)
        self.frame.pack()
        self.frame1.pack()

        ##그래프
        self.SearchAmount = [0]*10
        self.SearchKeyword=[0]*10
        self.SearchAmountIndex = 0
        self.SearchAmountStart = 0
        self.width=500
        self.height=300
        self.canvas = tk.Canvas(self.master,width=self.width,height = self.height, bg='white')
        self.canvas.pack()

    def new_window(self):

        self.keyword = self.entry1.get()

        if not self.keyword == '':
            self.newWindow = tk.Toplevel(self.master)
            self.app = Demo2(self.newWindow, self.keyword)

            newElement = eval(self.app.root.find("channel").find("total").text)
            if newElement is None:
                newElement = 1
            if self.SearchAmountIndex < 10:
                self.SearchKeyword[self.SearchAmountIndex] = self.keyword
                self.SearchAmount[self.SearchAmountIndex] = newElement
                self.SearchAmountIndex += 1
            else:
                self.SearchKeyword[self.SearchAmountStart] = self.keyword
                self.SearchAmount[self.SearchAmountStart] = newElement
                self.SearchAmountStart = (self.SearchAmountStart + 1) % 10
            self.displayGraph()
        else:
            tkinter.messagebox.showinfo("오류","단어를 입력해주세요")

    def displayGraph(self):
        self.canvas.delete('all')
        maxC = int(max(self.SearchAmount))
        self.canvas.create_line(10,self.height-30,self.width-10,self.height-30)
        barW = (self.width-20)/len(self.SearchAmount)
        for i in range(len(self.SearchAmount)):
            self.canvas.create_rectangle(i*barW+25,-30+self.height-((self.height-70)*self.SearchAmount[(i+self.SearchAmountStart)%len(self.SearchAmount)]/maxC),i*barW+30,self.height-30)
            #self.canvas.create_text(i*barW+10+5,self.height-10+5,text=chr(i+97))
            self.canvas.create_text(i*barW+10+10,-35+self.height-((self.height-70)*self.SearchAmount[(i+self.SearchAmountStart)%len(self.SearchAmount)]/maxC)-10,text=self.SearchAmount[(i+self.SearchAmountStart)%len(self.SearchAmount)])
            self.canvas.create_text(i * barW + 10 + 10,-50 + self.height - ((self.height - 70) * self.SearchAmount[(i+self.SearchAmountStart)%len(self.SearchAmount)] / maxC) - 10, text=self.SearchKeyword[(i+self.SearchAmountStart)%len(self.SearchAmount)])

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

##
        tk.Button(self.frameForResult, text ='이전자료', command = self.prevPage).pack(side=tk.LEFT)
        tk.Label(self.frameForResult, text='0').pack(side=tk.LEFT)
        self.PageLabel = tk.Label(self.frameForResult, text=str(self.page))
        self.PageLabel.pack(side=tk.LEFT)
        tk.Label(self.frameForResult, text=self.root.find("channel").find("total").text).pack(side=tk.LEFT)
        tk.Button(self.frameForResult, text ='다음자료', command = self.nextPage).pack(side=tk.LEFT)
##
        self.quitButton = tk.Button(self.frameForResult, text ='닫기', command = self.close_windows)
        self.quitButton.pack(side=tk.RIGHT)

    def nextPage(self):
        self.page += 10

        self.getXmlStartWithNthPage(self.conn, self.keyword, self.page)
        self.PageLabel.config(text=str(self.page))


    def prevPage(self):
        self.page -= 10
        if self.page < 1:
            self.page = 1

        self.getXmlStartWithNthPage(self.conn, self.keyword, self.page)
        self.PageLabel.config(text=str(self.page))

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
        if root.find("channel") is not None:
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
                        link = item.find("link").text
                        link = link.replace('<b>', '')
                        link = link.replace('</b>', '')
                        label = tk.Label(self.frameForSelect, text = link, fg="blue",cursor="hand2")
                        label.pack()
                        label.bind("<Button-1>", self.openWebBrowserFunc)
                        desc = item.find("description").text
                        if desc is not None:
                            tk.Label(self.frameForSelect, text = "-문서 설명-").pack()
                            desc = desc.replace('<b>', '')
                            desc = desc.replace('</b>', '')
                            tk.Label(self.frameForSelect, text = desc).pack()
                        else:
                            tk.Label(self.frameForSelect, text = "문서 설명이 존재하지 않습니다..").pack()

                        tk.Label(self.frameForSelect, text="        해당 정보를 메일로 전달").pack(side=tk.LEFT)
                        self.mailEntry = tk.Entry(self.frameForSelect)
                        self.mailEntry.pack(side=tk.LEFT)
                        if desc is None:
                            tk.Button(self.frameForSelect,text="보내기", command= lambda: self.MailButton(title+'\n'+link, title)).pack(side=tk.LEFT)
                        else:
                            tk.Button(self.frameForSelect,text="보내기", command= lambda: self.MailButton(title+'\n'+link+'\n'+desc, title)).pack(side=tk.LEFT)
                    i += 1


    def MailButton(self, mailsentence, mailtitle):
        if self.mailEntry.get() != '':
            gmail.sendMail(self.mailEntry.get(),mailsentence, mailtitle)


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

from urllib.request import urlopen
from PIL import Image, ImageTk
from io import BytesIO

class Demo3:
    def __init__(self, master):
        self.master = master
        self.frameForSearch = tk.Frame(self.master)
        #self.label = tk.Label(self.frame1, text = '오프라인 자료창', width =60, height = 30)
        #self.label.pack(side=tk.LEFT)
        self.frameForSearch.pack(side= tk.LEFT,anchor='n')

        tk.Label(self.frameForSearch, text='지역을 입력해주세요').pack()

        self.EntryForSearch = tk.Entry(self.frameForSearch)
        self.EntryForSearch.pack()

        self.tree = ElementTree

        tk.Button(self.frameForSearch,text = "검색", command = self.showResult).pack()

        self.ListboxForSearch = tk.Listbox(self.frameForSearch, height=20)
        self.ListboxForSearch.bind('<Double-Button-1>', self.ListClicked)
        self.ListboxForSearch.pack()

        self.quitButton = tk.Button(self.frameForSearch, text = '닫기', width = 15, command = self.close_windows)
        self.quitButton.pack()

        self.frameForMap = tk.Frame(self.master, height=250, width = 350)
        self.frameForMap.pack(side=tk.TOP,anchor='n')

        self.frameForSpotInfo = tk.Frame(self.master, height=140, width = 500)
        self.frameForSpotInfo.pack(side=tk.BOTTOM,anchor='s')

        tk.Label(self.frameForSpotInfo, text="소재지 간략 정보").place(y=0)
        tk.Label(self.frameForSpotInfo, text="기관명").place(y=20)
        self.libname = tk.Text(self.frameForSpotInfo, width=40,height=1)
        self.libname.place(x=55,y=20)
        tk.Label(self.frameForSpotInfo, text="전화").place(y=40)
        self.telno = tk.Text(self.frameForSpotInfo, width=40,height=1)
        self.telno.place(x=55,y=40)
        tk.Label(self.frameForSpotInfo, text="담당부서").place(y=60)
        self.task = tk.Text(self.frameForSpotInfo, width=40,height=1)
        self.task.place(x=55,y=60)
        tk.Label(self.frameForSpotInfo, text="홈페이지").place(y=80)
        self.siteUrl = tk.Text(self.frameForSpotInfo, width=40,height=1)
        self.siteUrl.place(x=55,y=80)
        tk.Label(self.frameForSpotInfo, text="우편번호").place(y=100)
        self.zipcod = tk.Text(self.frameForSpotInfo, width=40,height=1)
        self.zipcod.place(x=55,y=100)
        tk.Label(self.frameForSpotInfo, text="메일").place(y=120)
        self.mail = tk.Text(self.frameForSpotInfo, width=40,height=1)
        self.mail.place(x=55,y=120)

        ##

        ##
    def ListClicked(self, event):
        nIndex = event.widget.curselection()
        if len(nIndex) == 1:
            # self.newWindow = tk.Toplevel(self.master)
            # self.app = info_window(self.newWindow, self.root , nIndex)

            _list = self.frameForMap.winfo_children()
            for child in _list:
                child.destroy()
            i=0
            for item in self.tree.find("body").find("items").getiterator("item"):
                if i==nIndex[0]:
                    self.libname.delete(1.0,tk.END)
                    if item.find("libname") is not None:
                        self.libname.insert(tk.INSERT,item.find("libname").text)
                    else:
                        self.libname.insert(tk.INSERT,"정보가 없습니다")

                    self.mail.delete(1.0,tk.END)
                    if item.find("mainemail") is not None:
                        self.mail.insert(tk.INSERT, item.find("mainemail").text)
                    else:
                        self.mail.insert(tk.INSERT,"정보가 없습니다")

                    self.telno.delete(1.0,tk.END)
                    if item.find("maintelno") is not None:
                        self.telno.insert(tk.INSERT,item.find("maintelno").text)
                    else:
                        self.telno.insert(tk.INSERT,"정보가 없습니다")

                    self.task.delete(1.0,tk.END)
                    if item.find("taskdept") is not None:
                        self.task.insert(tk.INSERT,item.find("taskdept").text)
                    else:
                        self.task.insert(tk.INSERT,"정보가 없습니다")

                    self.siteUrl.delete(1.0,tk.END)
                    if item.find("url") is not None:
                        self.siteUrl.insert(tk.INSERT,item.find("url").text)
                    else:
                        self.siteUrl.insert(tk.INSERT,"정보가 없습니다")

                    self.zipcod.delete(1.0,tk.END)
                    if item.find("zipno") is not None:
                        self.zipcod.insert(tk.INSERT,item.find("zipno").text)
                    else:
                        self.zipcod.insert(tk.INSERT,"정보가 없습니다")

                    if item.find("address") is not None:
                        self.showMap(item.find("address").text)
                    else:
                        tk.Label(self.frameForMap,text="지도 정보가 없습니다..").pack()
                i+=1


    def close_windows(self):
        self.master.destroy()

    def getTree(self, keyword, Tree):
        conn = http.client.HTTPConnection("dev.ndsl.kr")  # openapi.naver.comdev.ndsl.kr/openapi/service
        keyword = parse.quote(keyword)
        # keyword = keyword.encode("utf-8")
        conn.request("GET",
                     "/openapi/service/SchlsphjrnlLocplcInfoInqireSvc/getRegstSchlshpjrnlInsttListInfo?serviceKey=pucypWLDfbEtC6UjRg%2BTBdXIpC2MNzs5iRuBns3ZhSkMD8JIA5DCkS4fojhfaQWkn%2FRiQz1%2FRphZOqKL7nC5ng%3D%3D&address={0}".format(
                         keyword))
        req = conn.getresponse()
        print(req.status, req.reason)
        data = req.read().decode('utf-8')
        self.tree = ElementTree.fromstring(data)
        self.ListboxForSearch.delete(0,self.ListboxForSearch.size())
        for i in self.tree.find("body").find("items").getiterator("item"):
            if i.find("abbrname") is not None:
                self.ListboxForSearch.insert(tk.END, i.find("abbrname").text)



    def showResult(self):
        if self.EntryForSearch.get() != '':
            self.getTree(self.EntryForSearch.get(), self.tree)


    def showMap(self, keyword):
        print(keyword)
        #print(Parsing_KAKAOMAP_Address(keyword)[0])
        MapURL = make_googlemap_url(Parsing_KAKAOMAP_Address(keyword)[0])
        with urlopen(MapURL) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        map_image = ImageTk.PhotoImage(im)
        tk.Label(self.frameForMap, image=map_image, height=250, width=350, background='white').pack()
        tk.mainloop()


def main():
    root = tk.Tk()
    app = TopWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()