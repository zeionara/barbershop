import list_all_commands
import command_storage
import connection
import configparser

connection.establish_default()[1].generate_mapping(create_tables=True)

if __name__ == '__main__':
    while(True):
        command = input('\nType a command (\'list\' to get available commands or \'exit\' to exit): \n\n').split(' ');

        if command[0] == 'list':
            list_all_commands.execute()
        elif command[0] == 'exit':
            break;
        else:
            print('\n\nresult:\n\n');
            command_storage.get_handler(command[0])(command)
