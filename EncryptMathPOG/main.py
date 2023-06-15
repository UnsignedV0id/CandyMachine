import os                  # Bloco de importação de bibliotecas                 
import random              # Bloco de importação de bibliotecas  
import math                # Bloco de importação de bibliotecas
import PySimpleGUI as sg   # Bloco de importação de bibliotecas             

path = os.getcwd() #obtendo local de excução do programa

f = open(path + r"\questions.txt", "r") # Abre arquivo
flines = f.readlines()                  # Salva linhas do arquivo em array     

randomNums = [] # Variavel para guardar 3 numeros randomicos para linhas do programa
# isto é feito para que a cada execução do programa as Crypto não sejam as mesmas
# deixando o programa menos monotono

while len(randomNums) < 3:      #obtendo 3 numeros randomicos não repetidos
    num = random.randint(0,16)
    if num not in randomNums: 
        randomNums.append(num)

questions = [] # variavel que guarda as 3 Cryptos utilizadas

for x in randomNums: # obtendo as cryptos de acordo com linhas randomicas
    questions.append(flines[x].rstrip("\n")) 

def encrypt(word, stage): #aqui se inicia a função resposavel por toda parte de criptografia do programa,
                          # passando como argumento a palavra para ser encripotada e o estagio do programa.

    alphabet = 'abcdefghijklmnopqrstuvwxyz' #definimos o alfabeto

    if stage == 0: #Caesar Stage -- Primeiro estagio do programa    

        difficulty = random.randint(0,3) # escolha randomica de dificuldade( uma letra, uma letra minuscula ou 2 letras)

        ### Nos seguintes blocos ifs fazemos o calculo base que sera reutilizado diversas
        ### vezes durante o codigo, nele, atravéz da tabela ascii , convertemos todas as letras
        ### para numeros .
        ### Geramos entao a Key, que pode ser uma int de 65 a 89 (aqui exclusa a letra Z, visto
        ### que a mesma, por representar 26, nao faz nada de alteraçao ao alfabeto)
        ###
        ### No primeiro if, a conta é feita com um offset positivo ( achando a letra e subtraindo 64
        ### para chegar no numero de casas deslogacas ex: a = 1 , b = 2)
        ### No segundo if repetimos a mesma logica porem com letras negativas ( a = -1, b = -2)
        ### No terceiro if são utilizadas as some de duas letras, uma positiva maiuscula e uma negativa
        ### Minuscula (Ac = -2 , Ca = 2)
        ###
        ### A conta:
        ### Iteramos por todas as letras da palabra passada no argumento, e entao para cada letra
        ### convertemos seu valor para ascii, deslogamos pelo offset apos tirarmos o modulo de 26
        ### e entao convertemos novamente para uma letra    

        ### a variavel cAlphabet presente em todos ifs é utilizada para o modo debug,nela representamos
        ### a integridade do novo alfabeto deslocado

        if difficulty == 0:
            key1 = random.randint(65,89) 
            offset = key1 - 64
            word1 = ''.join(( chr( 97 + ( ord(l) - 97 + offset ) % 26) for l in word))
            cAlphabet = ''.join(( chr( 97 + ( ord(letter) - 97 + offset ) % 26) for letter in alphabet))
            key = chr(key1) 

        elif difficulty == 1:
            key1 = random.randint(97,121) 
            offset = (key1 - 96) * -1
            word1 = ''.join(( chr( 97 + ( ord(l) - 97 + offset ) % 26) for l in word))
            cAlphabet = ''.join(( chr( 97 + ( ord(letter) - 97 + offset ) % 26) for letter in alphabet))
            key = chr(key1) 

        else:
            key1 = random.randint(65,90) 
            key2 = random.randint(97,122)
            #aqui garantimos que as duas letras nao sejam iguais, pois resultariam em um offset de zero
            if key1 == key2:
                while key1 != key2:
                    key2 = random.randint(97,122)

            offset = (key1 - 64) + ((key2 - 96) * -1)
            word1 = ''.join(( chr( 97 + ( ord(l) - 97 + offset ) % 26) for l in word))
            cAlphabet = ''.join(( chr( 97 + ( ord(letter) - 97 + offset ) % 26) for letter in alphabet))
            key = chr(key1) + chr(key2)

    elif stage == 1: #Circle Stage

        #geramos a chave para calcular a area do circulo e garantimos que ela nao seja 26
        #para que novamente o offset nao seja 0
        key1 = random.randint(65,90) 
        while math.floor(((key1 - 64) * (key1 - 64) * 3.14) % 26) == 26:
            key1 = random.randint(65,90) 
        #idem aos anteriores
        offset = (key1 - 64) * (key1 - 64) * 3.14
        offset = math.floor(offset)

        word1 = ''.join(( chr( 97 + ( ord(l) - 97 + offset ) % 26) for l in word))

        cAlphabet = ''.join(( chr( 97 + ( ord(letter) - 97 + offset ) % 26) for letter in alphabet))

        key = chr(key1) 

    elif stage == 2: # TimeCube Stage

        ### aqui geramos os emotes que representam horas a partir da tabela unicode (convertida para decimal)
        ### numeros de (128336 a 128346) são horas completas (13:00, 12:00)
        ### numeros de (128348 a 128359) são horas quebradas (13:30, 12:30)

        key1 = random.randint(128336,128346) #- 128335
        key2 = random.randint(128348,128359) #- 128347 + 0.5

        # escolhemos randomicamente que tipo de hora sera usada (inteira ou quebrada)
        time = key1 if bool(random.randint(0, 1)) else key2

        #ajustamos o offset a partir dos emotes de tempo
        offset = time - 128335 if time < 128348 else time - 128347 + 0.5
        #convertemos para minutos
        offset = offset * 60
        offset = offset * offset * offset # volume do cubo

        # garantimos que apos a conta acima nao caimos em offset de 26 ou mod zero
        while offset % 26 == 0 or offset == 26:
            key1 = random.randint(128336,128346) #- 128335
            key2 = random.randint(128348,128359) #- 128347 + 0.5

            time = key1 if bool(random.randint(0, 1)) else key2

            offset = time - 128335 if time < 128348 else time - 128347 + 0.5

            offset = offset * 60
            offset = offset * offset * offset

        word1 = ''.join(( chr(math.trunc( 97 + ( ord(l) - 97 + offset ) % 26)) for l in word))

        cAlphabet = ''.join(( chr(math.trunc( 97 + ( ord(letter) - 97 + offset ) % 26)) for letter in alphabet))
        
        #convertemos a key novamente para emote no retorno
        key = chr(time)
    
    # Aqui destacamos as letras no alfabeto e no alfabeto cifrado, para melhor visualização
    # Letras presentes na palavra e na cifra ficam em maisculo no modo debug
    for x in range(0, len(alphabet)):
        if(alphabet[x] in word):
            alphabet = alphabet[:x] + alphabet[x].upper() + alphabet[(x+1):]
            cAlphabet = cAlphabet[:x] + cAlphabet[x].upper() + cAlphabet[(x+1):]

    #Aqui inserimos estaços entre todas as letras para, novamente, melhor visualização
    alphabet = alphabet.replace("", " ")[1: -1]
    cAlphabet = cAlphabet.replace("", " ")[1: -1]

    # retornamos palavra cifrada, chave utilizada, alfabeto destacado e alfabeto cifrado destacado
    return [word1,key,alphabet, cAlphabet]

