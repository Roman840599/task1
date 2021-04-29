import json
import unittest
import traceback
from json import dumps
from time import sleep
from task1 import CustomExecutor, CustomParser


class TestCustomExecutor(unittest.TestCase):

    def setUp(self):
        self.test_ex = CustomExecutor()

    def test__choose_linux_command_human(self):
        class Arg:
            human = True
            inode = False

        arg = Arg()
        res = self.test_ex._CustomExecutor__choose_linux_command(arg)
        self.assertEqual(res, ['df', '-h'])

    def test__choose_linux_command_inode(self):
        class Arg:
            human = False
            inode = True

        arg = Arg()
        res = self.test_ex._CustomExecutor__choose_linux_command(arg)
        self.assertEqual(res, ['df', '-i'])

    def test__choose_linux_command_empty(self):
        class Arg:
            human = False
            inode = False

        arg = Arg()
        res = self.test_ex._CustomExecutor__choose_linux_command(arg)
        self.assertEqual(res, ['df'])

    def test__perform_linux_command(self):
        command = ["echo", "Hello World!"]
        res = self.test_ex._CustomExecutor__perform_linux_command(command)
        assert res == (b"Hello World!\n", None)

    def tearDown(self):
        sleep(1)


class TestCustomParser(unittest.TestCase):
    def setUp(self):
        self.data_parser = CustomParser()

    def test__reformat(self):
        succeeded = True

        try:
            data = (b'one two three\n 1 2 3', None)
            ans = json.dumps({'status': 'success', 'error': 'None', 'result': [{'one': '1', 'two': '2', 'three': '3'}]},
                             indent=4)
            res = self.data_parser._CustomParser__reformat(data)
            assert res == ans
        except:
            traceback.print_exc()
            succeeded = False

        try:
            data = ('one two three\n 1 2 3', None)
            ans = json.dumps({'status': 'failure', 'error': "'str' object has no attribute 'decode'", 'result': 'None'},
                             indent=4)
            res = self.data_parser._CustomParser__reformat(data)
            assert res == ans
        except:
            traceback.print_exc()
            succeeded = False

        self.assertEqual(succeeded, True)

    def tearDown(self):
        sleep(1)


if __name__ == '__main__':
    unittest.main()
