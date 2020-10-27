class ProgramInternalForm:
    def __init__(self):
        self.contents = []

    def genPif(self, given, id):
        self.contents.append((given, id))

    def __str__(self):
        prettyString = ""
        for ceva in self.contents:
            prettyString += str(ceva) + "\n"
        return prettyString