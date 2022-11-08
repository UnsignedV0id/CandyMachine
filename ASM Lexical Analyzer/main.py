import re
import time
import os
import curses
from curses import wrapper

tokens = open("tokens.txt", "w")

#define screens
stdscr = curses.initscr()
codeDisplay = curses.newwin(20, 115, 0, 5)
tokenDisplay = curses.newwin(9, 115,21,0)

with open('code.asm') as asmCode:
    asmLines = asmCode.readlines()


def checkNumeric(_string):
    isNumeric = False
    if(re.search(r'^((0[by])?((([0-1]+)(_?))*))?$', _string)): isNumeric = True #binário
    elif(re.search(r'^((0[dt])?((([0-9]+)(_?))*))?$', _string)): isNumeric = True #decimal
    elif(re.search(r'^((0[oq])?((([0-7]+)(_?))*))?$', _string)): isNumeric = True #octal
    elif(re.search(r'^((0[h])?((([0-9A-Fa-f]+)(_?))*))?$', _string)): isNumeric = True #hexa
    elif(re.search(r'^((([0-1]*_?)*)[by]?)?$', _string)): isNumeric = True #bin letra
    elif(re.search(r'^((([0-9]*_?)*)[dt]?)?$', _string)): isNumeric = True #deci letra
    elif(re.search(r'^((([0-7]*_?)*)[oq]?)?$', _string)): isNumeric = True #octal letra
    elif(re.search(r'^((([0-9A-Fa-f]+_?)*)[h]?)?$', _string)): isNumeric = True #hexaletra 
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


## RENDER FUNCTIONS

def fillCode(startLine):
    codeDisplay.clear()
    for x in range(startLine, startLine + 20):
        stdscr.addstr(x - startLine,0 , str(x),curses.A_UNDERLINE)

    startLine = startLine -1
    for x in range(startLine,startLine + 20):
        if x <= len(asmLines) -1:
            codeDisplay.addstr(x - startLine, 0, asmLines[x].rstrip())
    codeDisplay.refresh()

def tokenDisplayUpdate(currentBuffer = "Empty line",found = "", type = "",id = ""):
    
    tokenDisplay.clear()
    tokenDisplay.addstr(2,0,"Token buffer: ")
    tokenDisplay.addstr(2,14,currentBuffer)
    if(found == ""):pass
    else:
        tokenDisplay.addstr(3,0,"TOKEN FOUND:", curses.A_BOLD)
        tokenDisplay.addstr(3,13,found, curses.A_BOLD)
        tokenDisplay.addstr(4,0,"TYPE:",curses.A_UNDERLINE)
        tokenDisplay.addstr(4,5,type,curses.A_ITALIC)
        tokenDisplay.addstr(5,0,"TOKEN ID: ")
        tokenDisplay.addstr(5, 10, id)
        
    tokenDisplay.addstr(8, 0,"PRESS TO STEP THROUGH",curses.A_STANDOUT)
    tokenDisplay.refresh()
    stdscr.getkey()
    

## RENDER FUNCTIONS

