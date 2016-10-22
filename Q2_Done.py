#!/usr/bin/env python
#Assignment 1 [DES]
#Fundamental Concepts of Cryptography (314256)
#Alex Lim Siew Zhuan 	15597746

import string
import random
import binascii
import os # for md5sum check
################################################################# TABLES
PC1 		=  [56,48,40,32,24,16, 8,
				 0,57,49,41,33,25,17,
				 9, 1,58,50,42,34,26,
				18,10, 2,59,51,43,35,
				62,54,46,38,30,22,14,
				 6,61,53,45,37,29,21,
				13, 5,60,52,44,36,28,
				20,12, 4,27,19,11, 3]	
				
PC2 		=  [13,16,10,23, 0, 4,
 				 2,27,14, 5,20, 9,
				22,18,11, 3,25, 7,
				15, 6,26,19,12, 1,
				40,51,30,36,46,54,
				29,39,50,44,32,47,
				43,48,38,55,33,52,
				45,41,49,35,28,31]		

IP_order 	=  [57,49,41,33,25,17, 9, 1,
				59,51,43,35,27,19,11, 3,
				61,53,45,37,29,21,13, 5,
				63,55,47,39,31,23,15, 7,
				56,48,40,32,24,16, 8, 0,
				58,50,42,34,26,18,10, 2,
				60,52,44,36,28,20,12, 4,
				62,54,46,38,30,22,14, 6]
			
table_E		=  [31, 0, 1, 2, 3, 4,
				 3, 4, 5, 6, 7, 8,
				 7, 8, 9,10,11,12,
				11,12,13,14,15,16,
				15,16,17,18,19,20,
				19,20,21,22,23,24,
				23,24,25,26,27,28,
				27,28,29,30,31, 0]

PerP 		=  [15, 6,19,20,28,11,
				27,16, 0,14,22,25,
				 4,17,30, 9, 1, 7,
				23,13,31,26, 2, 8,
				18,12,29, 5,21,10,
				 3,24]
		 
IPerP 		=  [39, 7,47,15,55,23,63,31,
				38, 6,46,14,54,22,62,30,
				37, 5,45,13,53,21,61,29,
				36, 4,44,12,52,20,60,28,
				35, 3,43,11,51,19,59,27,
				34, 2,42,10,50,18,58,26,
				33, 1,41, 9,49,17,57,25,
				32, 0,40, 8,48,16,56,24]

