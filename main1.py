from btcmarkets import BTCMarkets
import urllib.request,json
from wxpy import *
import config
import time
api_key = config.api_key
private_key= config.private_key

#client = BTCMarkets(api_key, private_key)
#client.account_balance()
#client.trade_history("AUD", "XRP", 10, 1088157044)

pass
#print client.trade_history('AUD', 'BTC', 10, 1)
#print client.order_detail([1234, 213456])
#print client.order_create('AUD', 'LTC', 100000000, 100000000, 'Bid', 'Limit', '1')
#res = client.get_market_tick('ETH','AUD')
#print(res)
#print(res['lastPrice'])






#获取BTCMarket 瑞波澳元价格
def get_bitmarkets_price(coin1,coin2):
    print('获取BTCMarket 瑞波澳元价格')
    #res = client.get_market_tick('XRP', 'AUD')
    url = "https://api.btcmarkets.net/market/%s/%s/tick" % (coin1,coin2)
    try:
        res1 = urllib.request.urlopen(url)
    except urllib.request.HTTPError as e:
        print(e.code)
        return -1
    except urllib.request.URLError as e:
        print(e.reason)
        return -1
    else:
        print("OK")
        res = res1.read().decode('utf-8')
        res = json.loads(res)
        res1.close() 
        return res

    

#获取中币 QC报价
def get_zb_price(coin1,coin2):
    url = 'http://api.zb.com/data/v1/ticker?market=%s_%s' % (coin1,coin2)
    print('正在获取中币的报价')
    try:
        response = urllib.request.urlopen(url)
    except urllib.request.HTTPError as e:
        print(e.code)
        return -1
    except urllib.request.URLError as e:
        print(e.reason)
        return -1
    else:
        print("OK")
        b=str(response.read().decode("utf-8"))
        result = json.loads(b)
        #关闭连接
        #res.close()
        response.close()
        return result



def WexinNote():
    #初始化一个微信机器人
    bot = Bot();
    #扫描二维码登陆
    #将孙，袁全加到my_friend里面
    f1 = bot.friends().search('CameloG')[0]
    #f2 = bot.friends().search('源泉olivia')[0]
    f3 = bot.friends().search('卡莫拉内西')[0]
    f = {f1,f3}

    AUD_CNY = 4.95
    while(1):
        res = get_bitmarkets_price('XRP','AUD')
        result = get_zb_price('xrp','qc')
        if(res != -1 and result !=-1):
            price = {}
            price['AUD'] = res['lastPrice']
            #中币买一
            price['QC_buy'] =  float(result['ticker']['buy'])
            #中币卖一
            price['QC_sell'] =  float(result['ticker']['sell'])
  
            #计算人民币利润
            price['profit'] =  price['QC_buy']*0.99*0.998-price['AUD']*AUD_CNY*1.0075
            price['rate'] = price['profit'] /(price['AUD']*AUD_CNY*1.0075)
  
            #计算折合汇率
            price['aud_rate'] = (price['QC_sell']*1.002)/(price['AUD']*(0.9925))
    
            #给朋友提醒价格
            print('统计价格计算人民币套利价格')
            for x in f:
                x.send('马克思(人民币套利)：BTC Markets澳元报价 %f AUD, 汇率按照【4.95】算 ,中币【买一】%f QC,中币【卖一】 %f,存在差价 %f , CNY收益率为 %f, 折合汇率 %f' % ( price['AUD'] ,  price['QC_buy'],price['QC_sell'],price['profit'],price['rate'],price['aud_rate'] ))
        else:
            print('遇到了异常,进行下一次处理!')


        res = get_bitmarkets_price('XRP','BTC')
        result = get_zb_price('xrp','btc')
        if(res != -1 and result !=-1):
            price = {}
            price['btc_bid'] = res['bestBid']*100000000
            price['btc_ask'] = res['bestAsk']*100000000
            #中币买一
            price['btc_sell'] =  float(result['ticker']['sell'])*100000000
            price['btc_buy'] =  float(result['ticker']['buy'])*100000000
  
            #给朋友提醒价格
            print('统计价格计算人民币套利价格')
            for x in f:
                x.send('斯芬克斯套利(比特币) 孙买--->何卖：BTC Markets 【卖一】 %f 聪, 中币【买一】比特币报价 %f 聪, 赚： %f 聪。' % ( price['btc_ask'] ,  price['btc_buy'],price['btc_buy']*0.997-price['btc_ask']*1.0075 ))
                x.send('尼古拉斯套利(比特币) 何买--->孙卖：BTC Markets 【买一】 %f 聪, 中币【卖一】比特币报价 %f 聪, 赚： %f 聪。' % ( price['btc_sell'] ,  price['btc_sell'],price['btc_bid']*0.9925-price['btc_sell']*1.003))
        else:
            print('遇到了异常,进行下一次处理!')
        
        print('发送完毕')
        time.sleep(300)



#WexinNote()

