import urllib.request as ur
import urllib.error as uerror
import urllib.parse as up

import decimal

import LocalException


struct = ['股票名字','今日开盘','昨日收盘','当前','今日最高','今日最低','竞买价','竞卖价','成交的股票数','成交金额','买一','买一报价','买二','买二报价',\
            '买三','买三报价','买四','买四报价','买五','买五报价','卖一','卖一报价','卖二','卖二报价','卖三','卖三报价','卖四','卖四报价','卖五','卖五报价','日期','时间','unknow']


rowitems = ['股票名字','涨跌幅','当前','今日开盘','昨日收盘','今日最高','今日最低','卖一','卖一报价']



class SimpleModel:
    
    def __init__(self):        
        self._url = "http://hq.sinajs.cn/list="
        lines = open('code','r').readlines()

        for item in lines:
            self._url +=  item.strip()+','

    def Construct(self,result):
        
        if len(result) != 3:
            raise LocalException.NormalException('http response error')
        
        var = result[1]
        var = var.split(',')
        if(len(var) != len(struct)):
            raise LocalException.NormalException('format not match') 
        
        row = list()

        data = self.ParseData(var)

        for key in rowitems:
            row.append(data[key])
        
        return row

    def ParseData(self,var):

        if(len(var) != len(struct)):
            raise LocalException.NormalException('format not match') 

        data = dict()

        #字符串转换为数字
        for key ,value in zip(struct,var):
            try:
                data[key] = round(float(value),2)
            except ValueError:
                data[key] = value

        if data['当前'] == 0 :
            data['涨跌幅'] = 0
        else:
            data['涨跌幅'] = (data['当前']-data['昨日收盘'])/data['昨日收盘']

        #数字转换为字符串
        data['涨跌幅'] = str(round(data['涨跌幅']*100,2))+'%'
        for key ,value in zip(struct,var):
            data[key] = str(data[key])                    
        
        return data
            


    def Query(self):
        try:
            response = ur.urlopen(self._url)
            jsconts = response.read().decode('gbk').splitlines()
            counter = 1
            info = list()
            temp = str()
            for item in jsconts:
                var = item.split('"')
                data = self.Construct(var)
                info.append(tuple([data,counter]))
                counter += 1
            return info
        except Exception as e:
            print(e)
            pass
    
