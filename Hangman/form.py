colour = ['red', 'green', 'blue', 'yellow', 'black']


class Form(object):
    def __init__(self, x, y, c):
        self._xc = max(0, x)
        self._yc = max(0, y)
        if c in colour:
            self._c = c
        else:
            self._c = colour[0]

    def set_center(self, x, y):
        self._xc = x
        self._yc = y

    def get_center(self):
        return self._xc, self._yc

    def set_colour(self, c):
        if c in colour:
            self._c = c
        else:
            self._c = colour[0]

    def get_colour(self):
        return self._c

    def deplacement(self, dx, dy):
        self._xc = max(0, self._xc + dx)
        self._yc = max(0, self._yc + dy)
        
    def display(self, can):
        raise NotImplementedError
        
class Rectangle(Form):
    def __init__(self, x, y, c, l, h):
        Form.__init__(self, x, y, c)
        self._l = max(0, l)
        self._h = max(0, h)

    def set_dim(self, h, l):
        self._l = max(0, l)
        self._h = max(0, h)

    def get_dim(self):
        return self._h, self._l

    def perimeter(self):
        return (self._h + self._l) * 2

    def surface(self):
        return self._h * self._l

    def display(self, can):
        x, y = self.get_center()
        h, l = self.get_dim()
        c = self.get_colour()
        can.create_rectangle(x - l / 2, y - h / 2, x + l / 2, y + h / 2, fill=c)

    def __str__(self):
        return "Rectangle - center: {} | colour: {} | dimension: {} | perimeter {} | surface {}".format(
            self.get_center(), self.get_colour(), self.get_dim(), self.perimeter(), self.surface())


class Square(Rectangle):
    def __init__(self, x, y, c, l):
        Rectangle.__init__(self, x, y, c, l, l)
        self._l = max(0, l)

    def set_dim(self, l):
        Rectangle.set_dim(self, l, l)

    def get_dim(self):
        l, l = Rectangle.get_dim(self)
        return l

    def display(self, can):
        x, y = self.get_center()
        l = self.get_dim()
        c = self.get_colour()
        can.create_rectangle(x - l / 2, y - l / 2, x + l / 2, y + l / 2, fill=c)


class Circle(Form):
    def __init__(self, x, y, c, d):
        Form.__init__(self, x, y, c)
        self._d = max(0, d)

    def set_dim(self, d):
        self._d = max(0, d)

    def get_dim(self):
        return self._d

    def perimeter(self):
        return 3.14 * self._d

    def surface(self):
        return 3.14 / 4 * self._d ** 2

    def display(self, can):
        x, y = self.get_center()
        d = self.get_dim()
        c = self.get_colour()
        can.create_oval(x - d / 2, y - d / 2, x + d / 2, y + d / 2, fill=c)