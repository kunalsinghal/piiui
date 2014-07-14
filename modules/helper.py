from pymongo import MongoClient



client = MongoClient("localhost", 27017)
collection = client.pii.tweets.features



class Tweet:
    def __init__(self, lis):
        self.text = lis['text']
        self._id = lis['_id']
        self.id = lis['id']
        self.features = lis['features']

class Word:
    def __init__(self, isTer, text):
        self.isTerminal = isTer
        self.text = text
    def match(self, lis):
        if self.isTerminal:
            return lis[0] == self.text
        else:
            for x in lis:
                if x == self.text:
                    return True
            return False




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
