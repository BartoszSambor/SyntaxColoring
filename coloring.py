from main import lex
from termcolor import colored

colors = {"symbol": "red",
          "operation": "blue",
          "number": "white",
          "string": "green",
          "special": "orange",
          "preprocessor": "yellow",
          "library": "cyan",
          "empty": "white"
          }

tokens = lex("""
#include <stdlib.h>
 int main (void) {
    printf("Hello, World!\n");
    int a = 0;
    int b = a + 3;
    exit(0);
}
""")

for t in tokens:
    if t[0] in "(){}:;=.<>":
        color = "magenta"
    else:
        color = colors[t[0]]
    text = t[1]
    if text == "":
        text = t[0]
    print(colored(text, color), end="")
