import re

patt = re.compile('^\d{4}(,\d{4})*$')

test_patterns = [',1846,6947','1846,6947,',',1846,6947,','1846,6947','1846,697']

for tp in test_patterns:
    print(tp)
    print(tp.split(','))
    print(re.match(patt,tp))
    print()