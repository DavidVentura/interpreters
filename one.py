#!/usr/bin/env python3
import re
SUBEXP = re.compile(r"\([^(]*?\)")
# match parentheses that do not include opening parentheses

TOKENS = re.compile(r"(?P<val>[0-9.]+)|(?P<op>[+-/*])")
OPERATOR = 'op'
VALUE = 'val'
ORDER = {'+': 0,
         '-': 0,
         '*': 1,
         '/': 1,
         }


class Token:
    def __init__(self, _type, value):
        self.type = _type
        if self.type == VALUE:
            self.value = float(value)
        else:
            self.value = value

    def __repr__(self):
        return "Token (%s, %s)" % (self.type, self.value)


class Interpreter:
    val = 0

    def __init__(self, text):
        # these are by definition not nested / overlapping
        text = self.resolve_subexpressions(text)
        tokens = self.tokenizer(text)
        self.val = self.resolve(tokens)

    def resolve_subexpressions(self, text):
        """
        returns a token arr with subexpressions solved
        """
        match = SUBEXP.search(text)
        # No subexpressions? base case
        if match is None:
            return text

        print(match.string)
        # My sub expr str is just the substr delimited by the match
        sstr = match.string[match.start():match.end()]
        # Tokenize the subexpression (without parentheses)
        sub_tokens = self.tokenizer(sstr)
        # Resolve the subexpression
        val = self.resolve(sub_tokens)
        # Replace the subexpression in the text with the resolved value
        # I should have a subexpr token type and resolve it recursively
        # maybe
        text = text[:match.start()] + str(val) + text[match.end():]
        print("=>", text)
        # Keep resolving
        return self.resolve_subexpressions(text)

    def resolve(self, tokens):
        while len(tokens) > 1:
            result, used = self.resolve_most_important(tokens)
            # result = 6
            # used = [2, *, 3]
            # remove all 3 tokens from the initial list
            # replace with the result.
            # This should split the token list into 2, excluding
            # al 3 items and then return L1 + [result] + L2

            inserted = False
            for p in used:
                if p in tokens:
                    if inserted:
                        tokens.remove(p)
                    else:
                        idx = tokens.index(p)
                        tokens[idx] = result
                        inserted = True

        return tokens[0].value

    def resolve_most_important(self, tokens):
        split = self.to_ops(tokens)  # this returns overlap
        # 2 + 3 + 4 => (2+3), (3+4)
        # It's exclusively used for resolving in order.
        # After resolving (2+3), (3+4) gets updated to (5+4)

        # Pick a token with the highest resolving order
        pick = self.pick(split)
        # map the 3 tokens (left, op, right) to a 3-tuple of their values
        # like (2, +, 3), this calls the infix op that just reorders the args
        # and calls 'operate'
        calc = infix_op(*tuple([k.value for k in pick]))

        # return a number (val) with the calulated value from operate
        return (Token('val', calc), pick)

    def pick(self, lst):
        cmax = -1
        ret = None
        for item in lst:
            if item['order'] > cmax:
                cmax = item['order']
                ret = item['value']
        return ret

    def to_ops(self, tokens):
        """
        return all operations (overlapping). The best will be picked later
        2 + 3 + 4 => [(2+3),(3+4)]
        """
        split = []

        for idx in range(1, len(tokens) - 1):
            left = tokens[idx-1]
            token = tokens[idx]
            right = tokens[idx+1]
            if token.type == OPERATOR:
                split.append({'order': ORDER[token.value],
                              'value': (left, token, right)})

        return(split)

    def tokenizer(self, data):
        """
        return a list of Token from the input string
        """
        ret = []
        lst = TOKENS.finditer(data)
        for item in lst:
            d = item.groupdict()
            _type = get_token_type(d)
            ret.append(Token(_type, d[_type]))
        return ret


def infix_op(left, op, right):
    return operate(left, right, op)


def operate(left, right, op):
    if op == "+":
        return left + right
    elif op == "-":
        return left - right
    elif op == "*":
        return left * right
    elif op == "/":
        return left / right
    else:
        assert(1 == 0)


def get_token_type(d):
    return [k for k, v in d.items() if v][0]


if __name__ == '__main__':
    values = ["(2*(2+3))*2+(3*2)",
              "2*3*(1+2)*(2*(2*(2*2*(1+1)+1)+1)+1)+1",
              "22 + 2 * 3",
              "10 * 4  * 2 * 3 / 8",
              "2 + 7 * 4",
              "7 - 8 / 4",
              "14 + 2 * 3 - 6 / 2"]
    for t in values:
        i = Interpreter(t)
        print(t, end="")
        assert(i.val == float(eval(t)))
        print(" OK")
