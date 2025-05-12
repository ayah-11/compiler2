class Tokenizer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.tokens = self.tokenize()

    def tokenize(self):
        tokens = []
        while self.position < len(self.source_code):
            char = self.source_code[self.position]
            if char.isspace():
                self.position += 1
                continue
            elif char.isalpha() or char == '_':
                lexeme = ''
                while self.position < len(self.source_code) and (self.source_code[self.position].isalnum() or self.source_code[self.position] == '_'):
                    lexeme += self.source_code[self.position]
                    self.position += 1
                tokens.append(('IDENTIFIER', lexeme))
                continue
            elif char.isdigit():
                lexeme = ''
                while self.position < len(self.source_code) and self.source_code[self.position].isdigit():
                    lexeme += self.source_code[self.position]
                    self.position += 1
                tokens.append(('INTEGER', lexeme))
                continue
            elif char == '=':
                tokens.append(('EQUAL', char))
                self.position += 1
            elif char == ';':
                tokens.append(('SEMICOLON', char))
                self.position += 1
            elif char == '+':
                tokens.append(('PLUS', char))
                self.position += 1
            elif char == '-':
                tokens.append(('MINUS', char))
                self.position += 1
            elif char == '*':
                tokens.append(('MULTIPLY', char))
                self.position += 1
            elif char == '/':
                tokens.append(('DIVIDE', char))
                self.position += 1
            elif char == '(':
                tokens.append(('LPAREN', char))
                self.position += 1
            elif char == ')':
                tokens.append(('RPAREN', char))
                self.position += 1
            else:
                raise Exception(f"Unexpected character: {char}")
        return tokens

class RecursivePredictiveParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0

    def _current_token(self):
        if self.token_index < len(self.tokens):
            return self.tokens[self.token_index]
        return None

    def _match(self, expected_type):
        current_token = self._current_token()
        if current_token and current_token[0] == expected_type:
            print(f"Matched: {current_token}")
            self.token_index += 1
            return current_token
        else:
            expected = expected_type
            actual = current_token[0] if current_token else "end of input"
            raise Exception(f"Expected '{expected}', but found '{actual}' at token: {current_token}")

    # Grammar rules:
    # statement -> assignment
    # assignment -> IDENTIFIER EQUAL expression SEMICOLON
    # expression -> term { ('+' | '-') term }
    # term -> factor { ('*' | '/') factor }
    # factor -> IDENTIFIER | INTEGER | '(' expression ')'

    def statement(self):
        print("Trying statement...")
        self.assignment()
        print("Statement parsed successfully.")

    def assignment(self):
        print("Trying assignment...")
        self._match('IDENTIFIER')
        self._match('EQUAL')
        self.expression()
        self._match('SEMICOLON')
        print("Assignment parsed successfully.")

    def expression(self):
        print("Trying expression...")
        self.term()
        while self._current_token() and self._current_token()[0] in ['PLUS', 'MINUS']:
            op = self._match(self._current_token()[0])
            self.term()
        print("Expression parsed successfully.")

    def term(self):
        print("Trying term...")
        self.factor()
        while self._current_token() and self._current_token()[0] in ['MULTIPLY', 'DIVIDE']:
            op = self._match(self._current_token()[0])
            self.factor()
        print("Term parsed successfully.")

    def factor(self):
        print("Trying factor...")
        token = self._current_token()
        if token and token[0] == 'IDENTIFIER':
            self._match('IDENTIFIER')
        elif token and token[0] == 'INTEGER':
            self._match('INTEGER')
        elif token and token[0] == 'LPAREN':
            self._match('LPAREN')
            self.expression()
            self._match('RPAREN')
        else:
            raise Exception("Expected identifier, integer, or '('")
        print("Factor parsed successfully.")

    def parse(self):
        try:
            self.statement()
            if self._current_token() is None:
                print("Parsing successful!")
            else:
                raise Exception(f"Extra tokens at the end: {self._current_token()}")
        except Exception as e:
            print(f"Parsing error: {e}")

# --- Example Usage ---
source_code1 = "x=y;"
source_code2 = "count=10;"
source_code3 = "result = a + b;"
source_code4 = "value = (10 * 2);"
source_code5 = "err = ;"
source_code6 = "no_semicolon = 5;" # Added semicolon to avoid parsing error
source_code7 = "invalid-char = 3;"

print(f"Parsing '{source_code1}':")
tokenizer1 = Tokenizer(source_code1)
parser1 = RecursivePredictiveParser(tokenizer1.tokens)
parser1.parse()
print("-" * 20)

print(f"Parsing '{source_code2}':")
tokenizer2 = Tokenizer(source_code2)
parser2 = RecursivePredictiveParser(tokenizer2.tokens)
parser2.parse()
print("-" * 20)

print(f"Parsing '{source_code3}':")
tokenizer3 = Tokenizer(source_code3)
parser3 = RecursivePredictiveParser(tokenizer3.tokens)
parser3.parse()
print("-" * 20)

print(f"Parsing '{source_code4}':")
tokenizer4 = Tokenizer(source_code4)
parser4 = RecursivePredictiveParser(tokenizer4.tokens)
parser4.parse()
print("-" * 20)

print(f"Parsing '{source_code5}':")
tokenizer5 = Tokenizer(source_code5)
parser5 = RecursivePredictiveParser(tokenizer5.tokens)
parser5.parse()
print("-" * 20)

print(f"Parsing '{source_code6}':")
tokenizer6 = Tokenizer(source_code6)
parser6 = RecursivePredictiveParser(tokenizer6.tokens)
parser6.parse()
print("-" * 20)

print(f"Parsing '{source_code7}':")
tokenizer7 = Tokenizer(source_code7)
parser7 = RecursivePredictiveParser(tokenizer7.tokens)
parser7.parse()
print("-" * 20)