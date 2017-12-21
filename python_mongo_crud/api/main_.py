import list_all_commands
import command_storage
import expire_controller
from threading import Thread

thread = Thread(target = expire_controller.inspect, args = (10, ))
thread.start()

if __name__ == '__main__':
    while(True):
        command = input('\nType a command (\'list\' to get available commands or \'exit\' to exit): \n\n').split(' ');

        if command[0] == 'list':
            list_all_commands.execute()
        elif command[0] == 'exit':
            expire_controller.executing = False
            break;
        else:
            print('\n\nresult:\n\n');
            command_storage.get_handler(command[0])(command)
