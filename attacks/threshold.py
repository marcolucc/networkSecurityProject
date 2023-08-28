#!/usr/bin/env python3


def attack(ctx):
    # allocate all registers
    input_register1 = ctx.register('plc1', 'I', 0)
    coil_register_1 = ctx.register('plc1', 'C', 0)

    # get parameter from config file
    min_level = int(ctx.param('min-level', 70))
    max_level = int(ctx.param('max-level', 80))

    # setup attack
    def on_level_change(value: int):
        print('value =', value)
        if value < min_level:
            print('turn on')
            coil_register_1.write(1)
        if value >= max_level:
            print('turn off')
            coil_register_1.write(0)

    input_register1.start_polling(500, on_level_change)
