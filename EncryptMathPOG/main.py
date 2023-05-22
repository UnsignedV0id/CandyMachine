import os
import random
import PySimpleGUI as sg

path = os.getcwd()

f = open(path + r"\questions.txt", "r")
flines = f.readlines()

questions = []

for x in flines:
    questions.append(x.rstrip("\n"))

def encrypt(word, stage):

    if stage == 0:
        key1 = random.randint(65,90) 
        word1 = ''.join(( chr( 97 + ( ord(letter) - 97 + (key1 - 64) ) % 26) for l in word))
        return [word1,chr(key1)]
    elif stage == 1:
        key1 = random.randint(65,90) 
        word1 = ''.join(( chr( 97 + ( ord(letter) - 97 + ((key1 - 64)* -1) ) % 26) for l in word))
        return [word1,chr(key1)]
    else:
        return 2


currentStage = 1
currentKeyCrypto = encrypt(questions[currentStage],currentStage)

sg.theme('black')

layout = [  [sg.Text( text = "Key: " + currentKeyCrypto[0] , key = "-Key-" , text_color = "yellow", font = "bold" )] ,
            [sg.Text( text = "Crypto: " + currentKeyCrypto[1], key = "-Crypto-" , text_color = "white", font = "bold" )],
            [sg.Text('Anwser: '), sg.InputText(k = '-INPUT-')],
            [sg.Button('Enter', k = '-ENTER-', bind_return_key = True), sg.Button('Exit') ] ]

window = sg.Window('EncryptPOG', layout,element_justification='c')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': 
        break
    
window.close()