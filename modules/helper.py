from pymongo import MongoClient



client = MongoClient('localhost', 27017)
collection = client.pii.tweets.features
rdb = client.rules.list



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
    def encode(self):
        return {'isTer': self.isTerminal, 'text' : self.text}
    def out(self):
        print self.isTerminal, self.text

def decodeWord(a):
    return Word(a['isTer'], a['text'])

class Rule:
    def __init__(self, lis):
        self.words = [Word(x[0], x[1]) for x in lis]
    def match(self, tweet):
        i, j = 0, 0
        while i < len(self.words) and j < len(tweet['features']):
            if self.words[i].match(tweet['features'][j]):
                i += 1
                j += 1
            else:
                j += 1
        return i == len(self.words)
    def encode(self):
        return [x.encode() for x in self.words]

def decodeRule(a):
    b = [decodeWord(x) for x in a]
    ret = Rule([])
    ret.words = b
    return ret


def tag(s):
    s = s.replace(',', ' , ').replace('.', ' . ')
    lis = s.split()
    ret = ''
    cnt = 0
    for x in lis:
        ret += '<span onclick="pop(' + str(cnt) + ')" id="' + str(cnt) + '" class="words">' + x + '</span> '
        cnt += 1

    return ret, lis

def getTweet(idx):
    s = collection.find()[idx]['text']
    return tag(s)

def store(ruleList, idx):
    for rule in ruleList:
        if rdb.find({'rule' : rule.encode()}).count() > 0:
            score = rdb.find_one({'rule': rule.encode()})['score'] + 2
            rdb.update({'rule': rule.encode()}, {'rule': rule.encode(), 'score': score})
        else:
            rdb.insert({ 'rule' : rule.encode(), 'score' : 10 })
    tweet = collection.find()[idx]
    for iter in rdb.find():
        x = decodeRule(iter['rule'])
        if x.match(tweet):
            y = iter
            y['score'] -= 1
            rdb.update({'_id': iter['_id']}, y)


## calculate score for each tweet
def calculateScore(tweet):
    ret = 0
    for x in rdb.find():
        y = decodeRule(x['rule'])
        if y.match(tweet):
            ret += x['score']
    return ret

## this function updates score of each tweet
def rank():
    for x in collection.find():
        score  = calculateScore(x)
        y = x
        y['score'] = score
        collection.update({'_id': x['_id']}, y)
