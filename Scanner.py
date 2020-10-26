import re
import SymbolTable
import ProgramInternalForm
class Scanner:
    def __init__(self, sym: SymbolTable, pif: ProgramInternalForm, codePath = "lab1.txt"):
        self.operators = []
        self.tokens = self.readTokens()
        self.code = codePath
        self.pif = pif
        self.symbolTable = sym

    def readTokens(self):
        file = open("tokens.in")
        count = 0

        tokens = []
        line = file.readline()
        while line:
            if count < 19:
                self.operators.append(line.strip())
            tokens.append(line.strip())
            line = file.readline()
            count += 1
        self.operators.append(" ")
        return tokens

    def detect(self, line):
        tokens = []
        bigString = ""
        for i in range(0, len(line)):
            if line[i] in self.operators:
                if line[i] == "\"":
                    stringString = line[i]
                    i += 1
                    while line[i] != "\"":
                        stringString += line[i]
                        i += 1
                    stringString += line[i]
                tokens.append(bigString)
                bigString = ""
                tokens.append(stringString)
            else:
                bigString += line[i]
        return tokens

    def isToken(self, check):
        return check in self.tokens

    def isIdentifier(self, token):
        '''
        hiragana and katakana support limited. search for regex unicod 3000
        '''
        return re.match(r'^[a-zA-Z]([\p{Hiragana}\p{Katakana}\p{Han}]+)([a-zA-Z]|[0-9]|([\p{Hiragana}\p{Katakana}\p{Han}]+)_)$', token) is not None

    def isConstant(self, token):
        return re.match(r'^([\+\-]?[1-9][0-9])$|^\".\"$', token) is not None

    def scan(self):
        file = open(self.code)
        line = file.readline
        count = 0
        while line:
            readTokens = self.detect(line)
            for token in readTokens:
                if self.isToken(token):
                    self.pif.genPif(token, 0)
                elif self.isIdentifier(token) or self.isConstant(token):
                    self.symbolTable.add(token)
                    index = self.symbolTable.search(token)
                    self.pif.genPif(token, index)
                else:
                    raise Exception("There is a Lexical Error detected on line " + count)
            count += 1

'''
Tests
'''
symTable = SymbolTable()
pif = ProgramInternalForm()
scanner = Scanner(symTable, pif)

