import json

helper = local_import("helper")

## function the the first time the page is loaded
def index():
    ## index represents the index of tweet given to the analyst, this needs to be decided by the decision module but for now we are assuming it to be sequential
    session.index = 0
    ## flag represents whether the current tweet is marked as contining PII or not. True => contains PII
    session.flag = False
    ## ruleList is list of rules as the name suggest
    session.ruleList = []
    tweet, session.tweet = helper.getTweet(session.index)
    return dict(message=XML(tweet))

## function called which returns rules when new words are highlighted / unhighlighted
def back():
    ## arr is the array of words highlighted by the analyst in the current tweet
    lis = json.loads(request.vars.arr)
    lis.sort()
    ## the function in map needs to be changed, ie., op2 and op3 needs to be replaced with actual generalization/features of the words.
    lis = map(lambda x: [session.tweet[x], 'op2', 'op3'], lis)
    return  json.dumps({"arr":json.dumps(lis)})

## function called when a rule is finalized and more rules are left in the tweet
def nextrule():
    ## words is an array of rule elements encoded as a string, lis is the decoded array.
    lis = request.vars.words.split(',')
    ## if the rule is an empty rule then chuck
    if len(request.vars.words) == 0:
        return None
    ## if the rule is not an empty rule then it implies that the tweet contains some PII
    session.flag = True
    ## base is an array of rule root elements ecoded as string and base is the decoded array.
    roots = request.vars.base.split(',')
    paired = []
    ## this loop zips the two arrays
    for i in xrange(len(lis)):
        ## first element is a boolean which represents if the rule element is the original plaintext or a genralization
        paired += [(lis[i] == roots[i], lis[i])]
    ## rule is the instance of class Rule
    rule = helper.Rule(paired)
    ## add use to the current session
    session.ruleList.append(rule)


## function called when a tweet has been completely analyzed
def nexttweet():
    ## pushes all the rules learnt till now in the database if there were any
    if session.flag:
        helper.store(session.ruleList, session.index)
    ## recalculate score of each tweet
    # helper.rank()
    ## this needs to change, a call to decision unit is needed, for now we are assuming sequential call
    session.index += 1
    tweet, session.tweet = helper.getTweet(session.index)
    session.ruleList = []
    ## revert the PII flag to False ie., no PII
    session.flag = False
    return XML(tweet)
