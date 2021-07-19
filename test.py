import requests
import json
from concurrent.futures import ThreadPoolExecutor

# from uniswap import Uniswap

# response = requests.get("http://api.open-notify.org/astros.json")
# print(response)
# print(response.json())

# resp = requests.get("https://api.0x.org/swap/v1/quote?buyToken=DAI&sellToken=WETH&sellAmount=100000000000000000")
# print(resp)
# print(resp.json())
# print(resp.json()['price'])
def Convert(tup, di):
    for a in tup:
        di[a['symbol']] = float(a['price'])
    return di

def buildGraph(convertedArr, start, graph):
    graph[start]  = {}
    for i in convertedArr:
        graph[start][i] = convertedArr[i]
    return graph

def returnTokenPrices(sellToken):
    response = requests.get("https://api.0x.org/swap/v1/prices?sellToken=" + sellToken + "&perPage=100")
    jsonResponseArrx = response.json()['records']
    return jsonResponseArrx
def get_url(url):
    # ret = requests.get(url).json()['records']
    # dictt = {}
    # converted = Convert(ret, dictt)
    # return ret
    req = requests.get(url)
    if(req.status_code == 200):
        return req

def generateUrl(token):
    return "https://api.0x.org/swap/v1/prices?sellToken=" + token + "&perPage=1000"

def generateUrlList(listOfTokens):
    ret = []
    for i in listOfTokens:
        # if(len(ret) == 10):
        #     return ret
        ret.append(generateUrl(i))
    return ret
def makeConcurrentRequests(convertedArr):
    print('_ URL LIST')
    keys = list(convertedArr.keys())
    print(keys)
    print(type(keys))
    print(generateUrlList(keys))
    list_of_urls = generateUrlList(keys)
    print('END LIST')
    
    with ThreadPoolExecutor(max_workers=100) as pool:
        vx = list(pool.map(get_url,list_of_urls))
        print(len(vx))
        return list(filter(None, vx))


    

print('__________________')


# rsp = requests.get("https://api.0x.org/swap/v1/prices?sellToken=WETH&perPage=1000")
# jsonResponseArr = rsp.json()['records']
jsonResponseArr = returnTokenPrices('WETH')
print(type(jsonResponseArr))
print(len(jsonResponseArr))

parsed = set()

dic = {}
convertedArr = Convert(jsonResponseArr, dic)
print(convertedArr)
print("----")


#print(makeConcurrentRequests(convertedArr))
vxx = makeConcurrentRequests(convertedArr)
print(vxx)
print(len(vxx))
#print(rsp.json()['records'][0]['symbol'])

graph = {}


buildGraph(convertedArr, 'WETH', graph)
print(graph)
parsed.add('WETH')
v = 0

for i in convertedArr:
    print(i)
    v+=1
    if v == 1:
        break
    if i not in parsed:
        parsed.add(i)
        currentResponse = returnTokenPrices(i)
        freshdic = {}
        currentConvertedArr = Convert(currentResponse, freshdic)
        buildGraph(currentConvertedArr, i, graph)
print('FINAL')
#print(graph)

json_object = json.dumps(graph, indent = 4)  
print(json_object) 








