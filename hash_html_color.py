template = '''
<html>
<head><title>test</title></head>
<body>
%s
</body>
</html>
'''

body_template = '''
<p style="color: #%(color)s; background-color: #%(bg)s">
A test of %(name)s as %(color)s with a %(bg)s background</p>
'''

names = 'joe tom bill sue john'.split()

from hashlib import md5 as hasher

body = []
for name in names:
    h = hasher(name).hexdigest()
    color = h[:6]
    bg = h[-6:]
    body.append(body_template % {'color': color, 'name':name, 'bg':bg})
body = ''.join(body)
html = template % body
print html