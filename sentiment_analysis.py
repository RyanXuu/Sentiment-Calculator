#punctuation
import string


def compute_tweets(tweetFileName,keyFileName):
    keyDict = keyReader(keyFileName)

    #keywords of each region
    pValueList = []
    mValueList = []
    cValueList = []
    eValueList = []

    #number of keywords of each region
    pKeyCount = 0
    mKeyCount = 0
    cKeyCount = 0
    eKeyCount = 0

    #number of tweets of each region
    pTweetCount = 0
    mTweetCount = 0
    cTweetCount = 0
    eTweetCount = 0

    try:
        tweetList = open(tweetFileName, "r", encoding="utf‐8")
        for line in tweetList:
            line = tweetLister(line)
            latitude = line[0]
            longitude = line[1]
            timezone = timeZoneFinder(latitude, longitude)
            if timezone:
                sentimentValue, keywordCount = sentimentValueFinder(line, keyFileName)

                #handles all tweets with sentiment value > 0
                try:
                    tweetValue = sentimentValue / keywordCount
                    if timezone == "pacific":
                        pTweetCount += 1
                        pValueList.append(tweetValue)
                        if tweetValue > 0:
                            pKeyCount += 1
                    elif timezone == "mountain":
                        mTweetCount += 1
                        mValueList.append(tweetValue)
                        if tweetValue > 0:
                            mKeyCount += 1
                    elif timezone == "central":
                        cTweetCount += 1
                        cValueList.append(tweetValue)
                        if tweetValue > 0:
                            cKeyCount += 1
                    elif timezone == "eastern":
                        eTweetCount += 1
                        eValueList.append(tweetValue)
                        if tweetValue > 0:
                            eKeyCount += 1

                #handles all tweets with no sentiment value
                except ZeroDivisionError:
                    if timezone == "pacific":
                        pTweetCount += 1
                        pValueList.append(0)
                    if timezone == "mountain":
                        mTweetCount += 1
                        mValueList.append(0)
                    if timezone == "central":
                        cTweetCount += 1
                        cValueList.append(0)
                    if timezone == "eastern":
                        eTweetCount += 1
                        eValueList.append(0)

        #calculates the average tweet value of a region
        if pTweetCount == 0:
            pAverage = 0
        else:
            pAverage = (sum(pValueList))/pKeyCount

        if mTweetCount == 0:
            mAverage = 0
        else:
            mAverage = (sum(mValueList))/mKeyCount

        if cTweetCount == 0:
            cAverage = 0
        else:
            cAverage = (sum(cValueList))/cKeyCount

        if eTweetCount == 0:
            eAverage = 0
        else:
            eAverage = (sum(eValueList))/eKeyCount


        #Creates required tuples
        Eastern = (eAverage, eKeyCount, eTweetCount)
        Central = (cAverage, cKeyCount, cTweetCount)
        Mountain = (mAverage, mKeyCount, mTweetCount)
        Pacific = (pAverage, pKeyCount, pTweetCount)

        return Eastern, Central, Mountain, Pacific



    except IOError:
        return []

#this is for reading tweets
def tweetLister(line):
    #makes line into a list
    tweetList = line.split(" ")
    tweetList[-1] = tweetList[-1].strip("\n")

    #turns tweetList lowercase and removes punctuation
    for i in range(2,len(tweetList)):
        tweetList[i] = tweetList[i].strip(string.punctuation).lower()
    for i in range(0,2):
        tweetList[i] = tweetList[i].strip("[")
        tweetList[i] = tweetList[i].strip(",")
        tweetList[i] = tweetList[i].strip("]")

    return tweetList



#this is for reading keys
def keyReader(keyFileName):
    try:
        keyFile = open(keyFileName, "r",encoding="utf‐8")
        keyDictionary = {}
        for line in keyFile:
            keyList = line.split(",")
            keyList[1] = int(keyList[1].strip("\n"))
            keyDictionary[keyList[0]] = keyList[1]
        return keyDictionary
    except IOError:
        return []

#this determines timezone of a tweet
def timeZoneFinder(latitude,longitude):
    if 24.66085 < float(latitude) < 49.189787 and -125.242264 < float(longitude) < -115.236428:
        return "pacific"
    elif 24.66085 < float(latitude) < 49.189787 and -115.236428 < float(longitude) < -101.998892:
        return "mountain"
    elif 24.66085 < float(latitude) < 49.189787 and -101.998892 < float(longitude) < -87.518395:
        return "central"
    elif 24.66085 < float(latitude) < 49.189787 and -87.518395 < float(longitude) < -67.444574:
        return "eastern"
    else:
        return False

#this determines the sentiment value of a tweet
def sentimentValueFinder(line, keyFileName):
    keyDictionary = keyReader(keyFileName)
    sentimentValue = 0
    wordCount = 0
    for tweetWord in line:
        for keyWord in keyDictionary:
            if tweetWord == keyWord:
                sentimentValue += keyDictionary[keyWord]
                wordCount += 1
    return sentimentValue, wordCount

#this is for printing the final answer
def printer(Region):
    print("The happiness score for the", Region[3], "region is: ", Region[0])
    print("The number of keywords tweets in", Region[3], "region is: ", Region[1])
    print("The total number of tweets in", Region[3], "is: ", Region[2])
    print(" ")

