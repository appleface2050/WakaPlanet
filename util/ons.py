# encoding:utf-8
import ConfigParser
import hashlib
import httplib
import time
from urlparse import urlparse
import socket
import hmac
import json
from hashlib import sha1
import datetime

from bst_android_market.settings import ONE_URL, ALIYUN_ACCESS_ID, ALIYUN_ACCESS_SECRET_KEY


def parseURL(url):
    iplist = socket.gethostbyname_ex(url)
    if len(iplist) == 0:
        return None
    ips = iplist[2]
    if len(ips) == 0:
        return None
    return ips[0]


def calSignature(signString, sk):
    mac = hmac.new(sk, signString, sha1)
    return mac.digest().encode('base64').rstrip()


class HttpConsumer(object):
    def __init__(self, ONS_CONF):
        """签名字段"""
        self.signature = "Signature"
        """Consumer ID"""
        self.consumerid = "ConsumerID"
        """消费主题"""
        self.topic = "Topic"
        """访问码"""
        self.ak = "AccessKey"
        # """配置文件解析器"""
        # self.cf = ConfigParser.ConfigParser()
        self.ONS_CONF = ONS_CONF

    def job(self, message):
        print message.get("tag", "")
        print message.get("key", "")
        print message.get("body", "")

    def process(self):
        topic = self.ONS_CONF.get("topic")
        """存储消息URL路径"""
        url = self.ONS_CONF.get("url")
        """访问码"""
        ak = self.ONS_CONF.get("ak")
        """密钥"""
        sk = self.ONS_CONF.get("sk")
        """Producer ID"""
        cid = self.ONS_CONF.get("cid")
        newline = "\n"
        """获取URL主机域名地址"""
        urlname = urlparse(url).hostname
        """连接存储消息的服务器"""
        conn = httplib.HTTPConnection(parseURL(urlname))
        while True:
            try:
                """时间戳"""
                date = repr(int(time.time() * 1000))[0:13]
                """构造签名字符串"""
                signString = topic + newline + cid + newline + date
                """计算签名值"""
                sign = calSignature(signString, sk)
                """请求消息HTTP头部"""
                headers = {
                    self.signature: sign,
                    self.ak: ak,
                    self.consumerid: cid
                }
                """开始发送获取消息的HTTP请求"""
                conn.request(method="GET", url=url + "/message/?topic=" + topic + "&time=" + date + "&num=32",
                             headers=headers)
                """获取HTTP应答消息"""
                response = conn.getresponse()
                """验证应答消息状态值"""
                if response.status != 200:
                    print response.status
                    continue
                """从应答消息中读取实际的消息内容"""
                msg = response.read()
                """将实际的消费消息进行解码"""
                messages = json.loads(msg)
                if len(messages) == 0:
                    print datetime.datetime.now()
                    print "message: ",messages
                    time.sleep(2)
                    continue
                """依次获取每条消费消息"""
                for message in messages:
                    print message
                    """计算时间戳"""
                    date = repr(int(time.time() * 1000))[0:13]
                    """构建删除消费消息URL路径"""
                    delUrl = url + "/message/?msgHandle=" + message['msgHandle'] + "&topic=" + topic + "&time=" + date
                    """构造签名字符串"""
                    signString = topic + newline + cid + newline + message['msgHandle'] + newline + date
                    """进行签名"""
                    sign = calSignature(signString, sk)
                    """构造删除消费消息HTTP头部"""
                    delheaders = {
                        self.signature: sign,
                        self.ak: ak,
                        self.consumerid: cid,
                    }
                    """发送删除消息请求"""
                    conn.request(method="DELETE", url=delUrl, headers=delheaders)
                    """获取请求应答"""
                    response = conn.getresponse()
                    """读取应答内容"""
                    msg = response.read()
                    print "delete msg:" + msg

                    self.job(message)

            except Exception, e:
                print e
            finally:
                conn.close()


