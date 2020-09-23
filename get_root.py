from re import compile as compile_regex
from sys import exit as exit_program
from math import sqrt
from json import loads

f = open("tests.json")
tests = loads(f.read())
f.close()

regex = compile_regex(r"([-+]?\d*)\w?\^?\d?")
more = False

print("""Valid Inputs:
    expression following the format ax^2+bx+c
    exit
    run tests
    more : toggles info such as a b c delta On or Off : default = Off""")

def num_after_point(x):
    s = str(x)
    if not '.' in s:
        return 0
    return len(s) - s.index('.') - 1

def solve(expression):
    matches = regex.finditer(expression)

    a, b, c = (int((match.group(1) if match.group(1) != "-" else -1) or 1)  for matchNum, match in enumerate(matches, start=1) if matchNum != 4 )
    delta = b**2 - 4 * a * c

    roots = "No Root"

    if delta > 0:
        x_1 = (-b - sqrt(delta)) / (2*a)
        x_2 = (-b + sqrt(delta)) / (2*a)
        roots = [x_1, x_2]
    elif delta == 0:
        x = -b / 2*a
        roots = x

    if more:
        print(f'a={a}\nb={b}\nc={c}\ndelta={delta}')

    return {'a':a, 'b':b, 'c':c, 'delta':delta, 'roots':roots}

def run_test():
    succeeded = failed = 0
    for test_info in tests:
        print(f"Input: {test_info['expression']}")
        output = solve(test_info['expression'])
        common = list(set(output['roots']).intersection(test_info['expected']))

        if len(common) == len(output['roots']):
            print("Success")
            succeeded += 1
        else:
            print(f"Failed\nExpected: {test_info['expected']}\nGot: {output['roots']}")
            failed += 1

        print(common, "\n")
    print(f'Succeeded={succeeded} -> {succeeded/len(tests)*100}%\nFailed={failed} -> {failed/len(tests)*100}%')


while True:
    expression = input("Input: ")

    if expression:

        if expression == "exit":
            exit_program()

        elif expression == "run tests":
            run_test()

        elif expression == "more": 
            more = not more
            print("Turned On") if more else print("Turned Off") 
        else:
            print(solve(expression)['roots'])
