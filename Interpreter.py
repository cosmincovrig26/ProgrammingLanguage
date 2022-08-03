import string

import TokenKind
import Token

#### runs each method for our program ####
import TreeNodes

numbers = '1234567890'
letters = string.ascii_letters
numNletters = numbers + letters
conditionals = ('IF','ELIF','ELSE','FOR','TO', 'WHILE')


# VARIABLES
class VariableTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, varName):
        val = self.symbols.get(varName, None)
        if val == None and self.parent:
            return self.parent.get(varName)
        return val

    def set(self, varName, val):
        self.symbols[varName] = val

    def remove(self, name):
        del self.symbols[name]  # find another way to do this


GlobalVariables = VariableTable()  # initialise our table


#### our tokenizer will covert userinput into tokens (lexical analysis) ####

class Tokenizer:  # tokenizer gets all text through
    def __init__(self, myInput):
        self.myInput = myInput
        self.cursor = 0
        self.indexCursor()

    def indexCursor(self):  # make sure that index isn't out of range
        self.cursor = self.cursor if self.cursor < len(self.myInput) else None

    def get(self):  # create our tokens and append to list of tokens
        tokens = []

        while self.cursor != None:
            if self.myInput[self.cursor].isalpha():  # Identifier Tokens
                identifierStart = self.cursor
                while self.cursor != None and self.myInput[self.cursor] in numNletters + '_':
                    self.cursor += 1
                    self.indexCursor()
                identifierToken = self.myInput[identifierStart:self.cursor]
                if identifierToken in TokenKind.Keywords:
                    tokens.append(Token.Token(identifierToken, TokenKind.TokenKind["8"]))
                else:
                    tokens.append(Token.Token(identifierToken, TokenKind.TokenKind["1"]))

            # string tokens
            elif self.myInput[self.cursor] == '"':  # String
                self.cursor += 1
                stringStart = self.cursor
                while self.cursor < len(self.myInput) and not self.myInput[self.cursor] == '"':
                    self.cursor += 1
                tokens.append(Token.Token(self.myInput[stringStart:self.cursor], TokenKind.TokenKind["2"]))
                self.cursor += 1
                self.indexCursor()
            # integer/floats tokens
            elif self.myInput[self.cursor].isdigit():
                integerorFloatStart = self.cursor
                dot = 0
                while self.cursor != None and self.myInput[self.cursor] in numbers + '.':
                    if self.myInput[self.cursor] == '.':
                        if dot == 1:
                            break
                        else:
                            dot += 1
                    self.cursor += 1
                    self.indexCursor()
                if dot == 0:
                    tokens.append(Token.Token(self.myInput[integerorFloatStart:self.cursor], TokenKind.TokenKind["5"]))
                else:
                    tokens.append(Token.Token(self.myInput[integerorFloatStart:self.cursor], TokenKind.TokenKind["4"]))


            elif self.myInput[self.cursor] == '.':
                floatStart = self.cursor - 1
                while self.cursor < len(self.myInput) and not self.myInput[self.cursor].isspace():
                    if self.myInput[self.cursor].isdigit():
                        self.cursor += 1
                    else:
                        tokens.append(Token.Token(self.myInput[floatStart:self.cursor], TokenKind.TokenKind["7"]))
                tokens.append(Token.Token(self.myInput[floatStart:self.cursor], TokenKind.TokenKind["4"]))
                self.indexCursor()

            # our operator tokens
            elif self.myInput[self.cursor] == '+':  # operators
                self.cursor += 1
                tokens.append(Token.Token(self.myInput[self.cursor - 1], TokenKind.OpTokens[0]))
                self.indexCursor()
            elif self.myInput[self.cursor] == '-':  # operators
                self.cursor += 1
                tokens.append(Token.Token(self.myInput[self.cursor - 1], TokenKind.OpTokens[1]))
                self.indexCursor()
            elif self.myInput[self.cursor] == '*':  # operators
                self.cursor += 1
                tokens.append(Token.Token(self.myInput[self.cursor - 1], TokenKind.OpTokens[2]))
                self.indexCursor()
            elif self.myInput[self.cursor] == '/':  # operators
                self.cursor += 1
                tokens.append(Token.Token(self.myInput[self.cursor - 1], TokenKind.OpTokens[3]))
                self.indexCursor()
            elif self.myInput[self.cursor] == '(':  # operators
                self.cursor += 1
                tokens.append(Token.Token(self.myInput[self.cursor - 1], TokenKind.OpTokens[4]))
                self.indexCursor()
            elif self.myInput[self.cursor] == ')':  # operators
                self.cursor += 1
                tokens.append(Token.Token(self.myInput[self.cursor - 1], TokenKind.OpTokens[5]))
                self.indexCursor()
            elif self.myInput[self.cursor] == '{':  # operators
                self.cursor += 1
                tokens.append(Token.Token(self.myInput[self.cursor - 1], TokenKind.OpTokens[7]))
                self.indexCursor()
            elif self.myInput[self.cursor] == '}':  # operators
                self.cursor += 1
                tokens.append(Token.Token(self.myInput[self.cursor - 1], TokenKind.OpTokens[8]))
                self.indexCursor()


            # our logic tokens
            elif self.myInput[self.cursor] == '=':
                self.cursor += 1
                if self.myInput[self.cursor] == '=':
                    self.cursor += 1
                    tokens.append(Token.Token(self.myInput[self.cursor - 2:self.cursor], TokenKind.LogicTokens[0]))
                else:
                    tokens.append(Token.Token(self.myInput[self.cursor - 1], TokenKind.OpTokens[6]))
                self.indexCursor()
            elif self.myInput[self.cursor] == '!':
                self.cursor += 1
                if self.myInput[self.cursor] == '=':
                    self.cursor += 1
                    tokens.append(Token.Token(self.myInput[self.cursor - 2:self.cursor], TokenKind.LogicTokens[1]))
                # for '!FALSE' or '!TRUE'
                elif self.myInput[self.cursor] == 'F' or 'T':
                    negBoolStart = self.cursor - 1
                    self.cursor += 1
                    while self.cursor < len(self.myInput) and not self.myInput[self.cursor].isspace():
                        self.cursor += 1
                    tokens.append(Token.Token(self.myInput[negBoolStart:self.cursor], TokenKind.TokenKind["8"]))
                self.indexCursor()


            elif self.myInput[self.cursor] == '>':
                self.cursor += 1
                if self.myInput[self.cursor] == '=':
                    self.cursor += 1
                    tokens.append(Token.Token(self.myInput[self.cursor - 2:self.cursor], TokenKind.LogicTokens[4]))
                else:
                    tokens.append(Token.Token(self.myInput[self.cursor - 1:self.cursor], TokenKind.LogicTokens[2]))
                self.indexCursor()
            elif self.myInput[self.cursor] == '<':
                self.cursor += 1
                if self.myInput[self.cursor] == '=':
                    self.cursor += 1
                    tokens.append(Token.Token(self.myInput[self.cursor - 2:self.cursor], TokenKind.LogicTokens[5]))
                else:
                    tokens.append(Token.Token(self.myInput[self.cursor - 1:self.cursor], TokenKind.LogicTokens[3]))
                self.indexCursor()
            elif self.myInput[self.cursor] == ',':
                self.cursor += 1
                tokens.append(Token.Token(self.myInput[self.cursor - 1], TokenKind.OpTokens[9]))
                self.indexCursor()

            # whitespace tokens
            elif self.myInput[self.cursor] == ' ' or '\t' or '\n':
                self.cursor += 1
                self.indexCursor()
            else:  # these are the only type of tokens allowed, anything else is considered illegal
                print("Unexpected token!")

        tokens.append((Token.Token('END', TokenKind.TokenKind["6"])))
        return tokens


