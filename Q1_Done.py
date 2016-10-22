#!/usr/bin/env python
#Assignment 1 [Affine Cipher]
#Fundamental Concepts of Cryptography (314256)
#Alex Lim Siew Zhuan 	15597746


import os # for md5sum check
#Extended Euclidean Algorithm:
def inve(a,m):
    xb, yb, rb = 1, 0, a
    x , y , r  = 0, 1, m
    while r != 0:
        q = rb // r
        x, y, r, xb, yb, rb = (xb - q * x), (yb - q * y), (rb - q * r), x, y, r
    return xb
    
from fractions import gcd

def main():
	loop = 1
	while loop:
		enc={}
		dec={}
		ncap = 'a'
		CAP='A'

		filename = raw_input("Input the file with its path : >  ")
		
		txt_data = open(filename,'r')
		md5 = os.popen("md5sum "+filename).read()
		print 'MD5SUM CHECK: ' + md5[:32]
		
		data = txt_data.read() #list of data

		enc_dec = (raw_input("-e: Encrypt; -d: Decrypt : > "))

		
		if enc_dec == '-e' or enc_dec == '-d':

			a = int(raw_input("Insert Value 'a' which co-prime with 26: 1 3 5 .. 25: > "))
			b = int(raw_input("Insert Value 'b' from 1-25: > "))

			if enc_dec == '-d' and gcd(a,26)==1 and b >= 1 and b < 26:
				name_f = '[DEC]_'+filename
				dencypt = open(name_f,'w')
				
				inv_a = inve(a,26)

				for s in range(len(data)):
					
					if data[s].isalpha():
							if data[s].isupper():
								alpha = CAP
							else:
								alpha = ncap

							dec[s] = chr((inv_a*(ord(data[s])-ord(alpha)-b))%26+ord(alpha))
							
					else:
						dec[s]=data[s]

					dencypt.write(dec[s])
					
				print "data decrypted and saved as:"
				print name_f
				dencypt.close()   
				md5 = os.popen("md5sum "+name_f).read()
				print 'MD5SUM CHECK: ' + md5[:32]
				loop = 0
    
				
			elif enc_dec == '-e' and gcd(a,26)==1 and b >= 1 and b < 26:
				name_f = '[ENC-'+str(a)+'_'+str(b)+']_'+filename
				encypt = open(name_f,'w')
				
				for x in range(len(data)):
					
					if data[x].isalpha():
						if data[x].isupper():
							alpha = CAP
						else:
							alpha = ncap
							
						enc[x] = chr(((a*(ord(data[x])-ord(alpha))+b)%26)+ord(alpha))
						
					else:
						enc[x]=data[x]
						
					encypt.write(enc[x])
					
				print "data encrypted and saved as:"
				print name_f 
				encypt.close()
				md5 = os.popen("md5sum "+name_f).read()
				print 'MD5SUM CHECK: ' + md5[:32]
				loop = 0
				
			else:
				print "ERROR: illegal value of a or b; please try again..\n\n"
				
			if enc_dec == '-exit' or enc_dec == 'exit':
				loop = 0
				
		else:
				print "ERROR: either -e or -d; please try again..\n\n"
	return 0

if __name__ == '__main__':
	while True:
		main()
		print '\n -- reset --\n'
