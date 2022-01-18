import sys


class COMPARER():
    def __init__(self, test):
        self.test = test

    def compare(self):
        path = str(self.test).split('\\')
        targetfile = path[-1]
        targetDir = path[-2]
        target = f'..\\test_program\\{targetDir}\\{targetfile}'
        input1 = open(target, 'r')
        list1 = input1.readlines()

        input2 = open(self.test, 'r')
        list2 = input2.readlines()

        if len(list1) == len(list2):
            length = len(list1)
            for index in range(length):
                if list1[index].strip('\n') != list2[index].strip('\n'):
                    print(f'Error:two file is different in line{index+1}')
                    print(list1[index], list2[index])
                    sys.exit()
            print('all the content is identical!')
        else:
            print('Error:the length of two file is different')
