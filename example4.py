import Interpreter
import Token
import TokenKind



myInput = 'VAR num1 = 7 + 2'
result = Interpreter.run(myInput)
if result != None:
    print("OUTPUT: ", result)
