class Number:  # Takes in our number token
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token}'  # f-strings are used when values inside curly brackets are replaced


class String:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'"{self.token}"'


class VariableValue:
    def __init__(self, variableName, val):
        self.variableName = variableName
        self.val = val


class VariableName:
    def __init__(self, variableName):
        self.variableName = variableName


# keeps track of variable names + values

class SingularOperation:
    def __init__(self, operator, num1):
        self.operator = operator
        self.num1 = num1

    def __repr__(self):
        return f'({self.operator}, {self.num1})'


class BinaryOperation:  # Takes in our operations
    def __init__(self, num1, operator, num2):
        self.num1 = num1
        self.num2 = num2
        self.operator = operator

    def __repr__(self):
        return f'({self.num1}, {self.operator}, {self.num2})'


class If:
    def __init__(self, cases, elseCase):
        self.cases = cases
        self.elsecase = elseCase


class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class Input:
    def __init__(self, string, varName):
        self.string = string
        self.varName = varName


class List:
    def __init__(self, val):
        self.val = val
