'''
Classes supporting a geometry on R2 plane:
    R2Vector, R2Point
'''
from math import sqrt, atan2

class R2Vector(object):
    """Vector on R2-Plane"""

    def __init__(self, x = 0., y = 0.):
        self.x = float(x)
        self.y = float(y)

    def __getitem__(self, idx):
        if idx == 0:
            return x
        elif idx == 1:
            return y
        else:
            raise IndexError("Vector index out of range")

    def __setitem__(self, idx, v):
        if idx == 0:
            x = v
        elif idx == 1:
            y = v
        else:
            raise IndexError("Vector index out of range")

    def __add__(self, v):
        assert type(v) == R2Vector
        return R2Vector(self.x + v.x, self.y + v.y)

    def __iadd__(self, v):
        assert type(v) == R2Vector
        self.x += v.x; self.y += v.y
        return self

    def __sub__(self, v):
        assert type(v) == R2Vector
        return R2Vector(self.x - v.x, self.y - v.y)

    def __isub__(self, v):
        assert type(v) == R2Vector
        self.x -= v.x; self.y -= v.y
        return self

    def __mul__(self, v):
        if type(v) == R2Vector:
            """Dot (scalar) product of 2 vectors"""
            return self.x * v.x + self.y * v.y
        else:
            """Multiply a vector by a number"""
            return R2Vector(self.x*float(v), self.y*float(v))

    def __imul__(self, a):
        """Multiply a vector by a number"""
        # return R2Vector(self.x*float(a), self.y*float(a))
        self.x *= float(a)
        self.y *= float(a)
        return self

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return "(" + repr(self.x) + ", " + repr(self.y) + ")"

    def length(self):
        return sqrt(self.x*self.x + self.y*self.y)

    def norm(self):
        return length(self)

    def normalize(self):
        ''' Normalization of vector: make its length == 1
        preserving its direction'''
        l = self.length()
        if l > 0.:
            self.x /= l
            self.y /= l
        return self

    def normalized(self):
        '''Return a unit vector with the same direction'''
        l = self.length()
        if l > 0.:
            l = 1./l
        else:
            l = 1.
        return self*l

    def normal(self):
        '''Return a normal vector to the given vector.
        The normal is orthogonal to the given vector and
        obtained by rotation 90-degree counterclockwise'''
        return R2Vector(-self.y, self.x)

    def angle(self, v):
        '''Signed angle between two vectors in radians'''
        xx = v*self
        yy = v*self.normal()
        return atan2(yy, xx)

    def det(self, v):
        return self.x*v.y - v.x*self.y

    def signedArea(self, v):
        return self.det(v)

    def area(self, v):
        return abs(self.det(v))

    def __gt__(self, v):
        return (self.x, self.y) > (v.x, v.y)

    def __ge__(self, v):
        return (self.x, self.y) >= (v.x, v.y)

    def __lt__(self, v):
        return not (self >= v)

    def __le__(self, v):
        return not (self > v)

class R2Point(object):
    """Point on R2-Plane"""

    def __init__(self, x = 0., y = 0.):
        self.x = float(x)
        self.y = float(y)

    def __getitem__(self, idx):
        if idx == 0:
            return x
        elif idx == 1:
            return y
        else:
            raise IndexError("Coord. index out of range")

    def __setitem__(self, idx, v):
        if idx == 0:
            x = v
        elif idx == 1:
            y = v
        else:
            raise IndexError("Coord. index out of range")

    def __add__(self, v):
        assert type(v) == R2Vector
        return R2Point(self.x + v.x, self.y + v.y)

    def __iadd__(self, v):
        assert type(v) == R2Vector
        self.x += v.x; self.y += v.y
        return self

    def __sub__(self, v):
        if type(v) == R2Vector:
            return R2Point(self.x - v.x, self.y - v.y)
        else:
            assert type(v) == R2Point
            return R2Vector(self.x - v.x, self.y - v.y)

    def __isub__(self, v):
        assert type(v) == R2Vector
        self.x -= v.x; self.y -= v.y
        return self

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return "(" + repr(self.x) + ", " + repr(self.y) + ")"

    def distance(self, p):
        return (p - self).length()

    def distanceToLine(self, p, v):
        '''Distance from this point to a line defined by
           a point p and a vector v'''
        n = v.normal().normalize()
        return abs((self - p)*n)

    def __gt__(self, p):
        return (self.x, self.y) > (p.x, p.y)

    def __ge__(self, p):
        return (self.x, self.y) >= (p.x, p.y)

    def __lt__(self, p):
        return not (self >= p)

    def __le__(self, p):
        return not (self > p)

    @staticmethod
    def signedArea(p1, p2, p3):
        return ((p2 - p1).signedArea(p3 - p1))/2.0

    @staticmethod
    def area(p1, p2, p3):
        return abs(R2Point.signedArea(p1, p2, p3))

def intersectLines(p1, v1, p2, v2, eps=1e-8):
    """Intersect straight lines

    Each line is defined by a pair (point, vector).
    Return value is a tuple (True/False, P):
    True if the lines intersect, False if they are
    parallel; if lines intersect, then P is a point
    of their intersection"""
    n = v1.normal()
    s = n*v2
    if abs(s) <= eps:
        return False, R2Point()
    t = n*(p1 - p2) / s
    p = p2 + v2*t
    return (True, p)
