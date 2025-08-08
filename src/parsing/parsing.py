text = "int n = 0; " \
"int j = 1; " \
"if(n > 5)" \
"{n = n + 1; } " \
"while(n < 10)" \
"{n = n + 1; }"
import re
global PC
PC = 0  # Global program counter

def ExprEval(expr: str, var_stack: list[str]) -> str:
    global PC
    instructions = []

    # Initialize p0 to 0
    instructions.append(_emit("set 0 p0"))

    # Load variables from stack into registers
    reg_map = {}
    reg_pool = ['p2', 'p3', 'p4', 'p5', 'p6']
    for i, var in enumerate(reversed(var_stack)):
        if not reg_pool:
            raise RuntimeError("Too many variables.")
        reg = reg_pool.pop(0)
        offset = (i + 1)
        reg_map[var] = reg
        instructions.append(_emit(f"mov {reg} [{offset}]"))

    # Evaluate the expression
    temp_regs = ['p6', 'p5', 'p4', 'p3', 'p2']
    eval_instrs = _eval_expr(expr, 'p1', temp_regs.copy(), reg_map)
    instructions.extend(eval_instrs)

    return '\n'.join(instructions)


def _eval_expr(expr: str, target_reg: str, temp_regs, reg_map) -> list[str]:
    global PC
    instructions = []
    tokens = _tokenize(expr)

    def load_operand(token):
        if isinstance(token, list):
            sub_target = temp_regs.pop()
            sub_code = _eval_expr(' '.join(token), sub_target, temp_regs.copy(), reg_map)
            instructions.extend(sub_code)
            return sub_target
        elif token in reg_map:
            return reg_map[token]
        elif token.isdigit():
            reg = temp_regs.pop()
            instructions.append(_emit(f"set {reg} {token}"))
            return reg
        else:
            raise ValueError(f"Unknown token: {token}")

    i = 0
    left = load_operand(tokens[i])
    if left != target_reg:
        instructions.append(_emit(f"mov {target_reg} {left}"))
    i += 1

    while i < len(tokens) - 1:
        op = tokens[i]
        right_token = tokens[i + 1]
        right = load_operand(right_token)

        if op == '+':
            instructions.append(_emit(f"add {target_reg} {right}"))
        elif op == '-':
            instructions.append(_emit(f"sub {target_reg} {right}"))
        elif op == '*':
            instructions.append(_emit(f"mul {target_reg} {right}"))
        elif op == '/':
            instructions.append(_emit(f"div {target_reg} {right}"))
        elif op == '==':
            instructions.append(_emit(f"mov b {target_reg}"))
            instructions.append(_emit(f"cmp b {right}"))
            instructions.append(_emit(f"eqq b p0"))
            break
        elif op == '<':
            instructions.append(_emit(f"mov b {target_reg}"))
            instructions.append(_emit(f"lt b {right}"))
            break
        elif op == '>':
            instructions.append(_emit(f"mov b {target_reg}"))
            instructions.append(_emit(f"gt b {right}"))
            break
        else:
            raise NotImplementedError(f"Unsupported operator: {op}")

        i += 2

    return instructions


def _emit(instruction: str) -> str:
    global PC
    PC += 1
    return instruction


def _tokenize(expr: str) -> list:
    tokens = re.findall(r'\w+|==|[+\-*/<>()]', expr)
    output = []
    stack = []

    for token in tokens:
        if token == '(':
            stack.append([])
        elif token == ')':
            if not stack:
                raise SyntaxError("Unmatched ')'")
            group = stack.pop()
            if stack:
                stack[-1].append(group)
            else:
                output.append(group)
        else:
            if stack:
                stack[-1].append(token)
            else:
                output.append(token)

    if stack:
        raise SyntaxError("Unmatched '('")
    return output

def Tokenize(text):
    global PC
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
    global PC
    vars = []
    ans = ""
    for token in tokens:
        if token.startswith("int"):
            token = token[4:].strip()
            var_name = token.split("=")[0].strip()
            ans += ExprEval(token.split("=")[1].strip(), vars) + "\n"
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
            ans += ExprEval(value.strip("(").rstrip(), vars) + "\n"
            ans += "neg b\n"
            brackets = 0
            new_token = ""
            for char in token:
                if char == "{":
                    brackets += 1
                elif char == "}":
                    brackets -= 1
                elif brackets > 0:
                    new_token += char

            temp = Parse(Tokenize(new_token))
            ans += "jmpif " + str(PC) + "\n"
            ans += temp

        elif token.startswith("while"):
            token = token[5:]
            value = ""
            for char in token:
                if char == ")":
                    break
                else:
                    value += char
            tempPC = PC
            ans += ExprEval(value.strip("(").rstrip(), vars) + "\n"
            ans += "neg b\n"
            brackets = 0
            new_token = ""
            for char in token:
                if char == "{":
                    brackets += 1
                elif char == "}":
                    brackets -= 1
                elif brackets > 0:
                    new_token += char
            temp = Parse(Tokenize(new_token))
            ans += "jmpif " + str(PC) + "\n"
            ans += temp
            ans += "jmp " + str(tempPC) + "\n"

        elif token.startswith("for"):
            token = token[3:]
            value = ""
            for char in token:
                if char == ")":
                    break
                else:
                    value += char
            temp = ExprEval(value.strip("(").rstrip(), vars) + "\n"
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
                temp = ExprEval(new_token[1].rstrip()) + "\n"
                ans += temp
                ans += "mov p1 " + str(vars.index(name)) + "\n"
    return ans

