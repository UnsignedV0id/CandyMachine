import os
import PySimpleGUI as sg       
sg.theme('dark purple ')   
path = os.getcwd()


#! Create Checkout window
def openBuyWindow(price,product):
        layout = [  [sg.Text("You are buying $" + str(price) + " worth of " + product, text_color='green')],
                    [sg.Button('+$1',button_color="green",k='1'),sg.Button('+$2',button_color="green",k='2'),sg.Button('+$5',button_color="green",k='3')
                    ,sg.Checkbox('Subtract', k='-MINUSMODE-',enable_events=True)],
                    [sg.Text(" $ 0",text_color="green",font=("bold",20),k = "-INSERTED-")],
                    [sg.Button('Pay',button_color="orange"), sg.Button('Cancel',button_color='red')]]

        window = sg.Window('Checkout!', layout, modal=True)

        cash = [[1,0], [2,0], [5,0]] #* Value, Inserted , QAvailible, QReturn to client
        minus = False
        easter = 0

        while True:
            event, values = window.read()

            if event == 'Cancel' or event == sg.WIN_CLOSED:
                break

            elif event == 'Pay' and (cash[0][1] + cash[1][1]*2 + cash[2][1]*5) < price:
                sg.popup("not enoght money", title=":(",text_color="red")

            elif event == 'Pay' and (cash[0][1] + cash[1][1]*2 + cash[2][1]*5) == price:
                sg.popup("Enjoy your purchase!", title=":)",text_color="green")
                break
            elif event == 'Pay' and (cash[0][1] + cash[1][1]*2 + cash[2][1]*5) > price:
                sg.popup("Enjoy your purchase!\nHere is your change: $" + str((cash[0][1] + cash[1][1]*2 + cash[2][1]*5) - price), title=":)",text_color="green")
                break

            elif event == '-MINUSMODE-' and minus == False:
                
                window['1'].update(" -$1",button_color ='red')
                window['2'].update(" -$2",button_color ='red')
                window['3'].update(" -$5",button_color ='red')
                minus = True

            elif event == '-MINUSMODE-' and minus == True:
                
                window['1'].update("+$1",button_color ='green')
                window['2'].update("+$2",button_color ='green')
                window['3'].update("+$5",button_color ='green')
                minus = False
                
            elif (event == '1' or  event == '2' or event == '3') and (minus == False and cash[0][1] + cash[1][1]*2 + cash[2][1]*5 >= 8):
                sg.popup("Maximum of money  reached", title=":(",text_color="red")

            elif event == '1' and minus == False:
                cash[0][1] += 1
            elif event == '2' and minus == False:
                cash[1][1] += 1
            elif event == '3' and minus == False:
                cash[2][1] += 1
            elif event == '1' and minus == True:
                cash[0][1] -= 1
            elif event == '2' and minus == True:
                cash[1][1] -= 1
            elif event == '3' and minus == True:
                cash[2][1] -= 1

            if cash[0][1] + cash[1][1]*2 + cash[2][1]*5 < 0:
                cash[0][1] = 0
                cash[1][1] = 0
                cash[2][1] = 0
                easter +=1

            if easter == 5:
                sg.popup("why ? ʕ•ᴥ•ʔ", title=":(",text_color="red")
                easter = 19

            elif easter == 20:
                sg.popup("STOP ಠ_ಠ", title=":(",text_color="red")
                easter = -30
                
            window["-INSERTED-"].update(" $ " + str(cash[0][1] + cash[1][1]*2 + cash[2][1]*5))

            if (cash[0][1] + cash[1][1]*2 + cash[2][1]*5) >= price:
                window['Pay'].update(button_color="green")

            else:
                window['Pay'].update(button_color="orange")

            
        minus = False
        window.close()
    

#! Define the main window's contents
layout = [  [sg.Text("Pick your candy"), sg.Button('CANDY 1',tooltip='Price 6'), sg.Button('CANDY 2',tooltip='Price 7'), sg.Button('CANDY 3',tooltip='Price 8')],
            [sg.Text(key='-PRICE-')],
            [sg.Image(key="-IMAGE-", size=(300,300), background_color="white smoke")],
            [sg.Button('Checkout', button_color='green') ,sg.Button('Quit', button_color="red"),sg.Text(key='-WARNING-')]] 

#! Create main window
window = sg.Window('Candy shop', layout) 

price = 0 
product = "none"

#! Event loop
while True:
    event, values = window.read()       
                
    if event == sg.WINDOW_CLOSED or event == 'Quit': #? Exits
        break

    #Button Presses
    elif event == 'CANDY 1':
        price = 6
        product = "CANDY 1"
        window['-PRICE-'].update('CANDY 1|$'+ str(price) + '|', text_color ='lime green')

        window['CANDY 1'].update(button_color='green')
        window['CANDY 2'].update(button_color='gray')
        window['CANDY 3'].update(button_color='gray')
        window['-IMAGE-'].update(filename= path + '/CANDY 1.png')

    elif event == 'CANDY 2':
        price = 7
        product = "CANDY 2"
        window['-PRICE-'].update('CANDY 2|$'+ str(price) + '|', text_color ='lime green')

        window['CANDY 1'].update(button_color='gray')
        window['CANDY 2'].update(button_color='green')
        window['CANDY 3'].update(button_color='gray')
        window['-IMAGE-'].update(filename= path + '/CANDY 2.png')

    elif event == 'CANDY 3':
        price = 8
        product = "CANDY 3"
        window['-PRICE-'].update('CANDY 3|$'+ str(price) + '|', text_color ='lime green')

        window['CANDY 1'].update(button_color='gray')
        window['CANDY 2'].update(button_color='gray')
        window['CANDY 3'].update(button_color='green')
        window['-IMAGE-'].update(filename= path + '/CANDY 3.png')
    
    elif event == 'Checkout':

        if product == "none":
            window['-WARNING-'].update("Don't forget to choose your candy!",text_color = "red")

        else:
            openBuyWindow(price ,product)


window.close()             

