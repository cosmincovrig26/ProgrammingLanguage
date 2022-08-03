import Interpreter
import Token
import TokenKind



myInput = 'IF 2 > 1 DO INPUT "your value: " variable1'
result = Interpreter.run(myInput)
if result != None:
    print("OUTPUT: ", result)
