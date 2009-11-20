#!/usr/bin/env python
x = '#!/usr/bin/env python\nx = %s\nprint x %% `x`'
print x % `x`
