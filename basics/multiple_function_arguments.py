# edit the functions prototype and implementation
# edited by Mykyta Miakushka
def foo(a, b, c, *d):
    return len(d)

def bar(a, b, c, **d):
    if d.get("magicnumber") == 7:
        return True
    else:
        return False


# test code
if foo(1,2,3,4) == 1:
    print("Good.")
if foo(1,2,3,4,5) == 2:
    print("Better.")
if bar(1,2,3,magicnumber = 6) == False:
    print("Great.")
if bar(1,2,3,magicnumber = 7) == True:
    print("Awesome!")
