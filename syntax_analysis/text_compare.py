import sys


file1 = sys.argv[1]
file2 = sys.argv[2]

input1 = open(file1, 'r')
list1 = input1.readlines()

input2 = open(file2, 'r')
list2 = input2.readlines()
print(list1)
if len(list1) == len(list2):
    length = len(list1)
    print(length)
    for index in range(length):
        if list1[index].rstrip('\n') != list2[index].rstrip('\n'):
            print(f'tow file is different in line{index+1}')
            print(list1[index], list2[index])
            sys.exit()
    print('all the content is identical!')
else:
    print('the length of two file is different')
