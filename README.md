# esolang

**New Features!** Now with support for **while loops** and the ability to use variables as dynamic ranges in **for loops**!

```
>>> interpreter = Interpreter()
>>> a = 10
10
>>> interpreter.visit(parser.parse("for i in range(a) {print(i)}"))
0
1
2
3
4
5
6
7
8
9
>>> a = 5
5
>>> interpreter.visit(parser.parse("for i in range(a) {print(i)}"))
0
1
2
3
4
>>> a = 5
5
>>> interpreter.visit(parser.parse("while a > 0 {a = a - 1}"))
[4, 3, 2, 1, 0]
>>> a = 0
>>> interpreter.visit(parser.parse("while a < 10 {a = a + 1}"))
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```