### a partir daqui todo codigo utilizado utiliza a logica implementada na funçao em conjunto com a biblioteca
### pysimplegui para fazer toda a representaçao grafica do programa
### definimos aqui o estagio atual do programa, usamos a funçao passando a primeira palavra para gerar a primeira
### crypto; a ultima variavel é utilizada para o modo debug

currentStage = 0
currentCrypto = encrypt(questions[currentStage],currentStage)
hintVisible = False
# define tema de cores do programa
sg.theme('black')
### define o layout do programa, posicionamento dos textos e botões e conteudo exibido neles, tambem se define aqui o estilo de cada
### componente e sua "key" utilizada para checar eventos que ocorrem no decorrer do funcionamento do programa
layout = [  [sg.Text( text = "Crypto: " + currentCrypto[0] , key = "-Crypto-" , text_color = "white", font = ("Arial Black",30) )] ,
            [sg.Text( text = "Key: " + currentCrypto[1], key = "-Key-" , text_color = "yellow", font = ("Arial Black",30) )],
            [sg.Text('Answer: ',font = ("Arial Black",30)), sg.InputText(k = '-INPUT-',size = (25), font = ("Arial Black",30))],
            [sg.Button('Enter', k = '-ENTER-', bind_return_key = True), sg.Button('Exit') ],
            [sg.Text( text = currentCrypto[2], key = "-Help0-" , text_color = "white", font = ("Courier",20),visible = hintVisible)],
            [sg.Text( text = currentCrypto[3], key = "-Help1-" , text_color = "white", font = ("Courier",20),visible = hintVisible )],
            [sg.Text( text = "", key = "-Help2-" , text_color = "white", font = ("Courier",15),visible = hintVisible )],
            [sg.Text( text = questions[currentStage], key = "-Help3-" , text_color = "white", font = ("Courier",10),visible = hintVisible )] ]
