class Token:
    def __init__(self, text, TokenType):
        self.text = text
        self.TokenType = TokenType

    def __repr__(self):
        return f'{self.TokenType}:{self.text}'
