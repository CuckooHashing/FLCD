import re
from SymbolTable import SymbolTable
from ProgramInternalForm import ProgramInternalForm
from FA import FiniteAutomata
class Scanner:
    def __init__(self, sym: SymbolTable, pif: ProgramInternalForm, codePath = "D:\\Facultate\\Sem 1\\FLCD\\STlab2\\lab1.txt"):
        self.operators = []
        self.tokens = self.readTokens()
        self.code = codePath
        self.pif = pif
        self.symbolTable = sym
        self.intFA = FiniteAutomata.readFromFile("intFA.in")
        self.idFA = FiniteAutomata.readFromFile("idFA.in")

    def readTokens(self):
        file = open("D:\\Facultate\\Sem 1\\FLCD\\STlab2\\token.in")
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

    def detect(self, line: str):
        tokens = []
        bigString = ""
        for i in range(0, len(line)):
            if line[i] in self.operators:
                tokens.append(bigString)
                bigString = ""
                if line[i] == "\"":
                    stringString = line[i]
                    i += 1
                    while line[i] != "\"":
                        stringString += line[i]
                        i += 1
                    stringString += line[i]
                    tokens.append(stringString)
            else:
                bigString += line[i]
        finalTokens = []
        for tok in tokens:
            if tok != "" and tok != " " and tok != "\n":
                finalTokens.append(tok)
        return finalTokens

    def isToken(self, check):
        return check in self.tokens

    def isIdentifier(self, token):
        #return re.match(r'^[a-zA-Z]([a-zA-Z]|[0-9]|_){,7}$', token) is not None
        return self.idFA.checkString(token)

    def isStringConstant(self, token):
        return re.match(r'^\".*\"$', token) is not None

    def isIntConstant(self, token):
        return self.intFA.checkString(token)

    def scan(self):
        file = open(self.code)
        count = 0
        for line in file.read().splitlines():
            readTokens = self.detect(line)
            for token in readTokens:
                if self.isToken(token):
                    self.pif.genPif(token, 0)
                elif self.isIdentifier(token) or self.isIntConstant(token) or self.isStringConstant(token):
                    index = self.symbolTable.search(token)
                    if index is None:
                        self.symbolTable.add(token)
                    index = self.symbolTable.search(token)
                    self.pif.genPif(token, index)
                else:
                    raise Exception("There is a Lexical Error detected on line " + str(count) + " for token " + token)
            count += 1

'''
Tests
'''
symTable = SymbolTable()
pif = ProgramInternalForm()
scanner = Scanner(symTable, pif)
scanner.scan()
print("symTable: ")
print(symTable)
print("pif: ")
print(pif)

symTable = SymbolTable()
pif = ProgramInternalForm()
scanner = Scanner(symTable, pif, "D:\\Facultate\\Sem 1\\FLCD\\STlab2\\p1er.txt")
scanner.scan()
print("symTable: ")
print(symTable)
print("pif: ")
print(pif)

