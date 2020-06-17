#!/usr/bin/python3
from carrega_display import CarregaDisplay
from ada_info import AdaInfo
from lcd_12c import LCD
import datetime as dt
from time import sleep, time

troca = 0
troca2 = 0
ultima_atualizacao = 0,
last_update_line_0 = last_update_line_1 = last_update_line_2 = last_update_line_3 = last_update_save = time()
display = CarregaDisplay(i2c_bus=1, address=0x3F, numLinhas=4)
ada_info = AdaInfo()


def should_update(last_update, rate):
    if(time() - last_update) > rate:
        return True
    return False


def setDisplay_line0():  # passagens

    global troca
    global last_update_line_0
    if not should_update(last_update_line_0, 1.5):
        return

    try:
        passagens = ada_info.get_passagens()[0]
        if troca == len(passagens) or troca > 2:
            troca = 0
        display.display_line1_0(passagens[troca].replace(
            'EO-88', '').replace('AO-7', '').replace(' ', '').strip())
        troca += 1
    except:
        pass

    last_update_line_0 = time()


def setDisplay_line1():
    global troca2
    global last_update_line_1
    if not should_update(last_update_line_1, 3):
        return
    try:
        status = ada_info.get_status()
        if troca2 == 0:
            display.display_line1_1('ET-01 SSD:{} T:{}C'.format(status[0]['Status ET-CSS-001']['SSD_used'],
                                                                status[0]['Status ET-CSS-001']['Temp_CPU'].strip('+').strip('.0')))
            troca2 += 1
        elif troca2 == 1:
            display.display_line1_1('ET-02 SSD:{} T:{}C'.format(status[1]['Status ET-CSS-002']['SSD_used'],
                                                                status[1]['Status ET-CSS-002']['Temp_CPU'].strip('+').strip('.0')))
            troca2 = 0
    except:
        pass
    last_update_line_1 = time()


def setDisplay_line2():
    global last_update_line_2
    if not should_update(last_update_line_2, 1.0):
        return
    try:
        status = ada_info.get_status()
        display.display_line1_2(
            status[0]['Status ET-CSS-001']['Posicao_Atual'])
        last_update_line_2 = time()
    except:
        pass


def setDisplay_line3():
    global last_update_line_3
    if not should_update(last_update_line_3, 1.0):
        return
    try:
        status = ada_info.get_status()
        display.display_line1_3(
            status[1]['Status ET-CSS-002']['Posicao_Atual'])
        last_update_line_3 = time()
    except:
        pass


if __name__ == "__main__":

    while True:

        if dt.datetime.now().time() > dt.time(18, 0, 0):
            display.desliga_display()
        elif dt.datetime.now().time() > dt.time(8, 0, 0):
            display.liga_display()

        setDisplay_line0()
        setDisplay_line1()
        setDisplay_line2()
        setDisplay_line3()
