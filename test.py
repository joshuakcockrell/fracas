class Hi():
    def __init__(self):
        self.garbage = 10

    def get_some_garbage(self):
        return self.garbage

class Soup(Hi):
    def __init__(self):
        Hi.__init__(self)


soup = Soup()

print soup.__dict__.keys()
for k in soup.__dict__.keys():
    print str(k) + ' :' + str(soup.__dict__[k])
print dir(soup)