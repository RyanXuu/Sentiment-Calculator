from sentiment_analysis import compute_tweets
from sentiment_analysis import printer

fileName = input("Please enter a tweets file: ")
keyName = input("Please enter a key: ")
finalAnswer = compute_tweets(fileName, keyName)

finalAnswer = list(finalAnswer)
for i in range(0,len(finalAnswer)):
    finalAnswer[i] = list(finalAnswer[i])

try:
    Eastern = finalAnswer[0]
    Eastern.append("Eastern")
    Central = finalAnswer[1]
    Central.append("Central")
    Mountain = finalAnswer[2]
    Mountain.append("Mountain")
    Pacific = finalAnswer[3]
    Pacific.append("Pacific")

    print(" ")
    print("SENTIMENT VALUE RESULTS:")
    print(" ")
    printer(Eastern)
    printer(Central)
    printer(Mountain)
    printer(Pacific)

except IndexError:
    print(finalAnswer)




