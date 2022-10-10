from cs50 import get_string

cardNum = get_string("Number: ")

cardNum = cardNum.replace("-", "")

if len(cardNum) != 15 and len(cardNum) != 13 and len(cardNum) != 16:
    print('INVALID')
    exit(0)
    
if cardNum[:2] in ['34', '37']:
    cardComp = 'AMEX'
elif cardNum[:2] in ['51', '52', '53', '54', '55']:
    cardComp = 'MASTERCARD'
else:
    cardComp = 'VISA'

reversedCard = cardNum[::-1]
reversedCard = list(reversedCard)


for i in range(len(reversedCard)):
    if (i % 2) == 1:
        if ((int(reversedCard[i]) * 2) >= 10):
            reversedCard[i] = (int(reversedCard[i]) * 2) % 10 
            reversedCard[i] += 1
        else:
            reversedCard[i] = int(reversedCard[i]) * 2

numberSum = 0

for i in range(len(reversedCard)):
    numberSum += int(reversedCard[i])
    
numberSum = str(numberSum)
isValid = False


if numberSum[len(numberSum) - 1] == '0':
    isValid = True
    
if isValid :
    print(cardComp)
else:
    print("INVALID")
    