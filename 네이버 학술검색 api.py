import http.client
server = "openapi.naver.com"
client_id = "ZuLj_9774MFbh52EAnsz"
client_secret = "0fgHPxzAdQ"
conn = http.client.HTTPSConnection(server)
keyword = "5g"
keyword =  keyword.encode("utf-8")
conn.request("GET", "/v1/search/doc.xml?query={0}&display=10&start=1".format(keyword),
 None,{"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}) 
req = conn.getresponse() 
print(req.status, req.reason)
cLen = req.getheader("Content-Length")
print(req.read(int(cLen)).decode('utf-8')) 