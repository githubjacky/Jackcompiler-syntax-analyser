from constant import *

class PARSER():
    def __init__(self, xml_tokenize):
        # input file
        file_read = open(xml_tokenize, 'r')
        self.lines = file_read.readlines()
        file_read.close()

        # outputfile
        fileName = str(xml_tokenize).split('/')[-1]
        fileName = fileName.split('.')[0]
        # dirName = str(xml_tokenize).split('/')[-2]
        path = f'{fileName}_parse.xml'
        self.file_write = open(path, 'w')

        # some issue to handle-1: retraction
        self.retraction = 0

        # some issue to handle-2: process index of the tokenized file
        self.process = 0

    def parse_end(self):
        self.file_write.close()
    
    def parse_begin(self):
        if self.lines[0] == '</token>':
            if self.lines[1][1] == 'class':
                self.file_write.write('<class>' + '\n')
                self.retraction += 2
                self.parse_class()
                self.file_write.write('</class>')
    
    def parse_class(self):
        for index in range(5):
            if index == 0:
                self.process = 2
                if self.lines[self.process].split(' ')[0] == '<identifier>':
                    self.write_xml(self.process)
                else: break
            elif index == 1:
                self.process += 1
                if self.lines[self.process].split(' ')[1] == '{':
                    self.write_xml(self.process)
                else: break
            elif index == 2:
                self.write_xml('<classVarDec>')
                self.retraction += 2
                self.pase_classVarDec()
                self.retraction -= 2
                self.write_xml('</classVarDec>')
            elif index == 3:
                self.write_xml('<subroutineDec>')
                self.retraction += 2
                self.pase_subroutineDec()
                self.retraction -= 2
                self.write_xml('</subroutineDec>')
            else:
                self.process += 1
                if self.lines.split(' ')[1] == '}':
                    self.write_xml(self.process)
                else: break
    
    def write_xml(self, arg):
        if isinstance(arg, int):  # check the datatype
            write = ' '*self.retraction + self.lines[arg] + '\n'
            self.file_write.write(write)
        else:
            write = ' '*self.retraction + arg + '\n'
            self.file_write.write(write)

    def parse_classVarDec(self):
        for index in range(4):
            if index == 0:
                self.process += 1
            elif index == 1:
                self.process += 1
            elif index == 2:
                self.process += 1
            elif index == 3:
                pass
            else:
                self.process += 1

    def parse_subroutineDec(self):
        pass
            
