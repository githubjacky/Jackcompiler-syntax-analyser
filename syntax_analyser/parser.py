from constant import *
import sys

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
        if self.lines[0] == '<tokens>':
            self.process += 1
            if self.lines[1][1] == 'class':
                self.process += 1
                self.write_xml('<class>')
                self.retraction += 2
                self.parse_class()
                self.retraction -= 2
                self.write_xml('</class>')
            else: self.parse_error('missing class')
        else: self.parse_error('missing <tokens>')
    
    def parse_error(self, message):
        print(f'{message}')
        sys.exit()
    
    def write_xml(self, arg):
        if isinstance(arg, int):  # check the datatype
            write = ' '*self.retraction + self.lines[arg] + '\n'
            self.file_write.write(write)
        else:
            write = ' '*self.retraction + arg + '\n'
            self.file_write.write(write)
    
    def get_element(self):
        self.process += 1
        return self.lines[self.process].split(' ')
    
    def get_next_token_content(self):
        next_token_content = self.lines[self.process+1].split(' ')[1]
        return next_token_content
    
    def parse_class(self):
        for index in range(5):
            if index == 0:
                elements= self.get_element()
                if elements[0] == '<identifier>':
                    self.write_xml(self.process)
                    VAR_TYPE.append(elements[1])
                else: self.parse_error('wrong token for class name')
            elif index == 1:
                if self.get_element()[1] == '{':
                    self.write_xml(self.process)
                else: self.parse_error('missing "{" at the beginning of class')
            elif index == 2:
                next_token_content = self.get_next_token_content()
                if next_token_content in CLASSVAR_TYPE:
                    self.write_xml('<classVarDec>')
                    self.retraction += 2
                    self.pase_classVarDec()
                    self.retraction -= 2
                    self.write_xml('</classVarDec>')
                elif next_token_content in SUBROUTINE_TYPE: continue
                else: self.parse_error('neither class var assign  or subroutine')
            elif index == 3:
                self.write_xml('<subroutineDec>')
                self.retraction += 2
                self.pase_subroutineDec()
                self.retraction -= 2
                self.write_xml('</subroutineDec>')
            else:
                if self.get_element()[1] == '}':
                    self.write_xml(self.process)
                else: self.parse_error('missing "}" at the end of class')

    def parse_classVarDec(self):
        not_end = True
        while not_end:
            for index in range(4):
                if index == 0:
                    if self.get_element()[1] in CLASSVAR_TYPE:
                        self.write_xml(self.process)
                    else: self.parse_error('wrong class var type')
                elif index == 1:
                    if self.get_element()[1] in VAR_TYPE:
                        self.write_xml(self.process)
                    else: self.parse_error('wrong var type outside the subroutine')
                elif index == 2:
                    if self.get_element()[0] == '<identifier>':
                        self.write_xml(self.process)
                    else: self.parse_error('wrong token for class var name')
                    if self.has_multiple_var():
                        self.handle_multiple_var()
                else:
                    if self.get_element()[1] == ';':
                        self.write_xml(self.process)
                    else: self.parse_error('missing ";" for class var assignment')

            next_token_content = self.get_next_token_content()
            not_end = True if next_token_content in CLASSVAR_TYPE else False

    def has_multiple_var(self):
        next_token_content = self.get_next_token_content()
        return True if next_token_content == ',' else False

    def handle_multiple_var(self):
        not_end = True
        while not_end:
            self.process += 1
            self.write_xml(self.process)
            if self.get_element()[0] == '<identifier>':
                    self.write_xml(self.process)
            else: self.parse_error('wrong token for class var name')
            not_end = True if self.has_multiple_classVar() else False

    def parse_subroutineDec(self):
        not_end = True
        while not_end:
            for index in range(6):
                if index == 0:
                    if self.get_element()[1] in SUBROUTINE_TYPE:
                        self.write_xml(self.process)
                    else: self.parse_error('wrong subroutine type')
                elif index == 1:
                    elements = self.get_element()
                    if elements[1] in VAR_TYPE or elements[1] == 'void':
                        self.write_xml(self.process)
                    else: self.parse_error('wrong var type in subroutine')
                elif index == 2:
                    if self.get_element()[0] == '<identifier>':
                        self.write_xml(self.process)
                    else: self.parse_error('wrong token for subroutine name')
                elif index == 3:
                    if self.get_element()[1] == '(':
                        self.write_xml(self.process)
                    else: self.parse_error('missing "(" for subroutine parameter')
                elif index == 4:
                    next_token_content= self.get_next_token_content()
                    if next_token_content == ')':
                        self.write_xml('<parameterList>')
                        self.write_xml('</parameterList>')
                        self.process += 1
                        self.write_xml(self.process)
                    elif next_token_content in VAR_TYPE:
                        self.write_xml('<parameterList>')
                        self.retraction += 2
                        self.process += 1
                        self.write_xml(self.process)

                        if self.get_element()[0] == '<identifier>':
                            self.write_xml(self.process)
                        else: self.parse_error('wrong token for parameter name')
                        if self.has_multiple_var():
                            self.handle_multiple_var()

                        self.retraction -= 2
                        self.write_xml('</parameterList>')

                        if self.get_element()[1] == ')':
                            self.write_xml(self.process)
                        else: self.parse_error('missing ")" for subroutine parameter')
                    else: self.parse_error('parameter assign error')
                else:
                    if self.get_next_token_content() == '{':
                        self.write_xml('<subroutineBody>')
                        self.retraction += 2
                        self.parse_subroutineBody()
                        self.retraction -= 2
                        self.write_xml('</subroutineBody>')
                    else: self.parse_error('missing "{" at the beginning of subroutine')

            next_token_content = self.get_next_token_content()
            not_end = True if next_token_content != ';' else False
    
    def parse_subroutineBody():
        pass