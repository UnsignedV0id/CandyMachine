import re
tokens = open("tokens.txt", "w")

def checkNumeric(_string):
    isNumeric = False
    if(re.search(r'^((0[by])?((([0-1]+)(_?))*))?$', _string)): isNumeric = True #binário
    elif(re.search(r'^((0[dt])?((([0-9]+)(_?))*))?$', _string)): isNumeric = True #decimal
    elif(re.search(r'^((0[oq])?((([0-7]+)(_?))*))?$', _string)): isNumeric = True #octal
    elif(re.search(r'^((0[h])?((([0-9A-Fa-f]+)(_?))*))?$', _string)): isNumeric = True #hexa
    elif(re.search(r'^((([0-1]*_?)*)[by]?)?$', _string)): isNumeric = True #bin letra
    elif(re.search(r'^((([0-9]*_?)*)[dt]?)?$', _string)): isNumeric = True #deci letra
    elif(re.search(r'^((([0-7]*_?)*)[oq]?)?$', _string)): isNumeric = True #octal letra
    elif(re.search(r'^((([0-9A-Fa-f]*_?)*)[h]?)?$', _string)): isNumeric = True #hexaletra 
    elif(re.search(r'^[0-9]*.?(_?)*[0-9]+(_?)*$', _string)): isNumeric = True #floating point 

    return isNumeric


def writeToken(id_,type_,line_,symbol_):
    buffer = 'ID: {:<3} TYPE: {:<4} LINE: {:<7} SYMBOL: {} \n'.format(id_,type_,line_,symbol_)
    tokens.write(buffer)

def fillTokens(typeOfToken,listToFill):
    startRead = False
    with open("tokensList.txt","r") as tokensList:

        for line in tokensList:
            if(startRead):
                listToFill.append(line.replace("\n", ""))
            if(typeOfToken.lower() in line.lower()): startRead = not startRead
        listToFill.pop()
        return listToFill

blank = [" ", '\t']
comments = [';']
operators = ["+", "-", "*", "/", '&', '|', ">" , "<" , "%", "!" , "^", ">>", "<<"] #double bitwise used for verify and to match > >>
specialChar = ['(', ')', '[', ']', ',', '$', ]

separators = []
separators.extend(blank)
separators.extend(comments)
separators.extend(operators)
separators.extend(specialChar)

keywords = []
keywords = fillTokens("keywords", keywords)

tokenId = 0

tokenBuffer = ''


with open('code.asm') as asmCode:
    asmLines = asmCode.readlines()

