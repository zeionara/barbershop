import command_storage

def execute():
    print('%-30s %-10s %-50s' % ('name','short name','arguments'))
    for command in command_storage.commands:
        print('%-30s %-10s %-50s' % command[:3])
