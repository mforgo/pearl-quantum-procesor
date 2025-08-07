text = "int n = 0; int j = 1; if(n > 5){n = n + 1; } while(n < 10){n = n + 1; }"
ans = ""
PC = 0

def ExprEval(expr):
    pass
def Tokenize(text):
    tokens = []
    current_token = ""
    brackets = 0
    for char in text:
        if char == "}" or char == "]" or char == ")":
            brackets -= 1
        current_token += char
        if brackets == 0:
            if char == ";":
                tokens.append(current_token.strip(";").strip())
                current_token = ""
            elif char == "}":
                tokens.append(current_token.strip("}").strip())
                current_token = ""
        if char == "{" or char == "[" or char == "(":
            brackets += 1
    return tokens
def Parse(tokens):
    vars = []
    for token in tokens:
        if token.startswith("int"):
            token = token[4:].strip()
            var_name = token.split("=")[0].strip()
            ExprEval(token.split("=")[1].strip())
            vars.append(var_name)
            ans += "push p1 \n"
            PC += 1

        elif token.startswith("if"):
            token = token[2:]
            value = ""
            for char in token:
                if char == ")":
                    break
                else:
                    value += char
            ExprEval(value.strip("(").rstrip())
            brackets = 0
            new_token = ""
            for char in token:
                if char == "{":
                    brackets += 1
                elif char == "}":
                    brackets -= 1
                elif brackets > 0:
                    new_token += char
            Parse(Tokenize(new_token))


        elif token.startswith("while"):
            token = token[5:]
            value = ""
            for char in token:
                if char == ")":
                    break
                else:
                    value += char
            ExprEval(value.strip("(").rstrip())
            brackets = 0
            new_token = ""
            for char in token:
                if char == "{":
                    brackets += 1
                elif char == "}":
                    brackets -= 1
                elif brackets > 0:
                    new_token += char
            Parse(Tokenize(new_token))

        elif token.startswith("for"):
            token = token[3:]
            value = ""
            for char in token:
                if char == ")":
                    break
                else:
                    value += char
            ExprEval(value.strip("(").rstrip())
            brackets = 0
            new_token = ""
            for char in token:
                if char == "{":
                    brackets += 1
                elif char == "}":
                    brackets -= 1
                elif brackets > 0:
                    new_token += char
            Parse(Tokenize(new_token))
        else:
            new_token = token.split("=")
            name = new_token[0].rstrip()
            if name in vars:
                ExprEval(new_token[1].rstrip())
                ans += "mov p1 " + str(vars.index(name)) + "\n"


Parse(Tokenize(text))