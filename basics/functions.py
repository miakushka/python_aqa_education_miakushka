# Modify this function to return a list of strings as defined above
# Modified by Mykyta Miakushka
def list_benefits():
    return ['More organized code', 'More readable code', 'Easier code reuse',
            'Allowing programmers to share and connect code together']

# Modify this function to concatenate to each benefit - " is a benefit of functions!"
# Modified by Mykyta Miakushka
def build_sentence(benefit):
    return (benefit + ' is a benefit of functions!')

def name_the_benefits_of_functions():
    list_of_benefits = list_benefits()
    for benefit in list_of_benefits:
        print(build_sentence(benefit))

name_the_benefits_of_functions()