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
f = {f1,f2}
for i in range(50):
    #获取澳元汇率    
    #r = urllib.request.urlopen("https://finance.google.cn/finance/converter?a=1&from=AUD&to=CNY")
    #s = r.read();
    #解析汇率
    

    #获取BTCMarket 瑞波澳元价格
    #print('获取BTCMarket 瑞波澳元价格')
    #res = client.get_market_tick('XRP', 'AUD')
    res = urllib.request.urlopen("https://api.btcmarkets.net/market/XRP/AUD/tick")
    res = res.read().decode('utf-8')
    res = json.loads(res)

    #获取中币 QC报价
    print('正在获取中币的报价')
    response = urllib.request.urlopen('http://api.zb.com/data/v1/ticker?market=xrp_qc')

    b=str(response.read().decode("utf-8"))
    result = json.loads(b)
    #关闭连接
    #res.close()
    response.close()

    price = {}
    price['AUD'] = res['lastPrice']
    price['QC'] =  float(result['ticker']['buy'])
    price['profit'] =  price['QC']*0.99-price['AUD']*5.15
    price['rate'] = price['profit'] /(price['AUD']*5.15)
    #给朋友提醒价格
    for x in f:
        x.send('微信机器人BTC Markets澳元报价 %f AUD，中币买一价格 %f QC,存在差价 %f ,收益率为 %f' % ( price['AUD'] ,  price['QC'],price['profit'],price['rate']))
    time.sleep(300)


