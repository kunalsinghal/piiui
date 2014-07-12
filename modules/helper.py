from pymongo import MongoClient
client = MongoClient("localhost", 27017)
collection = client.pii.tweets.features

def tag(s):
    s = s.replace(',', ' , ').replace('.', ' . ')
    lis = s.split()
    ret = ""
    cnt = 0
    for x in lis:
        ret += '<span onclick="pop(' + str(cnt) + ')" id="' + str(cnt) + '" class="words">' + x + '</span> '
        cnt += 1

    return ret, lis

def getTweet():
    s = collection.find_one()['text']
    return tag(s)
