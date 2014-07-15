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
    def match(self, word):
        if self.isTerminal:
            return self.text.lower() == word['string'].lower()
        else:
            for x in word.values():
                if x.lower() == self.text.lower():
                    return True
            return False

class Rule:
    def __init__(self, lis):
        self.words = [Word(x[0], x[1]) for x in lis]
    def match(self, tweet):
        i, j = 0, 0
        while i < len(self.words) and j < len(tweet.features):
            if self.words[i].match(tweet.features[j]):
                i += 1
                j += 1
            else:
                j += 1
        return i == len(self.words)


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
