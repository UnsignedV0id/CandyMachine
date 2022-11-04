import re
tokens = open("tokens.txt", "w")
comments = ['*', ';']


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


keywords = []
keywords = fillTokens("keywords", keywords)

tokenId = 0

tokenBuffer = ''



with open('code.asm') as asmCode:
    fileSize = len(asmCode.readlines()) - 1
    asmCode.seek(0)

    for lineNum, line in enumerate(asmCode):

        #reads line char by char
        charPos = 0

        while(True):

            if(line[charPos] in comments ): break #ignore comments

            if(line[charPos] == '\n'): #checks for end of line

                writeToken(tokenId,"LNF", str(lineNum + 1)+":"+str(charPos + 1), "\\n")
                tokenId+=1
                charPos = 0
                break

            if(line[charPos] != ' '):

                if(line[charPos] in [".", "_"]): #labels in assembly can start with [a-Z] or [._]
                    tokenBuffer += str(line[charPos])
                    charPos +=1

                elif(line[charPos] == "\""):# gets strings
                    tokenBuffer+=str(line[charPos])
                    charPos +=1
                    while(line[charPos] != "\""):
                        tokenBuffer+=str(line[charPos])
                        if(lineNum == fileSize and charPos  == len(line) - 1): break #check for last character in file
                        charPos +=1
                    writeToken(tokenId,"STR", str(lineNum + 1)+":"+str(charPos), tokenBuffer)

                while(line[charPos] not in [' ', ',', '.', '\n' ]):
                    if(lineNum == 17):
                        pass
                    tokenBuffer += str(line[charPos])
                    if(lineNum == fileSize and charPos  == len(line) - 1): break #check for last character in file
                    charPos +=1

                if(tokenBuffer.upper() in keywords):  #KEYWORDS  
                    writeToken(tokenId,"KEY", str(lineNum + 1)+":"+str(charPos + 1), tokenBuffer)

                elif re.search(r'^[a-zA-Z|_.][a-zA-Z|_.|\d]+[:]?$', tokenBuffer): #IDENTIFIERS
                    writeToken(tokenId,"IDN", str(lineNum + 1)+":"+str(charPos + 1), tokenBuffer)
                
                elif(tokenBuffer.isnumeric()):
                    writeToken(tokenId,"NUM", str(lineNum + 1)+":"+str(charPos + 1), tokenBuffer)

                elif(line[charPos] == ","):
                    writeToken(tokenId, "CMM", str(lineNum + 1)+":"+str(charPos + 1), ',')
                    charPos+=1
                else:
                    writeToken(tokenId,"ERR", str(lineNum + 1)+":"+str(charPos + 1), tokenBuffer)
                    
                tokenId +=1
                tokenBuffer = ''

                if(lineNum == fileSize and charPos  == len(line) - 1): break #check for last character in file
            
            else:
                while(line[charPos] == ' '):
                    if(lineNum == fileSize and charPos  == len(line) - 1): break #check for last character in file
                    charPos+=1 #skip until non space
            
        
        
    



asmCode.close()
tokens.close()


#usefull stuff 
# https://www.tutorialspoint.com/assembly_programming/assembly_basic_syntax.htm
# https://www.mycompiler.io/new/asm-x86_64
# https://www.tutorialspoint.com/assembly_programming/assembly_basic_syntax.htm
# https://www.cse.psu.edu/~kxc104/class/cmpen472/20s/hw/hw1/AssemSyntax.html
# https://docs.oracle.com/cd/E19253-01/817-5477/817-5477.pdf
# https://spot.pcc.edu/~wlara/asmx86/asmx86_manual_4.pdf
# http://www.mathemainzel.info/files/x86asmref.html