##### our parser covers Tokens -> Abstract Syntax Tree #####

class Parser:
    def __init__(self, tokens):  # takes in all of our tokens
        self.tokens = tokens
        self.tokenIndex = -1  # indexing our Tokens, start at -1 to call method straight away
        self.incrementToken()

    def incrementToken(self):  # returns index of our token if its in range
        self.tokenIndex += 1
        if self.tokenIndex < len(self.tokens):
            self.currentToken = self.tokens[self.tokenIndex]
        return self.currentToken

    def parse(self):
        result = self.expr()
        return result

    def expr(self):  # building our expression

        if self.currentToken.text == 'VAR':
            self.incrementToken()
            if self.currentToken.TokenType != TokenKind.TokenKind["1"]:
                print("Expected Identifier!")
            variableName = self.currentToken
            self.incrementToken()

            if self.currentToken.TokenType != TokenKind.OpTokens[6]:
                print("Expected '=' after VAR")
            self.incrementToken()
            expr = self.expr()
            return TreeNodes.VariableValue(variableName, expr)

        elif self.currentToken.text == 'INPUT':
            self.incrementToken()
            if self.currentToken.TokenType != TokenKind.TokenKind["2"]:
                print("Expected String!")
            string = self.currentToken.text
            self.incrementToken()

            if self.currentToken.TokenType != TokenKind.TokenKind["1"]:
                print("Expected identifier!")
            variableName = self.currentToken
            return TreeNodes.Input(string, variableName)


        val1 = self.firstOrder()


        while self.currentToken.text in TokenKind.Keywords and self.currentToken.text not in conditionals:
            operator = self.currentToken
            self.incrementToken()
            val2 = self.firstOrder()
            val1 = TreeNodes.BinaryOperation(val1, operator, val2)

        return val1

    def firstOrder(self):  # first order of grammar
        #  NOT keyword
        if self.currentToken == TokenKind.Keywords[2]:
            operator = self.currentToken
            self.incrementToken()
            res = self.firstOrder()
            return TreeNodes.SingularOperation(operator, res)

        val1 = self.secondOrder()

        while self.currentToken.TokenType in TokenKind.LogicTokens:
            operator = self.currentToken
            self.incrementToken()
            val2 = self.secondOrder()
            val1 = TreeNodes.BinaryOperation(val1, operator, val2)

        return val1

    def secondOrder(self):  # second order of grammar
        val1 = self.thirdOrder()

        while self.currentToken.TokenType == TokenKind.OpTokens[0] or self.currentToken.TokenType == TokenKind.OpTokens[
            1]:
            operator = self.currentToken
            self.incrementToken()
            val2 = self.thirdOrder()
            val1 = TreeNodes.BinaryOperation(val1, operator, val2)

        return val1

    def thirdOrder(self):  # third order of grammar
        val1 = self.fourthOrder()

        while self.currentToken.TokenType == TokenKind.OpTokens[2] or self.currentToken.TokenType == TokenKind.OpTokens[
            3]:
            operator = self.currentToken
            self.incrementToken()
            val2 = self.fourthOrder()
            val1 = TreeNodes.BinaryOperation(val1, operator, val2)

        return val1

    def fourthOrder(self):  # fourth order of grammar
        token = self.currentToken

        # Unary operations
        if token.TokenType == TokenKind.OpTokens[0] or token.TokenType == TokenKind.OpTokens[
            1]:  # for +ve and -ve values inclusive
            self.incrementToken()
            val = self.fourthOrder()
            return TreeNodes.SingularOperation(token, val)

        # Brackets '()'
        elif token.TokenType == TokenKind.OpTokens[4]:  # LParen
            self.incrementToken()
            expr = self.expr()
            if self.currentToken.TokenType == TokenKind.OpTokens[5]:
                self.incrementToken()
                return expr
            else:
                print("Error, Paren not found!")

        # If Booleans are used
        elif token.text in TokenKind.Bools:

            if token.text == 'FALSE' or token.text == '!TRUE':
                token.text = 0
            if token.text == 'TRUE' or token.text == '!FALSE':
                token.text = 1
            self.incrementToken()
            return TreeNodes.Number(token)

        # Numbers and Floats
        elif token.TokenType == TokenKind.TokenKind["5"] or token.TokenType == TokenKind.TokenKind["4"]:
            self.incrementToken()
            return TreeNodes.Number(token)

        # String
        elif token.TokenType == TokenKind.TokenKind["2"]:
            self.incrementToken()
            return TreeNodes.String(token)

        # Identifier
        elif token.TokenType == TokenKind.TokenKind["1"]:
            self.incrementToken()
            return TreeNodes.VariableName(token)

        # If
        elif token.text == TokenKind.Keywords[8]:
            ifKeyword = self.ifExpr()
            return ifKeyword

        # While
        elif token.text == TokenKind.Keywords[11]:
            whileKeyword = self.whileExpr()
            return whileKeyword

        elif token.TokenType == TokenKind.OpTokens[7]:
            list = self.listExpr()
            return list

    def ifExpr(self):
        cases = []
        elseCase = None
        self.incrementToken()
        condition = self.expr()
        if self.currentToken.text != 'DO':
            print("Expected 'DO'")
            return None
        self.incrementToken()
        expr = self.expr()
        cases.append((condition, expr))

        while self.currentToken.text == TokenKind.Keywords[9]:
            self.incrementToken()
            condition = self.expr()
            if self.currentToken.text != 'DO':
                print("Expected 'DO'")
                return None
            self.incrementToken()
            expr = self.expr()
            cases.append((condition, expr))

        if self.currentToken.text == TokenKind.Keywords[10]:
            self.incrementToken()
            expr = self.expr()
            elseCase = expr

        return TreeNodes.If(cases, elseCase)


    def whileExpr(self):
        self.incrementToken()
        condition = self.expr()

        if self.currentToken.text != 'DO':
            print("Expected 'DO'")
            return None
        self.incrementToken()

        body = self.expr()

        return TreeNodes.While(condition, body)

    def listExpr(self):
        elements = []
        self.incrementToken()

        if self.currentToken.TokenType == TokenKind.OpTokens[8]:  # '}'
            self.incrementToken()
        else:
            elements.append(self.expr())
            while self.currentToken.TokenType == TokenKind.OpTokens[9]: # comma
                self.incrementToken()
                elements.append(self.expr())
            self.incrementToken()
        return TreeNodes.List(elements)





