# Miakushka: imported re module with custom name just for training purposes
import re as regex
# Miakushka: imported custom package, which is called "test"
from test import custom_module

# Your code goes here
# Added by Mykyta Miakushka
functions = dir(regex)
result = []
for function in functions:
    if 'find' in function:
        result.append(function)

result.sort()
print(result)

custom_module.foo("Mykyta")
