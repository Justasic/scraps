class FormattingCode(object):
    """Represents a code used to format text in IRC"""
    codes = {
        # Colors
        "black"       : "\x0301",
        "dark blue"   : "\x0302",
        "dark green"  : "\x0303",
        "green"       : "\x0303",
        "red"         : "\x0304",
        "light red"   : "\x0304",
        "dark red"    : "\x0305",
        "purple"      : "\x0306",
        "brown"       : "\x0307", # On some clients this is orange, others it is brown
        "orange"      : "\x0307",
        "yellow"      : "\x0308",
        "light green" : "\x0309",
        "aqua"        : "\x0310",
        "light blue"  : "\x0311",
        "blue"        : "\x0312",
        "violet"      : "\x0313",
        "grey"        : "\x0314",
        "gray"        : "\x0314",
        "light grey"  : "\x0315",
        "light gray"  : "\x0315",
        "white"       : "\x0316",

        # Other formatting
        "normal"      : "\x0F",
        "bold"        : "\x02",
        "reverse"     : "\x16",
        "underline"   : "\x1F",
        }

    def __init__(self, name):
        self.name = name
        self.value = self.codes[name]

    def __str__(self):
        return self.value

def format(text, *codeNames):
    """Apply each formatting code from the given list of code names
       to the given text, returnging a string ready for consumption
       by an IRC client.
       """
    if codeNames:
        codes = "".join([str(FormattingCode(codeName)) for codeName in codeNames])
        return codes + text + str(FormattingCode('normal'))
    else:
        return text