def main(stdscr):


    #starts screens with clear()
    stdscr.clear()
    codeDisplay.clear() 
    tokenDisplay.clear()
    stdscr.refresh()
    codeDisplay.refresh()
    tokenDisplay.refresh()

    error = False
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
    
    tokenDisplay.addstr(8,0,"Press any key to start",curses.A_STANDOUT)
    tokenDisplay.refresh()
    stdscr.getkey()

    for lineNum, line in enumerate(asmLines, start=1):
        if(error):break #checks if i got an error
        if lineNum == 1: 
            tokenDisplay.clear()
            tokenDisplay.refresh()

        else:
            tokenDisplayUpdate("NEXT LINE >>")

        fillCode(lineNum)
        
        charPos = 0 #char pointer
        tokenBuffer = ''

        while(charPos != len(line)):

            if(line[charPos] in comments): #* LINE END OR COMMENT
                tokenDisplayUpdate(";", ";", "SYM",str(tokenId))
                writeToken(tokenId,"SYM", str(lineNum)+":"+str(charPos - len(tokenBuffer)), ";") #* SPECIAL CHAR
                tokenId += 1
                break

            elif(line[charPos] == '"'): #* CATCHES STRINGS
                    tokenBuffer += str(line[charPos])
                    
                    charPos+=1
                    
                    while(line[charPos] != '"'):

                        if(line[charPos] == '\n'):

                            writeToken(tokenId,"ERR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), "MISSING CLOSING \"") #* ERROR IF MISSING END OF STRING
                            tokenDisplayUpdate(tokenBuffer,tokenBuffer,"ERR","ERR")
                            error=True
                            tokenId +=1
                            break

                        tokenDisplayUpdate(tokenBuffer)
                        tokenBuffer += str(line[charPos])
                        charPos+=1

                    if(error):break 
                    tokenBuffer+='"'
                    charPos+=1
                    tokenDisplayUpdate(tokenBuffer,tokenBuffer,"STR",str(tokenId))
                    writeToken(tokenId,"STR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), tokenBuffer) #* STRINGS
                    tokenId+=1
                    if(lineNum == len(asmLines)  and charPos == len(line) ): break #* exits if last char on file
                    tokenBuffer = ""

            elif(line[charPos] == "'"): #* CATCHES ASCII LITERAL
                    tokenBuffer += str(line[charPos])
                    
                    charPos+=1
                    
                    while(line[charPos] != "'"):

                        if(line[charPos] == '\n'):

                            writeToken(tokenId,"ERR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), "MISSING CLOSING \"") #* ERROR IF MISSING END OF STRING
                            tokenDisplayUpdate(tokenBuffer,tokenBuffer,"ERR","ERR")
                            error=True
                            tokenId +=1
                            break

                        tokenDisplayUpdate(tokenBuffer)
                        tokenBuffer += str(line[charPos])
                        charPos+=1
                        
                    if(error):break 
                    tokenBuffer+="'"
                    charPos+=1
                    tokenDisplayUpdate(tokenBuffer,tokenBuffer,"STR",str(tokenId))
                    writeToken(tokenId,"STR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), tokenBuffer) #* STRINGS
                    tokenId+=1
                    if(lineNum == len(asmLines)  and charPos == len(line) ): break #exits if last char on file
                    tokenBuffer = ""

            elif(line[charPos] == '`'): #* CATCHES UNICODE LITERAL
                    tokenBuffer += str(line[charPos])
                    
                    charPos+=1
                    
                    while(line[charPos] != '`'):

                        if(line[charPos] == '\n'):

                            writeToken(tokenId,"ERR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), "MISSING CLOSING \"") #* ERROR IF MISSING END OF STRING
                            tokenDisplayUpdate(tokenBuffer,tokenBuffer,"ERR","ERR")
                            error=True
                            tokenId +=1
                            break

                        tokenDisplayUpdate(tokenBuffer)
                        tokenBuffer += str(line[charPos])
                        charPos+=1
                        
                    if(error):break 
                    tokenBuffer+='`'
                    charPos+=1
                    tokenDisplayUpdate(tokenBuffer,tokenBuffer,"STR",str(tokenId))
                    writeToken(tokenId,"STR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), tokenBuffer) #* STRINGS
                    tokenId+=1
                    if(lineNum == len(asmLines)  and charPos == len(line) ): break #exits if last char on file
                    tokenBuffer = ""
            


            elif(line[charPos] in ['<', '>']): #* CATCHES BITWISE OPERATOS
                    if(charPos + 1 <= len(line) - 1 and line[charPos] == ">" and line[charPos+1] == ">"):
                        tokenDisplayUpdate(">>",">>","OPR",str(tokenId))
                        writeToken(tokenId,"OPR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), ">>")
                        charPos +=2
                        tokenId +=1

                    elif(charPos + 1 <= len(line) - 1 and line[charPos] == "<" and line[charPos+1] == "<"):
                        tokenDisplayUpdate("<<","<<","OPR",str(tokenId))
                        writeToken(tokenId,"OPR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), ">>")
                        charPos +=2
                        tokenId +=1
                    else:
                        writeToken(tokenId,"ERR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), "MISSING DOUBLE OPERATOR BITWISE")#* ERROR IF MISSING END OF OPERATOR
                        tokenDisplayUpdate(line[charPos],line[charPos],"ERR","ERR")
                        error=True
                        break
            
            elif(line[charPos] in operators): #* CATCHES OPERATORS
                tokenDisplayUpdate(line[charPos], line[charPos], "OPR",str(tokenId))
                writeToken(tokenId,"OPR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), line[charPos])
                tokenId +=1
                charPos+=1

            elif(line[charPos] in blank): charPos +=1 # skips spaces

            elif(line[charPos] in specialChar): #* CATCHES SPECIAL SYMBOLS

                tokenDisplayUpdate(line[charPos],line[charPos],"SYM",str(tokenId))
                writeToken(tokenId,"SYM", str(lineNum)+":"+str(charPos - len(tokenBuffer)), line[charPos])
                tokenId +=1
                charPos+=1
            
            elif(line[charPos] == "\n"): #* DETECTS LINE FEEDS \n
                tokenDisplayUpdate("\\n","\\n", "SYM",str(tokenId) )
                writeToken(tokenId,"SYM", str(lineNum)+":"+str(charPos - len(tokenBuffer)), "\\n")
                tokenId +=1
                charPos+=1

            else:

                while(line[charPos] not in separators and line[charPos] != "\n"): #* SEPARTES WORDS
                    tokenBuffer += str(line[charPos])
                    tokenDisplayUpdate(tokenBuffer)
                    charPos+=1
                    if(lineNum == len(asmLines)  and charPos == len(line) ): break #exits if last char on file
                
                if(checkNumeric(tokenBuffer)): #* NUMERIC
                    tokenDisplayUpdate(tokenBuffer,tokenBuffer,"NUM",str(tokenId))
                    writeToken(tokenId,"NUM", str(lineNum)+":"+str(charPos - len(tokenBuffer)), tokenBuffer)
                    tokenId +=1


                elif(tokenBuffer in keywords): #* KEYWORDS
                    tokenDisplayUpdate(tokenBuffer, tokenBuffer, "KEY", str(tokenId))
                    writeToken(tokenId,"KEY", str(lineNum)+":"+str(charPos - len(tokenBuffer)), tokenBuffer)
                    tokenId +=1

                elif(re.search(r'^[a-zA-Z|_.][a-zA-Z|_.|\d]+[:]?$', tokenBuffer) or re.search(r'^0x[0-9a-f]+$', tokenBuffer)): #* IDENTFIERS
                    tokenDisplayUpdate(tokenBuffer,tokenBuffer,"IDN",str(tokenId))
                    writeToken(tokenId,"IDN", str(lineNum)+":"+str(charPos - len(tokenBuffer)), tokenBuffer)
                    tokenId +=1

                else:
                    tokenDisplayUpdate(tokenBuffer,tokenBuffer,"ERR","ERR")
                    writeToken(tokenId,"ERR", str(lineNum)+":"+str(charPos - len(tokenBuffer)), tokenBuffer)
                    error = True
                    break
                    tokenId +=1
                tokenBuffer = ""

    
wrapper(main)

#TODO INSANO , ACRESCENTAR MOSTRADOR DE SETA NA LINHA E TABELA DE IDENTIFICADORES

#https://www.nasm.us/xdoc/2.10.09/html/nasmdoc3.html#:~:text=Floating%2Dpoint%20constants%20are%20expressed,declares%20a%20floating%2Dpoint%20constant.