class HttpProducer(object):
    def __init__(self, ONS_CONF):
        """签名值"""
        self.signature = "Signature"
        """ProducerID"""
        self.producerid = "ProducerID"
        """消息主题"""
        self.topic = "Topic"
        """访问码"""
        self.ak = "AccessKey"
        """配置文件解析器"""
        # self.cf = ConfigParser.ConfigParser()
        """MD5对象"""
        self.md5 = hashlib.md5()
        self.ONS_CONF = ONS_CONF

    """
    发布消息主流程
    """

    def process(self, tag, key, content):
        msg = ""
        """读取配置文件"""
        # self.cf.read("user.properties")
        """读取消息主题"""
        topic = self.ONS_CONF.get("topic")
        """存储消息URL路径"""
        url = self.ONS_CONF.get("url")
        """访问码"""
        ak = self.ONS_CONF.get("ak")
        """密钥"""
        sk = self.ONS_CONF.get("sk")
        """Producer ID"""
        pid = self.ONS_CONF.get("pid")
        """HTTP请求主体内容"""
        # content = U"中文".encode('utf-8')
        content = content
        """分隔符"""
        newline = "\n"
        """获取URL域名地址"""
        urlname = urlparse(url).hostname
        """根据HTPP主体内容计算MD5值"""
        self.md5.update(content)
        """建立HTTP连接对象"""
        conn = httplib.HTTPConnection(parseURL(urlname))
        try:
            """时间戳"""
            date = repr(int(time.time() * 1000))[0:13]
            """构造签名字符串"""
            signString = str(topic + newline + pid + newline + self.md5.hexdigest() + newline + date)
            """计算签名"""
            sign = calSignature(signString, sk)
            """内容类型"""
            contentFlag = "Content-type"
            """HTTP请求头部对象"""
            headers = {
                self.signature: sign,
                self.ak: ak,
                self.producerid: pid,
                contentFlag: "text/html;charset=UTF-8"
            }
            """开始发送HTTP请求消息"""
            conn.request(method="POST",
                         url=url + "/message/?topic=" + topic + "&time=" + date + "&tag=%s&key=%s" % (tag, key),
                         body=content,
                         headers=headers)
            """获取HTTP应答消息"""
            response = conn.getresponse()
            """读取HTTP应答内容"""
            msg = response.read()
            print "response:"+msg

        except Exception, e:
            print e
            msg = e
        finally:
            conn.close()
            return msg

"""流程入口"""
if __name__ == '__main__':
    # ONS_CONF = {
    #     "topic": "bst-ceshi",
    #     "url": "http://publictest-rest.ons.aliyun.com",
    #     "ak": "t8z6fuZ2B1FldqmL",
    #     "sk": "ES2YRYWBREeBNeGCBczpc63FCLJvc9",
    #     "pid": "PID-ceshi-producer1",
    #     "cid": "CID-ceshi-consumer1",
    # }

    # """创建消息发布者"""
    # producer = HttpProducer(ONS_CONF)
    # """开启消息发布者"""
    # content = {"user_name": "123"}
    # producer.process("a", "a20170427", json.dumps(content))
    # producer = HttpProducer(ONS_CONF)
    # producer.process("a", "a20170427b", json.dumps(content))
    # producer = HttpProducer(ONS_CONF)
    # producer.process("a", "a20170427d", json.dumps(content))
    # producer = HttpProducer(ONS_CONF)
    # producer.process("a", "a20170427e", json.dumps(content))
    # producer = HttpProducer(ONS_CONF)
    # producer.process("a", "a20170427f", json.dumps(content))

    # consumer = HttpConsumer(ONS_CONF)
    # consumer.process()

    ONS_CONF = {
        "topic": "bst-android-market-sync-data",
        "url": ONE_URL,
        "ak": ALIYUN_ACCESS_ID,
        "sk": ALIYUN_ACCESS_SECRET_KEY,
        "pid": "PID-android-market-sync-data",
        "cid": "CID-android-market-sync-data",
    }
    producer = HttpProducer(ONS_CONF)
    """开启消息发布者"""
    content = {"type": "normal"}
    producer.process("data_sync_game_library", "data_sync_game_library", json.dumps(content))