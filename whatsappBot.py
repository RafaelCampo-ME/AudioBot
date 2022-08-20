from multiprocessing.connection import wait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


browser = webdriver.Chrome(executable_path=r"./AudioBot/chromedriver.exe") 
last_printed_msg = None



def validarQR():
    try:
        element = browser.find_element_by_tag_name(By.TAG_NAME,"canvas")
    except:
        return False
    return True

def seleccionarChat(cliente: str):
    print("Obteniendo Chats")
    input_box = browser.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]')
    input_box.click()
    action = ActionChains(browser)
    action.send_keys(cliente)
    action.send_keys(Keys.RETURN)
    action.perform()
    print(f"Selecciono el chat correctamente de {cliente}")


def enviarMSG(msg:str):
    print("Enviando mensaje")
    input_box = browser.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]')
    input_box.click()
    action = ActionChains(browser)
    action.send_keys(msg)
    action.send_keys(Keys.RETURN)
    action.perform()
    print("Mensaje enviado")



def outgoingMsgCheck(webdriver_element):
        """
        Returns True if the selenium webdriver_element has "message-out" in its class.
        False, otherwise.
        """
        for _class in webdriver_element.get_attribute('class').split():
            if _class == "_22Msk":
                return True
        return False
 

def getMsgMetaInfo(webdriver_element):
        """
        Returns webdriver_element's sender and message text.
        Message Text is a blank string, if it is a non-text message
        TODO: Identify msg type and print accordingly
        """
        # check for non-text message


        try:
          
            msg = webdriver_element.find_element(By.XPATH, './/div[contains(@class, "copyable-text")]')
            msg_sender = msg.get_attribute('data-pre-plain-text')
            msg_text = msg.find_elements(By.XPATH, './/span[contains(@class, "selectable-text")]')[-1].text

        except IndexError:
             msg_text = ""

        except Exception:
            try:
                action = ActionChains(browser)
                action.move_to_element().click()
                webdriver_element.find_element(By.XPATH,'.//div[contains(@class, "><svg viewBox=")]')

                
                print("Estoy intentando descargar el mensaje")

                 
                
            except Exception as e:
                print(e)    
            

        return msg_sender, msg_text




def tomarMensajeVos():
    global last_printed_msg
    try:
        all_msgs = browser.find_elements(By.XPATH, '//*[@id="main"]//div[contains(@class, "message")]')

            # check if there is atleast one message in the chat

        if len(all_msgs) >= 1:
            last_msg_outgoing = outgoingMsgCheck(all_msgs[-1])
            last_msg_sender, last_msg_text = getMsgMetaInfo(all_msgs[-1])
            msgs_present = True
        else:
             msgs_present = False
             print("Se encontraron mensajes en el chat")
    except Exception as e:
        print(e)
        msgs_present = False

    print("Termino de buscar mensajes nuevos")   
        
    if msgs_present:
            # if last msg was incoming
            if not last_msg_outgoing:
                # if last_msg is already printed
                if last_printed_msg == last_msg_sender + last_msg_text:
                    pass
                # else print new msgs
                else:
                    print_from = 0
                    # loop from last msg to first
                    for i, curr_msg in reversed(list(enumerate(all_msgs))):
                        curr_msg_outgoing = outgoingMsgCheck(curr_msg)
                        curr_msg_sender, curr_msg_text = getMsgMetaInfo(curr_msg)

                        # if curr_msg is outgoing OR if last_printed_msg is found
                        if curr_msg_outgoing or last_printed_msg == curr_msg_sender + curr_msg_text:
                            # break
                            print_from = i
                            break
                    # Print all msgs from last printed msg till newest msg
                    try:
                        for i in range(print_from + 1, len(all_msgs)):
                            msg_sender, msg_text = getMsgMetaInfo(all_msgs[i])
                            last_printed_msg = msg_sender + msg_text
                            print(msg_sender + msg_text)
                    except Exception as e:
                        print("No es mensaje de texto")
                        print(e)

        # add the task to the scheduler again
     

     
    #input_box=browser.find_element(By.XPATH,'//*[@id="main"]/div[3]/div/div[2]/div[3]/div[69]/div/div[1]/div[1]/div[1]')
    #input_box.click()
#
    #input_box = browser.find_element(By.XPATH, '//*[@id="main"]/div[3]/div/div[2]/div[3]/div[67]/div/div[1]/span[2]')
    #input_box.click()
    #sleep(5)
    #input_box = browser.find_element(By.XPATH, '//*[@id="app"]/div/span[4]/div/ul/div/li[3]/div[1]')
    #input_box.click()
    

def bot():
    browser.get("https://web.whatsapp.com")
    sleep(5)
    print("Audio-Chat-Bot esta iniciando")
    Esperandoingreso = True
    while Esperandoingreso:
        print("Estoy Esperando la validacion")
        Esperandoingreso = validarQR()
        sleep(2)
        if Esperandoingreso == False:
            print("Se ha autenticado")
            break
    sleep(10)
    seleccionarChat("Andrés Marin")
    sleep(5)
    tomarMensajeVos()
    print('Paso seleccion')

bot()

#class="><svg viewBox="  class="><path fill=" 
#<div class="_2oldI dJxPU _3gcnK" role="button" aria-label="Descargar">Descargar</div>