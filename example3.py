import Interpreter
import Token
import TokenKind



myInput = '"hello" + " " + "world"'
result = Interpreter.run(myInput)
if result != None:
    print("OUTPUT: ", result)
