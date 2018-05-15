import csv

print __doc__
f = csv.reader(open('user.csv'), delimiter=',')
for [nome, sobrenome, email] in f:
    print 'nome=%s | sobrenome=%s | email=%s' % (nome, sobrenome, email)

print f.line_num, 'linhas lidas'
print '--- fim'
