import re

math  = '10x - 1x = x + 3 + 4x'
regex = '([0-9])([x])'
res = re.findall(regex, math)
print res[0][0]
print res