num_leftsh 	=  [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
############################################################## END TABLE
def SBOX(i,j,box_num):
	sboxes = [
			# S1 - 0
			[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
			 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
			 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
			 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

			# S2 - 1
			[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
			 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
			 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
			 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

			# S3 - 2
			[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
			 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
			 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
			 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

			# S4 - 3
			[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
			 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
			 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
			 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

			# S5 - 4
			[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
			 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
			 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
			 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

			# S6 - 5
			[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
			 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
			 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
			 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

			# S7 - 6
			[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
			 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
			 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
			 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

			# S8 - 7
			[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
			 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
			 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
			 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
		]				
	return sboxes[box_num][(i*16)+j] #output dec
	
#################################################################   KEYG
def key_gen(K,C):
	PC_1_Key = PC_1(K) #generate PC_1 Key 56bits
	C_0 = PC_1_Key[0:len(PC_1_Key)/2]	#1st half
	D_0 = PC_1_Key[len(PC_1_Key)/2: ]	#2nd half

	KEY_set	= {}
	C_1 	= C_0
	D_1 	= D_0
	
	for key_loop in range(16):
		C_1,D_1 = LS(C_1,D_1,key_loop)
		KEY_set[key_loop] = C_1+D_1

	KEY 	= KEY_set
	for b in range(len(KEY)):
		KEY[b] = PC_2(KEY[b])
		KK = KEY.values()	
		
	if C == 1:
		KK = [KK[i] for i in [15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]]
		
	return KK

################################################# SUB FUNCTION FOR K GEN
def ascii_8_K():
	usr_input_parity={}
	usr_input = raw_input("Input Key (Press return for random keys):")
	len_usr_input = len(usr_input) #should be 8 characters

	#padding or chopping
	if len_usr_input < 8:
		add_on = ''.join(random.choice(string.letters)\
		 for pp in range(8-len_usr_input))
		 
		usr_input = usr_input + add_on
		len_usr_input = len(usr_input)
	elif len_usr_input > 8:
		usr_input = usr_input[:8]
		len_usr_input = len(usr_input)
	
	print 'Key Entered: '+ usr_input
	
	for x in range(len_usr_input):
		chr_ascii = bin(ord(usr_input[x]))[2:] 
		#remove the 0b in front
		chr_ascii_len = len(chr_ascii)
		
		if chr_ascii_len < 7:				
			# for 6bits number case
			chr_ascii = format(ord(usr_input[x]),'07b')+'0'
			#remove the 0b in front
			chr_ascii_len = len(chr_ascii)
			
		#parity check - odd
		flag_ones = 0
		for i in range(chr_ascii_len):
			if chr_ascii[i] == '1':
				flag_ones = flag_ones + 1
			else:
				flag_ones = flag_ones
			
			if flag_ones % 2 == 0: 
				#even number of ones in 7 bits
				parity = 1
			else:
				parity = 0
		usr_input_parity[x] = (int(chr_ascii,2)<<1)\
		 + int(bin(parity),2)
		
	K_list = [bin(usr_input_parity[j])[2:]\
	 for j in range(len(usr_input_parity))] #bin
	 
	K = ''.join(K_list)
	return K,usr_input

def PC_1(K):
	susun_key = [K[i] for i in PC1]
	susun_key = ''.join(susun_key)
	return susun_key
	
def PC_2(K):
	susun_key = [int(K[i],2) for i in PC2]
	
	return susun_key
	
def LS(C,D,loop):
	#the leftshit numebrs

	shifter_CD = range(num_leftsh[loop],len(C))
	
	for g in range(num_leftsh[loop]):
		shifter_CD.append(g)
	
	C_1 = [C[c] for c in shifter_CD] #shift
	D_1 = [D[d] for d in shifter_CD] #shift
	return C_1,D_1	
##############################################################  KEYG-END

def IP(M):
	chopped = {}
	len_M = len(M) 
	bin_M = str_bit(M)
	bin_M = ''.join([bin(bin_M[a])[2:] for a in range(len(bin_M))])
	bin_len_M = len(bin_M)
	#$chopping and padding
	
	if bin_len_M <= 64:
		#for less than 64 bits
		padded_val = (64-bin_len_M) #important value for padding number
		add_on = format(ord(chr(padded_val/8)),'08b')*(padded_val/8) #PKCS5
		bin_M = bin_M + add_on
		bin_len_M = len(bin_M)
		chopped[0] = bin_M
		
	elif bin_len_M > 64:
		#for more than 64 bits
		the_rest = bin_M
		a = 0
		loop_con = 0
		while loop_con != 1:
			chopped[a],the_rest,loop_con,padded_val = rec_chhopping(the_rest,loop_con)
			if len(the_rest) == 0:
				loop_con = 1
			else:
				a = a + 1
				
	M_IP_order = {}
	for i in range(len(chopped)):
		M_IP_order[i] = [int(chopped[i][j],2) for j in IP_order]

	return M_IP_order

def rec_chhopping(bin_M,loop_con):
	#reculsively chopping the data into 64 bits 
	padded_val = 0
	
	len_bin_M = len(bin_M)
	chopped = bin_M[:64]

	if len_bin_M < 64:
		padded_val = (64-len_bin_M)%64
		the_rest = format(ord(chr(padded_val/8)),'08b')*(padded_val/8) #PKCS5
		chopped = chopped + the_rest
		loop_con = 1

	else:
		the_rest = bin_M[64:]
	
	return chopped,the_rest,loop_con,padded_val


def IP_R(RL):
	IP_RL = [int(bin(RL[i])[2:]) for i in IPerP]
	return IP_RL

def L_R_0(IP_data): #ok
	L_0 = {}
	R_0 = {}
	
	for a in range(len(IP_data)):
		L_0[a] = IP_data[a][:32]
		R_0[a] = IP_data[a][32:]

	return L_0.values(),R_0.values()
	
def bit_str(data,C):
	ans = ''
	bit_flg = 0
	for x in range(len(data)):
			bit_flg += data[x]<<(7-(x%8))
			if (x%8) == 7:
					ans = ans + chr(bit_flg)
					bit_flg = 0
	if C == True:
		padd = ord(ans[-1])
		if padd >= 1 and padd < 8: 
			ans = ans[:-padd]
		else:
			ans = ans
	return ans

def str_bit(data_s):
	data_b = {}
	data_b = ''.join([format(int(binascii.hexlify(data_s[a]), 16),'08b') for a in range(len(data_s))])
	data_b = [int(data_b[a]) for a in range(len(data_b))]
	return data_b

def swf(msg_IP,KEYS,C):
	ans = []
	#for a in range(len(msg_IP)):
	L_0,R_0 = L_R_0(msg_IP)	
	L16, R16 = L_R_n(L_0,R_0,KEYS)
	for f in range(len(R16[16])):
		RL = R16[16][f]+L16[16][f]
		IP_RL = IP_R(RL)
		ans = ans + IP_RL
		
	bin_ans = ''.join([bin(ans[a])[2:] for a in range(len(ans))])
	return bit_str(ans,C)

def function_RK(R,K):
#32 bits of R ; 48bits of K eturn 32 bits
	R_E = [R[i] for i in table_E] # checked with manualy #checked
	
	#R XOR K
	R_E_XOR_K = [R_E[i] ^ K[i] for i in range(len(K))]

	#S-BOXES
	# split the R_E_XOR_K 48/8 = 6 bits each S box
	REK_split={}
	b = 0
	for a in range(8):
		REK_split[a] = R_E_XOR_K[b:b+6]
		b = b + 6
		
	REK_split = REK_split.values()

	i_sbox	= {}
	j_sbox	= {}
	SB_DATA	= {}

	#extract i data
	for a in range(8):
		i_sbox[a] = int(bin(REK_split[a][0])[2:] + bin(REK_split[a][5])[2:],2)
		 
	#extract j data
	for a in range(8):
		j_sbox[a] = int(bin(REK_split[a][1])[2:] + bin(REK_split[a][2])[2:] + bin(REK_split[a][3])[2:] + bin(REK_split[a][4])[2:],2)
	
	# get value from S box
	for s in range(8):
		SB_DATA[s] = format(SBOX(i_sbox[s],j_sbox[s],s),'04b')
	
	SB_DATA = ''.join(SB_DATA[e] for e in range(len(SB_DATA)))

	funct = [int(SB_DATA[w]) for w in PerP]
	
	return funct

def L_R_n(L,R,K): #input L_0 R_0 Keys and Loop_counter = 1
	n = 1
	b = 0
	LL = {}
	RR = {}
	temp = {}
	LL[0] = L  #-> {0: [[L_Pt1],[L_Pt2],[L_Pt3]...]}
	RR[0] = R
	
	while n<17:
		LL[n] = RR[n-1]
		##############################
		#-L[0]-> | PART1(32) | PART2(32) | PART3(32) |...
		#-L[1]-> | PART1(32) | PART2(32) | PART3(32) |...	
		
		##############################
		#-R[0]-> | PART1(32) | PART2(32) | PART3(32) |...
		#-R[1]-> | PART1(32) | PART2(32) | PART3(32) |...
		for t in range(len(L)):
			fun_RK = function_RK(RR[n-1][t],K[n-1])
			temp[t] = list(map(lambda x, y: x ^ y, LL[n-1][t], fun_RK))
		RR[n] = temp.values()
		n = n + 1

	return LL,RR
	
def main():
	enc_dec = raw_input('Encrypt: -e | Decrypt: -d | String input: -s :')	
	
	K,usr_input	= ascii_8_K()    #input 8 chrs and generate KEY with parity 64bits
	
	if enc_dec == '-e':
		print '==Encryption=='
		filename = raw_input('File Location: ')
		md5 = os.popen("md5sum "+filename).read()
		print 'MD5SUM CHECK: ' + md5[:32]
		txt_data = open(filename,'r')
		save_name = '[ENC_'+ usr_input +']'+filename
		save_data = open(save_name,'w')
		code = False
		flag = True
		
	elif enc_dec == '-d':
		print '==Decryption=='
		filename = raw_input('File Location: ')
		md5 = os.popen("md5sum "+filename).read()
		print 'MD5SUM CHECK: ' + md5[:32]
		txt_data = open(filename,'r')
		save_name = '[DEC]'+filename
		save_data = open(save_name,'w')
		
		code = True
		flag = True
	else:
		flag = False
	
	if flag == True:
		msg = txt_data.read() #list of data
		KEYS 	= key_gen(K,code)		#0 for encryption
		msg_IP = IP(msg).values() # 3D_MAT msg_IP[a][b]
		msg = swf(msg_IP,KEYS,code)    #0 for encryption
		print msg
		save_data.write(msg)
		print '\n'
		print 'File Saved as: ' + save_name
		save_data.close()
		md5 = os.popen("md5sum "+save_name).read()
		print 'MD5SUM CHECK: ' + md5[:32]
		
	
	elif flag == False:
		print '==Encryption=='
		KEYS 	= key_gen(K,0)		#1 for decryption
		msg = raw_input('Input String :\n')
		msg_IP = IP(msg).values() # 3D_MAT msg_IP[a][b]
		msg = swf(msg_IP,KEYS,0)	#1 for decryption
		print msg	
	
		print '==Decryption=='
		KEYS 	= key_gen(K,1)		#1 for decryption
		#msg = raw_input('Input Text')
		msg_IP = IP(msg).values() # 3D_MAT msg_IP[a][b]
		msg = swf(msg_IP,KEYS,1)	#1 for decryption
		print msg	
		
	return 0

if __name__ == '__main__':
	while True:
		main()
		print '\n -- reset --\n'