for lineNum, line in enumerate(asmLines, start=1):

    charPos = 0 #char pointer
    tokenBuffer = ''

    if(lineNum <=700 ): #? remove this
        
        while(charPos != len(line)):

            #? V lines under this are commented, if the assemble code requires the line to end with ; uncomment 

            # if(charPos == len(line) - 1 and line[charPos] != ";"): #* GUARANTEE THAT LINES END WITH ;
            #     writeToken(tokenId,"ERR", str(lineNum)+":"+str(charPos + 1), "MISSING ; END OF LINE") #? KEEP EYE ON THIS
            #     break #! THIS IS NOT NECESSARY SINCE CODE SHOULD HALT HERE

            if(line[charPos] in comments): #! LINE END OR COMMENT
                writeToken(tokenId,"SYM", str(lineNum)+":"+str(charPos - len(tokenBuffer)), ";") #* SPECIAL CHAR
                break

            elif(line[charPos] == '"'): #* CATCHES STRINGS
                    tokenBuffer += str(line[charPos])
                    charPos+=1
                    while(line[charPos] != '"'):
                        if(line[charPos] == '\n'):
                            writeToken(tokenId,"ERR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), "MISSING CLOSING \"") # ! ERROR IF MISSING END OF STRING
                            tokenId +=1
                            break
                        tokenBuffer += str(line[charPos])
                        charPos+=1
                    tokenBuffer+='"'
                    charPos+=1
                    writeToken(tokenId,"STR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), tokenBuffer) #* STRINGS
                    if(lineNum == len(asmLines)  and charPos == len(line) ): break #exits if last char on file
                    tokenBuffer = ""

            elif(line[charPos] == "'"): #* CATCHES ASCII LITERALS
                    tokenBuffer += str(line[charPos])
                    charPos+=1
                    while(line[charPos] != "'"):
                        if(line[charPos] == '\n'):
                            writeToken(tokenId,"ERR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), "MISSING CLOSING \"") # ! ERROR IF MISSING END OF STRING
                            tokenId +=1
                            break
                        tokenBuffer += str(line[charPos])
                        charPos+=1

                    tokenBuffer+="'"
                    charPos+=1
                    writeToken(tokenId,"STR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), tokenBuffer) #* STRINGS
                    tokenId +=1
                    if(lineNum == len(asmLines)  and charPos == len(line) ): break #exits if last char on file
                    tokenBuffer = ""

            elif(line[charPos] == "`"): #* UNICODE LITERALS
                    tokenBuffer += str(line[charPos])
                    charPos+=1
                    while(line[charPos] != "`"):
                        if(line[charPos] == '\n'):
                            writeToken(tokenId,"ERR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), "MISSING CLOSING \"") # ! ERROR IF MISSING END OF STRING
                            tokenId +=1
                            break
                        tokenBuffer += str(line[charPos])
                        charPos+=1
                    tokenBuffer+="`"
                    charPos+=1
                    writeToken(tokenId,"STR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), tokenBuffer) #* STRINGS
                    tokenId +=1
                    if(lineNum == len(asmLines)  and charPos == len(line) ): break #exits if last char on file
                    tokenBuffer = ""


            elif(line[charPos] in ['<', '>']): #* CATCHES BITWISE OPERATOS
                    if(line[charPos] == ">" and line[charPos+1] == ">"):
                        writeToken(tokenId,"OPR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), ">>")
                        charPos +=2
                        tokenId +=1
                    elif(line[charPos] == "<" and line[charPos+1] == "<"):
                        writeToken(tokenId,"OPR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), ">>")
                        charPos +=2
                        tokenId +=1
                    else:
                        writeToken(tokenId,"ERR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), "MISSING DOUBLE OPERATOR BITWISE")# ! ERROR IF MISSING END OF OPERATOR
                        charPos+=1 #! THIS IS NOT NECESSARY SINCE THE CODE SHOULD HALT HERE!!!!
                        tokenId +=1
            
            elif(line[charPos] in operators): #* CATCHES OPERATORS
                writeToken(tokenId,"OPR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), line[charPos])
                tokenId +=1
                print(line[charPos])
                charPos+=1

            elif(line[charPos] in blank): charPos +=1 # skips spaces

            elif(line[charPos] in specialChar): #* CATCHES SPECIAL SYMBOLS
                writeToken(tokenId,"SYM", str(lineNum)+":"+str(charPos - len(tokenBuffer)), line[charPos])
                tokenId +=1
                print(line[charPos])
                charPos+=1
            
            elif(line[charPos] == "\n"): #* DETECTS LINE FEEDS \n
                writeToken(tokenId,"SYM", str(lineNum)+":"+str(charPos - len(tokenBuffer)), "\\n")
                tokenId +=1
                print("linefeed")
                charPos+=1

            else:

                while(line[charPos] not in separators and line[charPos] != "\n"):
                    tokenBuffer += str(line[charPos])
                    charPos+=1
                    if(lineNum == len(asmLines)  and charPos == len(line) ): break #exits if last char on file
                
                if(checkNumeric(tokenBuffer)): #* NUMERIC
                    writeToken(tokenId,"NUM", str(lineNum)+":"+str(charPos - len(tokenBuffer)), tokenBuffer)
                    tokenId +=1


                elif(tokenBuffer in keywords): #* KEYWORDS
                    writeToken(tokenId,"KEY", str(lineNum)+":"+str(charPos - len(tokenBuffer)), tokenBuffer)
                    tokenId +=1

                elif(re.search(r'^[a-zA-Z|_.][a-zA-Z|_.|\d]+[:]?$', tokenBuffer) or re.search(r'^0x[0-9a-f]+$', tokenBuffer)): #* IDENTFIERS
                    writeToken(tokenId,"IDN", str(lineNum)+":"+str(charPos - len(tokenBuffer)), tokenBuffer)
                    tokenId +=1

                else:
                    writeToken(tokenId,"ERR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), tokenBuffer)
                    tokenId +=1
                print(tokenBuffer)
                tokenBuffer = ""

            

        




#https://www.nasm.us/xdoc/2.10.09/html/nasmdoc3.html#:~:text=Floating%2Dpoint%20constants%20are%20expressed,declares%20a%20floating%2Dpoint%20constant.