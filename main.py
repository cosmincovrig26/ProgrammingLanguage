import Interpreter
import Token
import TokenKind


while True:
    myInput = input('Your code> ')
    result = Interpreter.run(myInput)
    if result != None:
        print("OUTPUT: ", result)
