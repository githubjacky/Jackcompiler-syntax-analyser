import re
from constant import *
import sys


class TOKENIZER():
    def __init__(self, jackFile):
        # input file
        file_read = open(jackFile, 'r')
        self.lines = file_read.readlines()
        file_read.close()
        
        # outputfile
        fileName = str(jackFile).split('/')[-1]
        fileName = fileName.split('.')[0]
        dirName = str(jackFile).split('/')[-2]
        path = f'./tokenize_result/{dirName}/{fileName}_tokenize.xml'
        self.file_write = open(path, 'w')
        self.file_write.write('<tokens>\n')

        # some issue to handle-1: identify the identifier
        self.identifier = []
        
        # some issue to handle-2: space exist in a string
        self.string_gap = False
        self.imperfect_string = ''
    
    def tokenize_end(self):
        self.file_write.write('</tokens>')
        self.file_write.close()

    def tokenize_begin(self):
        for line in self.lines:
            if self.is_blank(line) or self.is_comment(line):
                continue
            else:
                if line.count('//') != 0:
                    not_comment = line.split('//')[0]
                    if self.not_pair_string(not_comment):
                        print('there is an invalid string')
                        sys.exit()
                    else:
                        elementList = not_comment.split()
                else:
                    elementList = line.split()
                for element in elementList:
                    if element == '//':  # inline comment
                        break
                    else:
                        self.element_toekenize_process(element)

    def element_toekenize_process(self, element):
        if self.string_gap:
            if element.count('"') %2 != 0:
                self.imperfect_string_concatenate(element)
                self.string_gap = False
                self.imperfect_string = ''
            else: 
                self.imperfect_string += (element + ' ')
        elif self.is_keyword(element):
            self.write_xml(TOKEN[0], element)
        elif self.is_symbol(element):
            self.write_xml(TOKEN[1], element)
        elif self.is_integer(element):
            self.write_xml(TOKEN[2], element)
        elif self.is_string(element):
            if self.is_string_gap(element):
                self.imperfect_string = (element[1:] + ' ')
                self.string_gap = True
            else:
                self.write_xml(TOKEN[3], element[1:])
        elif self.is_pure_identifier(element):
            self.write_xml(TOKEN[4], element)
            if element not in self.identifier:
                self.identifier.append(element)
        else:  # symbol+token or identifier
            self.handle_symbol_complex(element)

    def write_xml(self, token, value):
        if value == '<':
            value = '&lt;'
        elif value == '>':
            value = '&gt;'
        xml = f'<{token}>' + ' ' + str(value) + ' ' + f'</{token}>'
        self.file_write.write(xml+'\n')

    def not_pair_string(self, line):
        return True if line.count('"') % 2 != 0 else False

    def is_blank(self, line):
        return True if line == '\n' else False

    def is_comment(self, line):
        pattern = re.compile(r'^(/\*{2}|//|\*{1})')
        match = pattern.match(line.strip())
        return True if match != None else False

    def is_keyword(self, element):
        return True if element in KEYWORD else False

    def is_symbol(self, element):
        return True if element in SYMBOL else False

    def is_integer(self, element):
        pattern = re.compile(r'^\d+$')
        match = pattern.search(element)
        return True if match != None else False

    def is_string(self, element):
        pattern = re.compile(r'^"')
        match = pattern.search(element)
        return True if match != None else False

    def is_string_gap(self, element):
        return True if element.count('"')  %2 != 0 else False

    def imperfect_string_concatenate(self, last_element):
        if last_element.index('"') == 0:
            self.write_xml(TOKEN[3], self.imperfect_string)
            self.handle_symbol_complex(last_element[1:])
        elif last_element.index('"') == len(last_element)-1:
            self.imperfect_string += last_element[:-1]
            self.write_xml(TOKEN[3], self.imperfect_string)
        else:
            self.imperfect_string += last_element[:-2]
            self.write_xml(TOKEN[3], self.imperfect_string)
            self.write_xml(TOKEN[1], last_element[-1])  #　deal with the ';'

    def is_pure_identifier(self, element):
        if element in self.identifier:
            return True
        else:
            for symbol in SYMBOL:
                if element.count(symbol) != 0:
                    return False
            return True
    
    def handle_symbol_complex(self, element):
        element_list = list(element)
        not_symbol = ''
        for sub_element in element_list:
            if sub_element in SYMBOL:
                if sub_element == '"':
                    self.string_gap = True
                else:
                    if not_symbol != '':
                        self.element_toekenize_process(not_symbol)
                        not_symbol = ''
                    self.write_xml(TOKEN[1], sub_element)
            else:
                not_symbol += sub_element
        if not_symbol != '':
            self.element_toekenize_process(not_symbol)