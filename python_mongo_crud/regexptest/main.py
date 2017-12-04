import re

#+7 (911) 199-11-11
m = re.match(r'\+7 \(9[0-9]{2}\) [0-9]{3}\-[0-9]{2}\-[0-9]{2}', '+7 (911) 163-33-33')
print(m)
m = re.match(r'[a-zA-Z][a-zA-Z0-9]{1,}@[a-zA-Z0-9]{3,}.[a-zA-Z0-9]{3,}','as@gmail.com')
print(m)
m = re.match(r'[a-z0-9A-Z_]{5,}','vikas')
print(m)