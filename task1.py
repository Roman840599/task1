from subprocess import Popen, PIPE
from argparse import ArgumentParser
from json import dumps


class CustomParser:
    def __init__(self):
        self.__data = None

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = self.__reformat(data)

    @staticmethod
    def __reformat(data):
        result = {'status': None, 'error': None, 'result': []}
        try:
            data = data[0].decode('utf-8')
            strings_list = data.splitlines()
            first_string = strings_list[0].split()
            for i in strings_list[1:]:
                current_string = i.split()
                raw_dict = dict(zip(first_string, current_string))
                result['result'].append(raw_dict)
            result['status'] = 'success'
            result['error'] = 'None'
        except Exception as ex:
            result['status'] = 'failure'
            result['error'] = str(ex)
            result['result'] = 'None'
        finally:
            json_result = dumps(result, indent=4)
            return json_result


class CustomExecutor:
    def __init__(self):
        self.myargparser = ArgumentParser()
        self.data_parser = CustomParser()

    def execute(self):
        self.myargparser.add_argument('--human', help='execute df -h', action="store_true")
        self.myargparser.add_argument('--inode', help='execute df -i', action="store_true")
        arg = self.myargparser.parse_args()
        commands = self.__choose_linux_command(arg)
        data = self.__perform_linux_command(commands)
        self.data_parser.data = data
        print(self.data_parser.data)

    @staticmethod
    def __choose_linux_command(arg):
        if arg.human:
            return ['df', '-h']
        elif arg.inode:
            return ['df', '-i']
        else:
            return ['df']

    @staticmethod
    def __perform_linux_command(commands):
        proc = Popen(commands, stdout=PIPE)
        data = proc.communicate()
        return data


if __name__ == '__main__':
    my_ex = CustomExecutor()
    my_ex.execute()