#### Our Interpreter will convert all of our tokens into actual logic ####

class Interpreter:
    def call(self, node):  # interate through branches on the AST
        name = f'call{type(node).__name__}'  # decides which type of operation it is and what to call
        method = getattr(self, name)
        return method(node)

    def callNumber(self, node):  # finds each node available
        return EvalNumber(node.token.text)

    def callString(self, node):
        return EvalString(node.token.text)

    def callVariableName(self, node):
        varName = node.variableName.text
        val = GlobalVariables.get(varName)

        if not val:
            print("variable not defined!")

        return val

    def callVariableValue(self, node):
        varName = node.variableName.text
        val = self.call(node.val)
        GlobalVariables.set(varName, val)
        return val

    def callBinaryOperation(self, node):
        var1 = self.call(node.num1)  ## evaluates branches of AST on EACH SIDE
        var2 = self.call(node.num2)  ##

        if node.operator.TokenType == TokenKind.OpTokens[0]:  ## goes through each node branch and EVALUATES
            result = var1.Addition(var2)
        elif node.operator.TokenType == TokenKind.OpTokens[1]:
            result = var1.Subtraction(var2)
        elif node.operator.TokenType == TokenKind.OpTokens[2]:
            result = var1.Multiply(var2)
        elif node.operator.TokenType == TokenKind.OpTokens[3]:
            result = var1.Divide(var2)
        # LOGICAL OPERATORS
        elif node.operator.TokenType == TokenKind.LogicTokens[0]:  # ==
            result = var1.EqualTo(var2)
        elif node.operator.TokenType == TokenKind.LogicTokens[1]:  # !=
            result = var1.NotEqualTo(var2)
        elif node.operator.TokenType == TokenKind.LogicTokens[2]:  # >
            result = var1.MoreThan(var2)
        elif node.operator.TokenType == TokenKind.LogicTokens[3]:  # <
            result = var1.LessThan(var2)
        elif node.operator.TokenType == TokenKind.LogicTokens[4]:  # >=
            result = var1.MoreThanEQ(var2)
        elif node.operator.TokenType == TokenKind.LogicTokens[5]:  # <=
            result = var1.LessThanEQ(var2)
        elif node.operator.text == TokenKind.Keywords[0]:  # AND
            result = var1.And(var2)
        elif node.operator.text == TokenKind.Keywords[1]:  # OR
            result = var1.Or(var2)

        return result

    def callSingularOperation(self, node):
        var1 = self.call(node.num1)
        if node.operator.TokenType == TokenKind.OpTokens[1]:
            result = var1.Multiply(EvalNumber(-1))
        elif node.operator.TokenType == TokenKind.Keywords[2]:
            result = var1.Not()

        return result

    def callIf(self, node):
        for condition, expr in node.cases:
            conditionVal = self.call(condition)

            if conditionVal.isTrue():
                exprVal = self.call(expr)
                return exprVal

        if node.elsecase:
            val = self.call(node.elsecase)
            return val
        return None

    def callWhile(self, node):

        while True:
            condition = self.call(node.condition)
            if not condition.isTrue():
                break
            self.call(node.body)
        return None

    def callInput(self, node):

        i = input(node.string)
        if i.isnumeric():
            newToken = Token.Token(i, TokenKind.TokenKind["5"])
            expr = EvalNumber(newToken.text)
        elif isinstance(i, str):
            newToken = Token.Token(i, TokenKind.TokenKind["2"])
            expr = EvalString(newToken.text)
        GlobalVariables.set(node.varName.text, expr)

    def callList(self, node):
        elements = []

        for val in node.val:
            elements.append(self.call(val))
        return EvalList(elements)

