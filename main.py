from btcmarkets import BTCMarkets
import urllib.request,json
from wxpy import *
import config
import time
api_key = config.api_key
private_key= config.private_key

#client = BTCMarkets (api_key, private_key)

#print client.trade_history('AUD', 'BTC', 10, 1)

#print client.order_detail([1234, 213456])
 
#print client.order_create('AUD', 'LTC', 100000000, 100000000, 'Bid', 'Limit', '1')
#res = client.get_market_tick('ETH','AUD')
#print(res)
#print(res['lastPrice'])

#初始化一个微信机器人
bot = Bot();
#扫描二维码登陆
#将孙，袁全加到my_friend里面
f1 = bot.friends().search('CameloG')[0]
f2 = bot.friends().search('源泉olivia')[0]
f3 = bot.friends().search('卡莫拉内西')[0]
f = {f1,f2,f3}

while(1):
    #获取澳元汇率    
    #r = urllib.request.urlopen("https://finance.google.cn/finance/converter?a=1&from=AUD&to=CNY")
    #s = r.read();
    #解析汇率
    

    #获取BTCMarket 瑞波澳元价格
    print('获取BTCMarket 瑞波澳元价格')
    #res = client.get_market_tick('XRP', 'AUD')
    try:
        res1 = urllib.request.urlopen("https://api.btcmarkets.net/market/XRP/AUD/tick")
    except urllib.request.HTTPError(e):
        print(e.code)
    except urllib.request.URLError(e):
        print(e.reason)
    else:
        print("OK")
 
    res = res1.read().decode('utf-8')
    res = json.loads(res)
    res1.close()
    #获取中币 QC报价
    print('正在获取中币的报价')
    try:
        response = urllib.request.urlopen('http://api.zb.com/data/v1/ticker?market=xrp_qc')
    except urllib.request.HTTPError(e):
        print(e.code)
    except urllib.request.URLError(e):
        print(e.reason)
    else:
        print("OK")

    b=str(response.read().decode("utf-8"))
    result = json.loads(b)
    #关闭连接
    #res.close()
    response.close()

    price = {}
    price['AUD'] = res['lastPrice']
    price['QC'] =  float(result['ticker']['buy'])
    price['profit'] =  price['QC']*0.99*0.998-price['AUD']*5.13*1.0085
    price['rate'] = price['profit'] /(price['AUD']*5.13*1.0085)
    #给朋友提醒价格
    print('统计价格')
    for x in f:
        x.send('微信机器人BTC Markets澳元报价 %f AUD，中币买一价格 %f QC,存在差价 %f ,收益率为 %f' % ( price['AUD'] ,  price['QC'],price['profit'],price['rate']))
    time.sleep(300)

