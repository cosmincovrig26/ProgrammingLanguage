import Interpreter
import Token
import TokenKind



myInput = '8.5 / (2 * 9) - -3'
result = Interpreter.run(myInput)
if result != None:
    print("OUTPUT: ", result)