##### Evaluating the tree nodes from interpreter #####

class EvalNumber:  # evaluates any nodes that are found
    def __init__(self, val):
        self.val = val

    def Addition(self, val2):  # takes in our number
        if isinstance(val2, EvalNumber):
            return EvalNumber(float(self.val) + float(val2.val))

    def Subtraction(self, val2):
        if isinstance(val2, EvalNumber):
            return EvalNumber(float(self.val) - float(val2.val))

    def Multiply(self, val2):
        if isinstance(val2, EvalNumber):
            return EvalNumber(float(self.val) * float(val2.val))

    def Divide(self, val2):
        if isinstance(val2, EvalNumber):
            return EvalNumber(float(self.val) / float(val2.val))

    def EqualTo(self, val2):
        if isinstance(val2, EvalNumber):
            return EvalNumber(int(self.val) == int(val2.val))

    def NotEqualTo(self, val2):
        if isinstance(val2, EvalNumber):
            return EvalNumber(int(self.val) != int(val2.val))

    def MoreThan(self, val2):
        if isinstance(val2, EvalNumber):
            return EvalNumber(int(self.val) > int(val2.val))

    def LessThan(self, val2):
        if isinstance(val2, EvalNumber):
            return EvalNumber(int(self.val) < int(val2.val))

    def MoreThanEQ(self, val2):
        if isinstance(val2, EvalNumber):
            return EvalNumber(int(self.val) >= int(val2.val))

    def LessThanEQ(self, val2):
        if isinstance(val2, EvalNumber):
            return EvalNumber(int(self.val) <= int(val2.val))

    def And(self, val2):
        if isinstance(val2, EvalNumber):
            return EvalNumber(int(self.val) and int(val2.val))

    def Or(self, val2):
        if isinstance(val2, EvalNumber):
            return EvalNumber(int(self.val) or int(val2.val))

    def Not(self):
        return EvalNumber(True if self.val == False else 0)

    def isTrue(self):
        return self.val != 0

    def __repr__(self):
        return str(self.val)


class EvalString:
    def __init__(self, val):
        self.val = val

    def Addition(self, val2):
        if isinstance(val2, EvalString):
            return EvalString(self.val + val2.val)

    def EqualTo(self, val2):
        if isinstance(val2, EvalString):
            return EvalString(self.val == val2.val)

    def NotEqualTo(self, val2):
        if isinstance(val2, EvalString):
            return EvalString(self.val != val2.val)

    def isTrue(self):
        return self.val != 0

class EvalList:
    def __init__(self, val):
        self.val = val

    def Addition(self, val2):
        list = self
        list.val.append(val2)
        return list

    def Subtraction(self, val2):
        list = self
        list.val.pop(int(val2.val))
        return list

    def EqualTo(self, val2):
        return self.val[int(val2.val)]

def run(myInput):
    tokenizer = Tokenizer(myInput)
    tokens = tokenizer.get()

    parser = Parser(tokens)
    ast = parser.parse()

    # Run interpreter
    if ast != None:
        interpreter = Interpreter()
        res = interpreter.call(ast)
        if res == None:
            return None
        else:
            return res.val