# definimos configuração da janela do programa, estilo, justificação de elementos e retorno de teclas
window = sg.Window('EncryptPOG', layout,element_justification='c',finalize=True,return_keyboard_events=True)

# executamos em loop até break a janela
while True:
    #le os eventos da janela
    event, values = window.read()
    #caso evento de saida, quebra o loop 
    if event == sg.WIN_CLOSED or event == 'Exit': 
        break
    #caso evento enter 
    elif event == "-ENTER-":
        #verifica se a pessoa acertou
        if window['-INPUT-'].get() == questions[currentStage]:
            #caso ainda estamos antes do ultimo estagio
            if currentStage < 2:
                #subimos de estagio e chamamos a funçao de encriptar na proxima palavra
                currentStage += 1
                currentCrypto = encrypt(questions[currentStage],currentStage)
                #atualizamos os conteudos da janela com a crypto key atuais e tmb atualizamos o menu de hint (debug)
                window['-Crypto-'].update(value="Crypto: " + currentCrypto[0])
                window['-Key-'].update(value="Key: " + currentCrypto[1])
                window['-Help0-'].update(value=currentCrypto[2])
                window['-Help1-'].update(value=currentCrypto[3])
                #caso estagio seja segundo
                if currentStage == 1 :
                    #atualizamos  menu hint com dica customizada para nivel
                    char = ord(currentCrypto[1]) - 64
                    result = char * char * 3.14
                    window['-Help2-'].update("π * {0}² = {1} ☛ {2} % 26 = {3}".format(char,result,result,math.floor(result % 26)))
                if currentStage == 2 :
                    #idem
                    key = currentCrypto[1]
                    keyToTime = ord(key) - 128335 if ord(key) < 128348 else ord(key) - 128347 + 0.5
                    timeToMin = keyToTime * 60
                    minSquared = timeToMin*timeToMin*timeToMin
                    minSquared = math.trunc(minSquared)
                    squaredMod = minSquared % 26
                    window['-Help2-'].update(key + "={0} ☛ {1} * 60 = {2} ☛ {3}³(❒) = {4} ☛ {5} % 26 = {6}".format(keyToTime,keyToTime,timeToMin,timeToMin,minSquared,minSquared,squaredMod))
                #atualizamos o valor para mostrar a palavra atual 
                window['-Help3-'].update(value=questions[currentStage])
                window['-INPUT-'].update('') #resetamos input
                #atualizamos crypto conforme estagio
                if currentStage == 1:
                   window['-Crypto-'].update(value="Crypto ◯ : " + currentCrypto[0])

                if currentStage == 2:
                   window['-Crypto-'].update(value="Crypto ⏳ = ❒ : " + currentCrypto[0])

            else: #check final que exibe tela final de acertos
                sg.Popup("Correct Answer :D",custom_text = "Bye",no_titlebar = True, text_color = "Green",font = ("Arial Black",50))
                break

        else: #check final que exibe tela de erro 
            sg.popup_no_buttons("Incorrect Answer :(",no_titlebar = True,auto_close = True,auto_close_duration = 1.5, text_color = "Red",font = ("Arial Black",50))
            window['-INPUT-'].update('')
    elif event == "?": #ativa ou desativa menu de dicas
        hintVisible = not hintVisible
        window['-Help0-'].update(visible=hintVisible)
        window['-Help1-'].update(visible=hintVisible)
        window['-Help2-'].update(visible=hintVisible)
        window['-Help3-'].update(visible=hintVisible)
        window['-INPUT-'].update('')
        
window.close()