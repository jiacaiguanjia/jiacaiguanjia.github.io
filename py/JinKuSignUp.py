from  multiprocessing import Process,Pool
import time
import urllib.request
import urllib.parse
from http import cookiejar
import datetime
import numpy as np

st_time = datetime.datetime(2020,5,13,21,9,0,0)
end_time = datetime.datetime(2020,5,13,21,11,0,0)

cookie_str = 'gr_user_id=d3349930-8483-4458-ad97-e10da2c9555e; SERVERID=eb82104259da493cf985864c9a1bc0e9|1589361830|1589361770; JSESSIONID=8B0F2BBF7E8C8C4CA947E7BE31AAC919; SESSION_COOKIE=15; ssoTGC=HWYST7im26de7amP9qU%2BCOzChlYznVARZNImZjgOsrkD6JE56Gv0fBrmSyZs%2BralNdz2fkQN7pJo%0Apw31fOGu69zQDnM2ICdq1rLzzVMBYBuhQoXjT21hRB8%2FXI2u%2B6VNtiZkrxDjYhx%2FYKs4Umor9rtf%0A5ajKQieI; ssoTGCU=8j%2BVb1O%2FC2TVEcaXNh%2BBV2vsdCZZ%2FJMpZ35dt5bFwA%2FaB917f8PhbxaOM5W6U8vc%2Bxb1nhTHsRqj%0As0W7zpztO%2FTE5%2FI2q5QBflQkO6NfuRpQvUMwWub1Mwa2cDToF9PU%2FYOr379Iw4%2BFouIGXrr%2F1CY1%0A5uyX%2FaE9ZWZW4t45N%2BfQU0%2BAd5QBASkXtitSC9jzBRhmnquKmB9hEfYt76EfJ1uffXtrHqDnEtXB%0ABw%2Fl95dcvFDqqIsI5Y815et7hg48WF7XXNIQ6a1sFkM8ranzKZ4fomtKBL2727ADIS1fgCOtMrfL%0AsuqgYOjRMrQNmurHbEheBju%2Bpww%2B1svPK7HnvA3hX7cgULuft5VnEj%2FSLYFhIV6yHjFsWCoDi22s%0AjRz5krwB09ULaSks0eCIPE30JXOUfEcyzJrOEoAtGZJTF5SaW5McAXZYwllA93rRaEhGf5yoRKkc%0AG%2FLH6mGNoNa7ZhZ281taEeH73vqQ56NZIPptbKhX0JympY2vm3rx8F1RtqaW05z%2FLs6VPD6xC%2BYn%0A7X%2BQzvf0WVMraOPwe8hSqqeNNPe%2B75BGUg%3D%3D; ssoTGCSYN=DPT; orderWindow=1'



def get_act_list(min_limit=1, max_limit=100):
    act_id = [i for i in range(min_limit,max_limit)]
    for act_loc in range(len(act_id)):
        act_url = "https://www.jinku.com/activity/%s/" % str(act_id[act_loc])
        act_req = urllib.request.Request(url=act_url, method='GET')
        try:
            act_response = urllib.request.urlopen(act_req)
            act_id[act_loc] = 0
        except Exception as e:
            continue

    for i in range(100):
        try:
            act_id.remove(0)
        except Exception as e:
            break
        
    return act_id
	
	
	
def signUp(act_id, cookie_str):
    
    # headers and data setting
    url = "https://www.jinku.com/activity/signup/"
    data_dict = {'debug':''}
    headers_dict = {}
    headers_dict['Host']='www.jinku.com'
    headers_dict['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
    headers_dict['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers_dict['Accept-Language']='zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    headers_dict['Accept-Encoding']='gzip, deflate, br'
    headers_dict['Connection']='keep-alive'
    headers_dict['Upgrade-Insecure-Requests']='1'

    headers_dict['Pragma']='no-cache'
    headers_dict['Content-Type']='application/x-www-form-urlencoded'
    headers_dict['Content-Length']='21'
    headers_dict['Origin']='https://www.jinku.com'
    headers_dict['Cache-Control']='no-cache'

    headers_dict['Referer'] = 'https://www.jinku.com/activity/%s/' % str(act_id)
    headers_dict['Cookie'] = cookie_str
    data_dict['activity_id'] = int(act_id)

    data_dict_urlencode = urllib.parse.urlencode(data_dict).encode('utf-8')
    
    req = urllib.request.Request(url=url, method='POST', headers=headers_dict, data=data_dict_urlencode)
    
    try:
        response = urllib.request.urlopen(req)
    except Exception as e:
        print(e)
        return act_id, 0, 0
#     print(html)
    return act_id, response.status,response
	
	
	
def run_one_list(act_id, st_time, end_time):
    while True:
        if (datetime.datetime.now()>end_time):
            break
        elif (datetime.datetime.now()<st_time):
            continue

        print('启动')
        print(datetime.datetime.now())
        for i in act_id:
            signUp(i, cookie_str)
        print(datetime.datetime.now())

    print("end")
	


if __name__=="__main__":
    print(datetime.datetime.now())
    act_id = get_act_list()
    act_id
    print(datetime.datetime.now())
    act_list = []
    group_num = int(np.ceil(len(act_id)/10))
    for i in range(group_num):
        print(i)
        print(act_id[i*10:i*10+10])
        act_list.append(act_id[i*10:i*10+10])
    
    def Bar(arg):
        print('-->exec done:',arg)
 
    pool = Pool(group_num)
 
    for i in range(group_num):
        pool.apply_async(func=run_one_list, args=(act_list[i],st_time, end_time, ),callback=Bar)
        #pool.apply(func=Foo, args=(i,))

    print('end')
    pool.close()
    pool.join()#进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
