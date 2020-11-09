class FiniteAutomata:
    def __init__(self, Q, q0, delta, F, sigma, dfa):
        self.Q = Q #set of states
        self.q0 = q0 #initial state
        self.delta = delta #transitions
        self.F = F #final state
        self.sigma = sigma #terminals
        self.dfa = dfa

    @staticmethod
    def removeWhiteSpace(stuff):
        '''
        strips the strings from a list of any white spaces
        '''
        for i in range(len(stuff)):
            stuff[i] = stuff[i].strip()
        return stuff

    @staticmethod
    def makeTransitions(line):
        '''
         algorithm used for delta lines, i.e. lines of the form "something,other = stuff"
        '''
        stuff = line.split("=")
        lhs = FiniteAutomata.removeWhiteSpace(stuff[0].split(","))
        rhs = FiniteAutomata.removeWhiteSpace(stuff[1].split(","))
        return [lhs, rhs[0]]

    @staticmethod
    def readFromFile(filename = "D:\\Facultate\\Sem 1\\FLCD\\FA.in"):
        '''
        reading and parsing the FA from the file
        '''
        file = open(filename)

        Q = FiniteAutomata.removeWhiteSpace(file.readline().split(","))
        sigma = FiniteAutomata.removeWhiteSpace(file.readline().split(","))
        q0 = FiniteAutomata.removeWhiteSpace(file.readline().split(","))
        F = FiniteAutomata.removeWhiteSpace(file.readline().split(","))
        delta = {}
        line = file.readline()
        dfa = True
        while line:
            transition = FiniteAutomata.makeTransitions(line)
            dfa = True
            if (transition[0][0], transition[0][1]) in delta.keys():
                delta[(transition[0][0], transition[0][1])].append((transition[0][1], transition[1]))
                dfa = False
            else:
                delta[(transition[0][0], transition[0][1])] = [transition[1]]
            line = file.readline()
        return FiniteAutomata(Q, q0, delta, F, sigma, dfa)
    

    def checkString(self, potential):
        '''
        checks if a given string passes according to the FA rules
        '''
        if not self.dfa:
            return False 
        current  = self.q0[0] 
        for s in potential:
            if (current, s) in self.delta.keys():
                current = self.delta[(current, s)][0]
            else:
                return False
        return current in self.F

def printMenu():
    '''
    generates a menu
    '''
    print("this is a menu :)")
    print("0. Exit")
    print("1. Show the set of states - Q")
    print("2. Show the alphabeth - sigma")
    print("3. Show the transitions - delta")
    print("4. Show the set of final states - F")
    print("5. Check if a DFA is accepted")

FA = FiniteAutomata.readFromFile()
while True:
    printMenu()
    choice = input("Pick one pls ")
    if choice == "0":
        break
    elif choice == "1":
        print(FA.Q)
    elif choice == "2":
        print(FA.sigma)
    elif choice == "3":
        print(FA.delta)
    elif choice == "4":
        print(FA.F)
    elif choice == "5":
        seq = input("Gimme a sequence to check pls ")
        prin(FA.checkString(seq))