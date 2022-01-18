from operator import ne

from urllib3 import Retry
from constant import *
import sys
import os
import re


class PARSER():
    def __init__(self, xml_tokenize):
        # input file
        file_read = open(xml_tokenize, 'r')
        rawline = file_read.readlines()
        file_read.close()
        self.lines = []
        for line in rawline:
            self.lines.append(line.strip())
        # outputfile
        pathList = str(xml_tokenize).split('\\')
        fileName = pathList[-1]
        fileName = fileName.split('.')[0]
        dirName = pathList[-2]
        self.output = f'..\\analysis_result\\{dirName}\\{fileName[:-1]}.xml'
        self.file_write = open(self.output, 'w')

        # some issue to handle-1: retraction
        self.retraction = 0
        # some issue to handle-2: process index of the tokenized file
        self.process = 0
        # some issue to handle-3: className
        dir = os.listdir(f'..\\test_program\\{dirName}\\')
        pattern = re.compile(r'\w\.jack')
        for d in dir:
            if pattern.search(d) != None:
                className = d.split('.')[0]
                VAR_TYPE.append(className)

    def parse_end(self):
        self.file_write.close()
    
    def parse_begin(self):
        if self.lines[0] == '<tokens>':
            if self.get_element()[1] == 'class':
                self.write_xml('<class>')
                self.retraction += 2
                self.write_xml(self.process)
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
    
    def get_element(self, *arg):
        if len(arg) == 0:
            self.process += 1
            return self.lines[self.process].split(' ')
        else:
            if arg[0] != 'n': self.parse_error('wrong arg for get element')
            return self.lines[self.process+1].split(' ')
    
    def get_next_token_content(self):
        return self.lines[self.process+1].split(' ')[1]
    
    def parse_class(self):
    # stage 1
        elements= self.get_element()
        if elements[0] == '<identifier>':
            self.write_xml(self.process)
        else: self.parse_error('wrong token for class name')
    # stage 2
        if self.get_element()[1] == '{':
            self.write_xml(self.process)
        else: self.parse_error('missing "{" at the beginning of class')
    # stage 3
        if self.get_next_token_content() in CLASSVAR_TYPE:
            self.write_xml('<classVarDec>')
            self.retraction += 2
            self.parse_classVarDec()
        if self.get_next_token_content() in SUBROUTINE_TYPE:
            self.write_xml('<subroutineDec>')
            self.retraction += 2
            self.parse_subroutineDec()
        else: self.parse_error('missing token for subroutine')
    # stage 4
        if self.get_element()[1] == '}':
            self.write_xml(self.process)
        else: self.parse_error('missing "}" at the end of class')

    def parse_classVarDec(self):
        unfinished_classVarDec = True
        while unfinished_classVarDec:
        # stage 1
            self.process += 1
            self.write_xml(self.process)
        # stage 2
            if self.get_element()[1] in VAR_TYPE:
                self.write_xml(self.process)
            else: self.parse_error('wrong var type outside the subroutine')
        # stage 3
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
        # stage 4
            if self.get_element()[1] == ';':
                self.write_xml(self.process)
            else: self.parse_error('missing ";" for class var create')

            self.retraction -= 2
            self.write_xml('</classVarDec>')

            if self.get_next_token_content() not in CLASSVAR_TYPE: unfinished_classVarDec = False
            else: 
                self.write_xml('<classVarDec>')
                self.retraction += 2

    def parse_subroutineDec(self):
        unfinished_shubroutineDect = True
        while unfinished_shubroutineDect:
        # stage 1
            self.process += 1
            self.write_xml(self.process)
        # stage 2
            elements = self.get_element()
            if elements[1] in VAR_TYPE or elements[1] == 'void':
                self.write_xml(self.process)
            else: self.parse_error('wrong subroutine return type')
        # stage 3
            if self.get_element()[0] == '<identifier>':
                self.write_xml(self.process)
            else: self.parse_error('wrong token for subroutine name')
        # stage 4
            if self.get_element()[1] == '(':
                self.write_xml(self.process)
            else: self.parse_error('missing "(" for subroutine parameter')
        # stage 5
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
        # stage 6
            if self.get_element()[1] == '{':
                self.write_xml('<subroutineBody>')
                self.retraction += 2
                self.write_xml(self.process)
                if self.get_next_token_content()  == KW_VAR:
                    self.write_xml('<varDec>')
                    self.retraction += 2
                    self.varDec()
                if self.get_next_token_content() in STATEMENT_TYPE:
                    self.write_xml('<statements>')
                    self.retraction += 2
                    self.statements()
                else:
                    self.parse_error('not var or statement in subroutineBody')
                if self.get_element()[1] == '}':
                    self.write_xml(self.process)
                else: self.parse_error('missing "}" at the end of the statement of subroutine')

                self.retraction -= 2
                self.write_xml('</subroutineBody>')
            else: self.parse_error('missing "{" at the beginning of subroutine')
            
            self.retraction -= 2
            self.write_xml('</subroutineDec>')
            if self.get_next_token_content() not in SUBROUTINE_TYPE: unfinished_shubroutineDect = False
            else: 
                self.write_xml('<subroutineDec>')
                self.retraction += 2
    
    def varDec(self):
        unfinished_localVar_create = True
        while unfinished_localVar_create:
        # stage 1
            self.process += 1
            self.write_xml(self.process)
        # stage 2
            next_element = self.get_element('n')
            if next_element[1] in VAR_TYPE:
                self.process +=1
                self.write_xml(self.process)
            elif next_element[0] == '<identifier>':
                self.process +=1
                self.write_xml(self.process)
            else: 
                self.parse_error('wrong var type for local variable(subroutineBody)')
        # stage 3
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
        # stage 4
            if self.get_element()[1] == ';':
                self.write_xml(self.process)
            else: self.parse_error('missing ";" for same type local var create')

            self.retraction -= 2
            self.write_xml('</varDec>')
            if self.get_next_token_content() != KW_VAR: 
                unfinished_localVar_create = False
            else:
                self.write_xml('<varDec>')
                self.retraction += 2

    def statements(self):
        unfinished_statements = True
        while unfinished_statements:
            statements_type = self.get_element()[1]

            if statements_type == KW_LET:
                self.write_xml('<letStatement>')
                self.retraction += 2
                self.write_xml(self.process)
            # stage 1
                if self.get_element()[0] == '<identifier>':
                    self.write_xml(self.process)
                else: self.parse_error('wrong token of var assigned')
            # stage 2
                next_element = self.get_element()
                if next_element[1] == '[':
                    self.write_xml(self.process)
                    self.write_xml('<expression>')
                    self.retraction += 2
                    self.expression()
                    self.retraction -= 2
                    self.write_xml('</expression>')
                    if self.get_element()[1] == ']':
                        self.write_xml(self.process)
                    else: self.parse_error('missing "]" in expression of let statement')
                    if self.get_element()[1] == '=':
                        self.write_xml(self.process)
                    else: self.parse_error('missing "=" after "]" of let statmenet')
                elif next_element[1] == '=':
                    self.write_xml(self.process)
                else: self.parse_error('assign error in let statement')
            # stage 3
                self.write_xml('<expression>')
                self.retraction += 2
                self.expression()
                self.retraction -= 2
                self.write_xml('</expression>')
            #　stage 4
                if self.get_element()[1] == ';':
                    self.write_xml(self.process)
                else: self.parse_error('missing ";" at the end of let statement')
                self.retraction -= 2
                self.write_xml('</letStatement>')

            elif statements_type == KW_IF:
                self.write_xml('<ifStatement>')
                self.retraction += 2
                self.write_xml(self.process)
            #　stage 1
                if self.get_element()[1] == '(':
                    self.write_xml(self.process)
                else: self.parse_error('missing "(" in if statement')
            # stage 2
                self.write_xml('<expression>')
                self.retraction += 2
                self.expression()
                self.retraction -= 2
                self.write_xml('</expression>')
            # stage 3
                if self.get_element()[1] == ')':
                    self.write_xml(self.process)
                else: self.parse_error('missing ")" in if statement')
            # stage 4
                if self.get_element()[1] == '{':
                    self.write_xml(self.process)
                else: self.parse_error('missing "{" in if statement')
            # stage 5
                self.write_xml('<statements>')
                if self.get_element('n')[1] != '}':
                    self.retraction += 2
                    self.statements()
                else:
                    self.write_xml('</statements>')
            # stage 6
                if self.get_element()[1] == '}':
                    self.write_xml(self.process)
                else: self.parse_error('missing "}" in statement')
            # else statement
                if self.get_element('n')[1] == KW_ELSE:
                    self.process += 1
                    self.write_xml(self.process)
                # stage 1
                    if self.get_element()[1] == '{':
                        self.write_xml(self.process)
                    else: self.parse_error('missing "{" in if statement')
                # stage 2
                    self.write_xml('<statements>')
                    if self.get_element('n')[1] != '}':
                        self.retraction += 2
                        self.statements()
                    else:
                        self.write_xml('</statements>')
                # stage 3
                    if self.get_element()[1] == '}':
                        self.write_xml(self.process)
                    else: self.parse_error('missing "{" in if statement')
                self.retraction -= 2
                self.write_xml('</ifStatement>')

            elif statements_type == KW_WHILE:
                self.write_xml('<whileStatement>')
                self.retraction += 2
                self.write_xml(self.process)
            # stage 1
                if self.get_element()[1] == '(':
                    self.write_xml(self.process)
                else: self.parse_error('missing "(" in while statement')
            # stage 2
                self.write_xml('<expression>')
                self.retraction += 2
                self.expression()
                self.retraction -= 2
                self.write_xml('</expression>')
            # stage 3
                if self.get_element()[1] == ')':
                    self.write_xml(self.process)
                else: self.parse_error('missing ")" in while statement')
            # stage 4
                if self.get_element()[1] == '{':
                    self.write_xml(self.process)
                else: self.parse_error('missing "{" in while statement')
            # stage 5
                self.write_xml('<statements>')
                self.retraction += 2
                self.statements()
            # stage 6
                if self.get_element()[1] == '}':
                    self.write_xml(self.process)
                else: self.parse_error('missing "}" in while statement')
                self.retraction -= 2
                self.write_xml('</whileStatement>')

            elif statements_type == KW_DO:
                self.write_xml('<doStatement>')
                self.retraction += 2
                self.write_xml(self.process)
                self.subroutineCall()
                if self.get_element()[1] == ';':
                    self.write_xml(self.process)
                else: self.parse_error('missing ";" at the end of do statement')
                self.retraction -= 2
                self.write_xml('</doStatement>')

            elif statements_type == KW_RETURN:  # KW_RETURN
                self.write_xml('<returnStatement>')
                self.retraction += 2
                self.write_xml(self.process)
                next_token_content = self.get_next_token_content()
                if next_token_content == ';':
                    self.process += 1
                    self.write_xml(self.process)
                else:
                    self.write_xml('<expression>')
                    self.retraction += 2
                    self.expression()
                    self.retraction -= 2
                    self.write_xml('</expression>')
                    if self.get_element()[1] == ';':
                        self.write_xml(self.process)
                    else: self.parse_error('missing ";" at the end of return statement')
                self.retraction -= 2
                self.write_xml('</returnStatement>')
            if self.get_next_token_content() not in STATEMENT_TYPE: 
                unfinished_statements = False
                self.retraction -= 2
                self.write_xml('</statements>')

    def expression(self):
        self.write_xml('<term>')
        self.retraction += 2
        self.term()
        self.retraction -= 2
        self.write_xml('</term>')
        unfinished_expression = True if self.get_next_token_content() in OP else False
        while unfinished_expression:
            self.process += 1
            self.write_xml(self.process)
            self.write_xml('<term>')
            self.retraction += 2
            self.term()
            self.retraction -= 2
            self.write_xml('</term>')

            if self.get_next_token_content() not in OP: unfinished_expression = False

    def subroutineCall(self):
    # stage 1
        if self.get_element()[0] == '<identifier>':
                    self.write_xml(self.process)
        else: self.parse_error('wrong token of subroutineCall name')
    # stage 2
        next_element = self.get_element()
        if next_element[1] == '(':
            self.write_xml(self.process)
            self.write_xml('<expressionList>')
            if self.get_element('n')[1] != ')':
                self.retraction += 2
                self.expressionList()
                self.retraction -= 2
            self.write_xml('</expressionList>')
            if self.get_element()[1] == ')':
                self.write_xml(self.process)
            else: self.parse_error('missing ")" in subroutineCall')
        elif next_element[1] == '.':
            self.write_xml(self.process)
            if self.get_element()[0] == '<identifier>':
                self.write_xml(self.process)
            else: self.parse_error('wrong token in subroutineCall')
            if self.get_element()[1] == '(':
                self.write_xml(self.process)
            else: self.parse_error('missing "(" in subroutine Call')
            self.write_xml('<expressionList>')
            if self.get_next_token_content() != ')':
                self.retraction += 2
                self.expressionList()
                self.retraction -= 2
            self.write_xml('</expressionList>')
            if self.get_element()[1] == ')':
                self.write_xml(self.process)
            else: self.parse_error('missing ")" in subroutineCall')

    def expressionList(self):
        self.write_xml('<expression>')
        self.retraction += 2
        self.expression()
        self.retraction -= 2
        self.write_xml('</expression>')
        unfinished_expression = True if self.get_next_token_content() == ',' else False
        while unfinished_expression:
            self.process += 1
            self.write_xml(self.process)
            self.write_xml('<expression>')
            self.retraction += 2
            self.expression()
            self.retraction -= 2
            self.write_xml('</expression>')
            if self.get_next_token_content() != ',': unfinished_expression = False

    def term(self):
        next_element = self.get_element('n')
        if next_element[0] == '<integerConstant>':  # intConst
            self.process += 1
            self.write_xml(self.process)
        elif next_element[0] == '<stringConstant>':  # stringConst
            self.process += 1
            self.write_xml(self.process)
        elif next_element[1] in KEYWORD_CONSTANT:
            self.process += 1
            self.write_xml(self.process)
        elif next_element[0] == '<identifier>':
            next_element = self.lines[self.process+2].split(' ')[1]
            if next_element == '[':
                self.process += 1
                self.write_xml(self.process)
                self.process += 1
                self.write_xml(self.process)
                self.write_xml('<expression>')
                self.retraction += 2
                self.expression()
                self.retraction -= 2
                self.write_xml('</expression>')
                if self.get_element()[1] == ']':
                    self.write_xml(self.process)
                else: self.parse_error('missing "]" in term')
            elif next_element in ';()=*/|]+-,' or next_element == '&lt;' or next_element == '&gt;':
                self.process += 1
                self.write_xml(self.process)
            else:
                self.subroutineCall()
        elif self.get_element()[1] == '(':
            self.write_xml(self.process)
            self.write_xml('<expression>')
            self.retraction += 2
            self.expression()
            self.retraction -= 2
            self.write_xml('</expression>')
            if self.get_element()[1] == ')':
                self.write_xml(self.process)
            else: self.parse_error('missing ")" in term')
        elif next_element[1] in UNARYOP:
            self.write_xml(self.process)
            self.write_xml('<term>')
            self.retraction += 2
            self.term()
            self.retraction -= 2
            self.write_xml('</term>')
        else: 
            self.parse_error('wrong token for term')
