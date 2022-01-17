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
            if self.get_element()[1] == 'class':
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
        return self.lines[self.process+1].split(' ')[1]
    
    def parse_class(self):
        for index in range(4):
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
                elif next_token_content in SUBROUTINE_TYPE:
                    self.write_xml('<subroutineDec>')
                    self.retraction += 2
                    self.pase_subroutineDec()
                    self.retraction -= 2
                    self.write_xml('</subroutineDec>')
                else: self.parse_error('neither class var assign  or subroutine')
            else:
                if self.get_element()[1] == '}':
                    self.write_xml(self.process)
                else: self.parse_error('missing "}" at the end of class')

    def parse_classVarDec(self):
        unfinished_classVarDec = True
        while unfinished_classVarDec:
            for index in range(4):
                if index == 0:  # wirte th class Var type
                    self.process += 1
                    self.write_xml(self.process)
                elif index == 1:
                    if self.get_element()[1] in VAR_TYPE:
                        self.write_xml(self.process)
                    else: self.parse_error('wrong var type outside the subroutine')
                elif index == 2:
                    unfinished_classVar_create = True
                    while unfinished_classVar_create:
                        if self.get_element()[0] == '<identifier>':
                            self.write_xml(self.process)
                        else: self.parse_error('wrong token for class var name')
                        if self.get_next_token_content() == ',':
                            self.process += 1
                            self.write_xml(self.process)
                        else:
                            unfinished_classVar_create = False
                else:
                    if self.get_element()[1] == ';':
                        self.write_xml(self.process)
                    else: self.parse_error('missing ";" for class var create')

            if self.get_next_token_content() not in CLASSVAR_TYPE: unfinished_classVarDec = False

    def parse_subroutineDec(self):
        unfinished_shubroutineDect = True
        while unfinished_shubroutineDect:
            for index in range(6):
                if index == 0:
                    self.process += 1
                    self.write_xml(self.process)
                elif index == 1:
                    elements = self.get_element()
                    if elements[1] in VAR_TYPE or elements[1] == 'void':
                        self.write_xml(self.process)
                    else: self.parse_error('wrong subroutine return type')
                elif index == 2:
                    if self.get_element()[0] == '<identifier>':
                        self.write_xml(self.process)
                    else: self.parse_error('wrong token for subroutine name')
                elif index == 3:
                    if self.get_element()[1] == '(':
                        self.write_xml(self.process)
                    else: self.parse_error('missing "(" for subroutine parameter')
                elif index == 4:
                    elements= self.get_element()
                    if elements[1] == ')':
                        self.write_xml('<parameterList>')
                        self.write_xml('</parameterList>')
                        self.write_xml(self.process)
                    elif elements[1] in VAR_TYPE:
                        self.write_xml('<parameterList>')
                        self.retraction += 2
                        unfinished_parameter_create = True
                        while unfinished_parameter_create:
                            self.write_xml(self.process)  # write the parameter type
                            if self.get_element()[0] == '<identifier>':
                                self.write_xml(self.process)
                            else: self.parse_error('wrong token for parameter name')
                            if self.get_next_token_content() == ',':
                                self.process += 1
                                self.write_xml(self.process)
                                if self.get_element()[1] in VAR_TYPE: continue
                                else: self.parse_error('wrong parameter type')
                            else:
                                unfinished_parameter_create = False
                        self.retraction -= 2
                        self.write_xml('</parameterList>')

                        if self.get_element()[1] == ')':
                            self.write_xml(self.process)
                        else: self.parse_error('missing ")" for subroutine parameter')

                    else: self.parse_error('subroutine parameter create error')
                else:
                    if self.get_element[1]() == '{':
                        self.write_xml('<subroutineBody>')
                        self.retraction += 2
                        self.write_xml(self.process)
                        next_token_content = self.get_next_token_content()
                        if next_token_content  == KW_VAR:
                            self.write_xml('<varDec>')
                            self.retraction += 2
                            self.varDec()
                            self.retraction -= 2
                            self.write_xml('</varDec>')
                        elif  next_token_content in STATEMENT_TYPE:
                            self.write_xml('<statements>')
                            self.retraction += 2
                            self.statements()
                            self.retraction -= 2
                            self.write_xml('</statements>')
                        else:
                            self.parse_error('not var or statement')

                        if self.get_element()[1] == '}':
                            self.write_xml(self.process)
                        else: self.parse_error('missing "}" at the end of the statement of subroutine')

                        self.retraction -= 2
                        self.write_xml('</subroutineBody>')
                    else: self.parse_error('missing "{" at the beginning of subroutine')

            if self.get_next_token_content() not in SUBROUTINE_TYPE: unfinished_shubroutineDect = False
    
    def varDec(self):
        unfinished_localVar_create = True
        while unfinished_localVar_create:
            for index in range(4):
                if index == 0:  # write 'var'
                    self.process += 1
                    self.write_xml(self.process)
                elif index == 1:
                    if self.get_element()[1] in VAR_TYPE:
                        self.write_xml(self.process)
                    else: self.parse_error('wrong var type for local variable(subroutineBody)')
                elif index == 2:
                    unfinished_sameType_localVar_create = True
                    while unfinished_sameType_localVar_create:
                        if self.get_element()[0] == '<identifier>':
                            self.write_xml(self.process)
                        else: self.parse_error('wrong token for local var name')
                        if self.get_next_token_content() == ',':
                            self.process += 1
                            self.write_xml(self.process)
                        else:
                            unfinished_sameType_localVar_create = False
                else:
                    if self.get_element()[1] == ';':
                        self.write_xml(self.process)
                    else: self.parse_error('missing ";" for same type local var create')

            if self.get_next_token_content() != KW_VAR: unfinished_localVar_create = False

    def statements(self):
        unfinished_statments = True
        while unfinished_statments:
            statements_type = self.get_element()[1]
            self.write_xml(self.process)  # write the statement type
            if statements_type == KW_LET:
                pass
            elif statements_type == KW_IF:
                pass
            elif statements_type == KW_WHILE:
                pass
            elif statements_type == KW_DO:
                pass
            else:
                pass
                
            if self.get_next_token_content() not in STATEMENT_TYPE: unfinished_statments = False