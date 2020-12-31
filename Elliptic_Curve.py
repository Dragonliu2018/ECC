"""
Implementing an elliptic curve over a finite field F_p for prime p > 3.
	
E:	y^2 = x^3 + ax + b,

where a,b /in F_p and -16(4a^3 + 27b^2) /neq 0 (discriminant being non-zero guarantees associativity).

Has natural abelian group structure on the set of all points (x,y) in F_p x F_p satisfying equation E with the additional point at infinity.
"""
import math


INF_POINT = None #abstract point at infinity


def tobinary(n):
	while(n>=0):
		i = 0
		if n==0:
			return n
		binary_digits = []
		r = int(math.log(n,2))
		for l in range(0,r+1):
			if n % 2 == 1:
				binary_digits.append(1)
				n=int(n/2)
			else:
				binary_digits.append(0)
				n=int(n/2)
		return binary_digits

		
def isprime(n):
	factors = []
	if (n>1):
		floor_sqrt = int(n ** (0.5))
		for d in range(2,floor_sqrt + 1):
			if n % d != 0:
				continue
			factors.append(d)
			n = n/d

		if len(factors) == 0:
			return True
	return False


class EllipticCurve:
	def __init__ (self,a,b,p):
		self.a = a
		self.b = b
		self.p = p
		self.points = []

	def definePoints(self):
		self.points.append(INF_POINT)
		for x in range(self.p):
			for y in range(self.p):
				if self.equalModp(y*y, x** 3 + self.a*x + self.b):
					self.points.append((x,y))

	def printPoints(self):
		print(self.points)

	def numberPoints(self):
		return len(self.points)

	def discriminant(self):	
		D = -16*(4*(self.a ** 3) + 27 * self.b * self.b)
		return self.reduceModp(D)

	#helper functions

	def reduceModp(self, x):
		return x % self.p

	def equalModp(self, x, y):
		return self.reduceModp(x-y) == 0

	def inverseModp(self,x):
	    if x == 0:
	        raise ZeroDivisionError('division by zero')

	    if x < 0:
	        # k ** -1 = p - (-k) ** -1  (mod p)
	        return self.p - self.inverseModp(-x)

	    # Extended Euclidean algorithm.
	    s, old_s = 0, 1
	    t, old_t = 1, 0
	    r, old_r = self.p, x

	    while r != 0:
	        quotient = old_r // r
	        old_r, r = r, old_r - quotient * r
	        old_s, s = s, old_s - quotient * s
	        old_t, t = t, old_t - quotient * t

	    gcd, k, y = old_r, old_s, old_t

	    assert gcd == 1
	    assert (x * k) % self.p == 1

	    return k % self.p


	def add(self, P1,P2):
		"""
		Take in two points, draw a line from one to the other. At the third point of intersection with the elliptic curve on the line, reflect across the x axis.
		This defines a binary operation of addition on the elliptic curve which is abelian, always invertible, and associative. In other words it defines a group law.
		INPUTS: P1=(x1,y1), P2 = (x2,y2)
		OUTPUTS: P1 + P2 = (x3,y3)
		"""

		if P1 == INF_POINT: # i.e. P1 is the additive identity
			return P2
		if P2 == INF_POINT: # i.e. P2 is the additive identity
			return P1

		x1 = P1[0]
		y1 = P1[1]
		x2 = P2[0]
		y2 = P2[1]

		if self.equalModp(x1,x2) and self.equalModp(y1,-y2): #in this case the points are negatives of each other in the EC group law
			return None 									 #since vertical lines dont intersect the curve, their sum goes to infinity
		if self.equalModp(x1,x2) and self.equalModp(y1,y2):
			u =  self.reduceModp(3 * x1 * x1 + self.a) * self.inverseModp(2*y1) # geometrically this is the slope of the tangent line to the curve at the point ( implicitly differentiate y^2 = x^3 +ax +b)
		else:
			u = self.reduceModp(y1 - y2) * self.inverseModp(x1 - x2) #geometrically its the slope of the line throught the points
		v = self.reduceModp(y1-u*x1)		#geometrically this is the y-intercept of the line (either the tangent or through the points depending on the above if-else)
		x3 = self.reduceModp(u*u - x1 - x2) #the x-coordinate of P1 + P2
		y3 = self.reduceModp(-u*x3-v)       #the y-coordinate of P1 + P2

		return(x3,y3)

	def testAssociativity(self):
		n = len(self.points)
		for i in range (n):
			for j in range(n):
				for k in range(n):
					P = self.add(self.points[i], self.add(self.points[j], self.points[k]))
					Q = self.add(self.add(self.points[i], self.points[j]), self.points[k])
					if P != Q:
						return False
		return True

	def multiply(self, n, P):
		"""
		Implements "double and add method". For n = m_0 + m_1 *2 + m_2 * 2^2 + ... + m_r 2^r
		compute nP = m_0P + m_1 * 2P + m_2 * 2^2 P + ... + m_r * 2^r P

		this is a faster O(log n) method than the naive multiplication, which is exponential
		"""
		Q = INF_POINT
		binary_n = tobinary(n)
		for x in binary_n:
			if x == 1:
				Q = self.add(P,Q)
			P = self.add(P,P)
		return Q





if __name__ == "__main__":
	p = 1

	while not isprime(p) or p < 4:
		p = int(input("Enter a prime number (> 3) to calculate the number of elliptic curves modulo that prime."))
	count = 0
	for a in range(p):
		for b in range(p):
			ec = EllipticCurve(a,b,p)
			ec.definePoints()
			if ec.discriminant() == 0:
				continue

			count += 1
			print("y^2 = " + "x^3 + " + str(a)+"x + " + str(b))
			print( "a= " + str(a) + "\tb= " +str(b))
			print("discriminant= " + str(ec.discriminant()))
			print("number of points = " + str(ec.numberPoints()))
			print("associative=" + str(ec.testAssociativity()))
			ec.printPoints()
			print("="*21)

	#print(0)
	print("The number of elliptic curves over F_ " + str(p) + " is " + str(count))


