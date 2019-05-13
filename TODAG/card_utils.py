def multiline_input():
    print("(multiline_input)")
    res = ""
    while True:
        line = input()
        if line == '': return res
        res += "\n"+line

if __name__ == "__main__":
    test_input = multiline_input()
    print("====")
    print(test_input) 
