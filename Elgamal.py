#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, random, base64, time
import ECCkeyGen as ECC


class ELGAMAL:
	p =0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF 
	a =0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC 
	b =0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93 
	n =0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123 
	Gx=0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7 
	Gy=0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
	G =(Gx,Gy)

	def egcd(self,a, b):
		if a == 0:
			return (b, 0, 1)
		else:
			g, y, x = self.egcd(b % a, a)  # g为公因子
			return (g, x - (b // a) * y, y)

	def modinv(self,a, m):
		g, x, y = self.egcd(a, m)
		if (g != 1):
			print('modular inverse does not exist')
		else:
			return x % m

	def PointAdd(self,a,p,A,B):
		if A[0]==-1:
			return B
		if B[0]==-1:
			return A
		if A[0]==B[0]:
			if A[1]!=B[1]:
				return(-1,-1)
			else:
				lam=(((3*(A[0]**2)+a)%p)* self.modinv(2*A[1], p))%p
		else:
			lam=(((B[1]-A[1])%p)* self.modinv((B[0]-A[0])%p, p))%p
		x3=(lam**2-A[0]-B[0] )% p
		y3=(lam*(A[0]-x3)-A[1]) % p
		return (x3,y3)
		
	def MultipyPoint(self,n,A,a,p):   #借鉴了模重复平方计算法
		D=(-1,-1)
		E=bin(n)[2:]
		for i in range(len(E)):
			D=self.PointAdd(a,p,D,D)
			if E[i]=="1":
				D=self.PointAdd(a,p,D,A)
		return D

	def __init__(self,message,d):
			self.message=message
			self.d=d
		
	def bytes2int(self,text,l,r): #加密输入l=31,解密输入l=32
		b=text
		data = []
		for i in range(r):
			a=b[:l]
			c = 0
			for j in range(l):
				c+=a[j]<<(8*(l-j-1))
			data.append(c)
			b=b[l:]
		return data
		
	def int2bytes(self,data,l):    #解密输出l=31,加密输出l=32
		text = []
		for i in data:
			A = i
			for j in range(l)[::-1]:
				text.append((A >> 8*j) % 0x100)
		text = bytes(text)
		return text
		
	def MessageDiv(self,A):
		if (len(A))%31!=0:
			A=A+bytes(31-(len(A))%31)
		r=len(A)//31
		return self.bytes2int(A,31,r)

	def encrypt(self,message,d):
		Message = bytes(message, encoding='UTF-8')
		block = self.MessageDiv(Message)
		p =0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF 
		a =0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC 
		b =0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93 
		n =0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123 
		Gx=0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7 
		Gy=0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
		Qx = d
		Qy = Qx
		G =(Gx,Gy)
		X1=ECC.MultipyPoint(Qx,G,a,p)
		Qx = X1[0]
		Qy = X1[1]
		Q = (Qx,Qy)

		data = []
		for i in block:
			flag = False
			while not flag:
				k=random.randrange(300,n-1)
				X1=ECC.MultipyPoint(k,G,a,p)
				X2=ECC.MultipyPoint(k,Q,a,p)
				if X2[0]!=None:
					flag=True
			C=X2[0]*i%n
			data.append(X1[0])
			data.append(X1[1])
			data.append(C)
		text = base64.b64encode(self.int2bytes(data,32))
		text = str(text, encoding="ascii")
		print(text)
		return text

	def decrypt(self,message,d):
		Message = bytes(message, encoding='ascii')
		message = base64.b64decode(Message)
		p =0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF 
		a =0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC 
		b =0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93 
		n =0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123 
		r=len(message)//96
		C = self.bytes2int(message,32,r*3)
		data = []
		for i in range(r): 
			X1=(C[0],C[1])
			X2=ECC.MultipyPoint(d,X1,a,p)
			V=ECC.modinv(X2[0], n)
			data.append((C[2]*V)%n)
			C=C[3:]
		print(self.int2bytes(data,31).decode('UTF-8').strip(chr(0)))
		return self.int2bytes(data,31).decode('UTF-8').strip(chr(0))

if __name__ == "__main__":
	s1=ELGAMAL("哈哈",1)
	s1.encrypt("哈哈",1)
	s2=ELGAMAL("EP1eO942vNwVOXB9pq+fywLUrF3QPWT0O518e8t2EaRc0Tk7/P67OLqfd5mkNmvrGErRwGSnDXKcmm7HV6EXBkN558/KHi8BLimjEmFTFSEK9cgEiv32bCNE/VDvehfv",1)
	s2.decrypt("EP1eO942vNwVOXB9pq+fywLUrF3QPWT0O518e8t2EaRc0Tk7/P67OLqfd5mkNmvrGErRwGSnDXKcmm7HV6EXBkN558/KHi8BLimjEmFTFSEK9cgEiv32bCNE/VDvehfv",1)