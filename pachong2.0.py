import requests
import json
import pymysql
def Down_data_1():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'
    }
    r = requests.get(url, headers)
    res = json.loads(r.text)
    data_res = json.loads(res['data'])
    return data_res


def Down_data_2():
    url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=statisGradeCityDetail'
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'
    }
    r = requests.get(url, headers)
    res = json.loads(r.text)
    return res['data']

def Down_data_3():
    url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province=%E5%8C%97%E4%BA%AC&'
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'
    }
    r = requests.get(url, headers)
    res = json.loads(r.text)
    return res['data']

def Parse_data1():
    data = Down_data_1()
    list = ['截至时间：' + str(data['lastUpdateTime']) + '\n'
                            '全国确诊人数：' + str(data['chinaTotal']['confirm']) + '\n'
                            '今日新增确诊：' + str(data['chinaAdd']['confirm']) + '\n'
                            '全国疑似：' + str(data['chinaTotal']['suspect']) + '\n'
                            '今日新增疑似：' + str(data['chinaAdd']['suspect']) + '\n'
                            '全国治愈：' + str(data['chinaTotal']['heal']) + '\n'
                            '今日新增治愈：' + str(data['chinaAdd']['heal']) + '\n'
                            '全国死亡：' + str(data['chinaTotal']['dead']) + '\n'
                            '今日新增死亡：' + str(data['chinaAdd']['dead']) + '\n']
    result = ''.join(list)
    sql = "truncate table txy.t_chinatotal;"
    Run_sql(sql)
    sql1 = "insert into txy.t_chinatotal(confirm,heal,dead,nowConfirm,suspect,nowSevere,importedCase,noInfect)" \
           " values ("+str(data['chinaTotal']['confirm'])+","+str(data['chinaTotal']['heal'])+","+str(data['chinaTotal']['dead'])+\
           ","+str(data['chinaTotal']['nowConfirm'])+","+str(data['chinaTotal']['suspect'])+","+str(data['chinaTotal']['nowSevere'])+\
           ","+str(data['chinaTotal']['importedCase'])+","+str(data['chinaTotal']['importedCase'])+")"
    Run_sql(sql1)
    sql2 = "truncate table txy.t_chinaadd;"
    Run_sql(sql2)
    sql3 = "insert into txy.t_chinaadd(confirm,heal,dead,nowConfirm,suspect,nowSevere,importedCase,noInfect)" \
           " values (" + str(data['chinaAdd']['confirm']) + "," + str(data['chinaAdd']['heal']) + "," + str(
        data['chinaAdd']['dead']) + \
           "," + str(data['chinaAdd']['nowConfirm']) + "," + str(data['chinaAdd']['suspect']) + "," + str(
        data['chinaAdd']['nowSevere']) + \
           "," + str(data['chinaAdd']['importedCase']) + "," + str(data['chinaAdd']['importedCase']) + ")"
    Run_sql(sql3)
    sql4 = "truncate table txy.t_upd_time;"
    Run_sql(sql4)
    sql5 = "insert into t_upd_time(update_time) select concat('统计日期:',now())"
    Run_sql(sql5)
def Parse_data2():
    data = Down_data_1()['areaTree'][0]['children']
    sql1 = "truncate table txy.t_area;"
    Run_sql(sql1)
    for item in data:
        list_city = [
                '地区: ' + str(item['name']) + '\n'
                ' 确诊人数：' + str(item['total']['confirm']),
                ' 新增确诊：' + str(item['today']['confirm']),
                ' 治愈：' + str(item['total']['heal']),
                #' 新增治愈：' + str(item['today']['heal']),
                ' 死亡：' + str(item['total']['dead']),
                #' 新增死亡：' + str(item['today']['dead']) + '\n'
        ]
        sql = "insert into t_area(name,total_confirm,today_confirm,total_heal,total_dead) values (" \
              "'%s',%s,%s,%s,%s)"%(str(item['name']),str(item['total']['confirm']),str(item['today']['confirm']),
                                str(item['total']['heal']),str(item['total']['dead']))
        Run_sql(sql)

def Parse_data3():
    data = Down_data_2()['statisGradeCityDetail']
    sql1 = "truncate table txy.t_graph;"
    Run_sql(sql1)
    for item in data:
        list_graph = [
                '地区: ' + str(item['city']) + '\n'
                '等级：' + str(item['grade']),
                '省：' + str(item['province']),
                '治愈：' + str(item['heal']),
                '新增：' + str(item['nowConfirm']) + '\n'
        ]
        print(list_graph)
        sql = "insert into t_graph(city,grade,province,heal,nowConfirm) values (" \
              "'%s','%s','%s',%s,%s)"%(str(item['city']),str(item['grade']),str(item['province']),str(item['heal']),str(item['nowConfirm']) )

        Run_sql(sql)



def Parse_data4():
    data = Down_data_3()
    sql1 = "truncate table txy.t_beijing;"
    Run_sql(sql1)
    for item in data:
        list_graph = [
                '年: ' + str(item['year']) + '\n'
                '日期：' + str(item['date']),
                '确诊人数：' + str(item['confirm']),
                 '新增人数：' + str(item['confirm_add']),
                 '现有人数：' + str(item['newConfirm']),
                '治愈：' + str(item['heal']),
                '死亡：' + str(item['dead']) + '\n'
        ]
        sql  = "insert into t_beijing (year,day,confirm,confirm_add,newConfirm,heal,dead)" \
               " values ('%s','%s','%s','%s','%s','%s','%s')"%(str(item['year']),str(item['date']),
                                                               str(item['confirm']),str(item['confirm_add']),
                                                               str(item['newConfirm']),str(item['heal']),
                                                               str(item['dead']))
        Run_sql(sql)

def Run_sql(sql):
    conn = pymysql.connect(host="localhost", user="bfd001", password="Liyong123!@#", database="txy", charset="utf8")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

print("begin")
Parse_data1()
Parse_data2()
Parse_data3()
Parse_data4()
print("end")
