import Interpreter
import Token
import TokenKind



myInput = '2 == 3 OR 3 >= 3'
result = Interpreter.run(myInput)
if result != None:
    print("OUTPUT: ", result)
