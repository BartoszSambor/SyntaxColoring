import re


# based on:
# https://accu.org/journals/overload/26/145/balaam_2510/


def lex(chars_iter):
    chars = PeekableStream(chars_iter)
    while chars.next is not None:
        c = chars.move_next()
        if c in " \n":
            yield "empty", _scan(c, chars, "[ \n]")
        # Ignore white space
        elif c in "(){},;=:":
            yield (c, "")
        # Special characters
        elif c in "+-*/":
            yield ("operation", c)
        elif c in ("'", '"'):
            yield ("string",
                   _scan_string(c, chars))
        elif re.match("[.0-9]", c):
            yield ("number",
                   _scan(c, chars, "[.0-9]"))
        elif re.match("[_a-zA-Z]", c):
            yield "symbol", _scan(c, chars, "[_a-zA-Z0-9]")
        elif re.match("#", c):
            yield "preprocessor", _scan(c, chars, "[a-z]+")
        elif c in "<>":
            yield "library", _scan(c, chars, "[<>a-z/.]")
        elif c == "\t":
            raise Exception(
                "Tabs are not allowed in Cell.")
        else:
            raise Exception(
                "Unexpected character: '" + c + "'.")


class PeekableStream:
    def __init__(self, iterator):
        self.iterator = iter(iterator)
        self._fill()

    def _fill(self):
        try:
            self.next = next(self.iterator)
        except StopIteration:
            self.next = None

    def move_next(self):
        ret = self.next
        self._fill()
        return ret


def _scan(first_char, chars, allowed):
    ret = first_char
    p = chars.next
    while p is not None and re.match(allowed, p):
        ret += chars.move_next()
        p = chars.next
    return ret


def _scan_string(delim, chars):
    ret = ""
    while chars.next != delim:
        c = chars.move_next()
        if c is None:
            raise Exception( \
                "A string ran off the end of the program.")
        if c == "\n":
            ret += "\\n"
        else:
            ret += c

    chars.move_next()
    return ret


