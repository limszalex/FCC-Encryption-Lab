#!/usr/bin/env python
#Assignment 2 [RSA]
#Fundamental Concepts of Cryptography (314256)
#Alex Lim Siew Zhuan 	15597746

import os # for md5sum check
import random
from fractions import gcd

def inve(a,m):
    xb, yb, rb = 1, 0, a
    x , y , r  = 0, 1, m
    while r != 0:
        q = rb // r
        x, y, r, xb, yb, rb = (xb - q * x), (yb - q * y), (rb - q * r), x, y, r
    return xb%m

def a_pow_b_mod_n(a,b,n):
    c = 0
    f = 1
    binb = bin(b)[2:]
    k = len(binb)-1
    i = k
    while i >= 0:
        c = 2*c
        f = (f*f)%n
        if binb[k-i] == '1': # k-i as bigendian issue
            c = c + 1
            f = (f*a)%n
        i = i - 1
    #ans for a^b mod n
    return f

def prime_check(p):
    #assume no negative 'p'
    
    if p > 1:
        r_count = 0
        a = 0
        #Based on Lehmann Algorithm
        while a < (p-1):
            fa = random.randrange(2,p)
            r = a_pow_b_mod_n(fa,(p-1)/2,p)
            
            if r == 1 or r == p-1:
                r_count = r_count + 1
                
            a = a + 1

        if (float(r_count)/float(a))*100 >= 90:
            return 1 # TRUE
        else:
            return 0 # FALSE
    else:
        return 0

def p_q_checker(p,q):
    #return 0 if one of them is not prime and must unique
    if p - q == 0:
        return 0
    else:
        return prime_check(p)*prime_check(q)

def char_2ord(text):
    dat = {}
    #return ["099023","100120","100ppp","pppppp"]
    #return ["099023","100120","100111","111111"]
    #return ["099023","100120","100098","000000"]
    len_str = len(text)

    if len_str%2 != 0:
        flag_odd = 1
        len_str = len_str - 1 #len_str%2
    else:
        flag_odd = 0

    a = 0
    b = 0
    while a < len_str:        
        if a%2 == 0:
            dat[b] = "%s%s" %("{:0>3d}".format(ord(text[a])),"{:0>3d}".format(ord(text[a+1])))
            b = b + 1
            #print dat
        a = a + 1
                
    if flag_odd == 1:
        dat[b] = "%s" %("{:0>3d}".format(ord(text[a])) + str(len(text)%2)*3) #for padding
        #print dat
        b = b + 1

    dat[b] = "%s" %(str(len(text)%2)*6) # for padding
    
        #print dat
    #change back to list
    data = [dat[a] for a in range(len(dat))]
    #print data
    return data

def ord_2str(text):
    #098097 - > 'ba';
    sp_dat = spliter(text,'123')
    sp_data = [chr(int(sp_dat[b])) for b in range(len(sp_dat))]
    
    if sp_data[len(sp_data)-1] == chr(111):
        
        sp_data[len(sp_data)-1]= ''
        sp_data[len(sp_data)-2]= ''
        sp_data[len(sp_data)-3]= ''
##
    elif sp_data[len(sp_data)-1] == chr(000):
        sp_data[len(sp_data)-1] = ''
        sp_data[len(sp_data)-2] = ''
    
    return sp_data



def enc(ord_str,e,n):
    enc_dat = {}
    a = 0
    while a < len(ord_str):
        enc_dat[a] = a_pow_b_mod_n(int(ord_str[a]),e,n)
        a = a + 1
        
    enc_data = ["{num:0>{size}d}".format(num = enc_dat[b],size = len(str(n))) for b in range(len(enc_dat))]
    return ''.join(enc_data)+str()

def spliter(enc_str,n):
    splited = {}
    a = 0
    L = 0
    R = len(str(n))
    
    while a < len(enc_str)/len(str(n)):
        splited[a] = enc_str[L:R]
        L = R
        R = R+len(str(n))
        a = a + 1
    return splited
    

def dec(enc_str,d,n):
    dec_dat = {}
    a = 0
    enc_data = spliter(enc_str,n)
    
    while a < len(enc_data):
        dec_dat[a] = a_pow_b_mod_n(int(enc_data[a]),d,n)
        a = a + 1
    
    dec_data = ["{:0>6d}".format(dec_dat[b]) for b in range(len(dec_dat))]
    return ''.join(dec_data)

def enc_chr(data):
    d_enc_chr = spliter(data,'99')
    dd_enc_chr = [chr(int(d_enc_chr[a])) for a in range(len(d_enc_chr))]
    return ''.join(dd_enc_chr)
    
def dec_ord(data):
    dd_chr = ["{:0>2d}".format(data[a]) for a in range(len(data))]
    return ''.join(dd_chr)
    


def key_setup():
    print "EG: 9697 9719 9721 9733 9739 9743 9749 9767 9769 9781 9787 9791 9803 9811"
    
    p = 0
    q = 0
    
    while p < 1000 or p > 10000:
        p = int(raw_input('input P = '))
		
    while q < 1000 or q > 10000:
        q = int(raw_input('input Q = '))
    
    if p_q_checker(p,q) == 1:
        print "Prime? \t= YES!"
    else:
        print "Prime? \t= NO!"
        print "System Exit!"
        exit()
    
    n = p*q
    print "n \t= %d"%n
    phi_n = (p-1)*(q-1)
    print "phi_n \t= %d"%phi_n

    e = int(raw_input('input e = '))
    
    if e < phi_n and gcd(e,phi_n) == 1:
        print '<&GCD? \t= YES!'
    else:
        print '<&GCD? \t= NO!'
        print "System Exit!"
        exit()
    
    d = inve(e,phi_n)
    print "d \t= %d"%d
    print "\n"
    return p,q,e,d,n,phi_n


#===============================================
#========================================== main
#===============================================

while 1:
    #========================================= INIT
    ord_str  = []
    the_data = []
    #========================================= INIT
    #Type Promp
    enc_dec = (raw_input("-e: Encrypt; -d: Decrypt; -s: String : > "))
    #=========================================== IO
    #I/O Promp
    if enc_dec == '-e' or enc_dec == '-d':
        flag_not_s = 1
        filename = raw_input("Input the file with its path : >  ")
        filee = open(filename,'r')
        md5 = os.popen("md5sum "+filename).read()
        print 'MD5SUM CHECK: ' + md5[:32]
        txt_data = filee.read()
        
    #Str Promp
    else:
        flag_not_s = 0
        txt_data = raw_input("Input String : >  ")
        enc_dec = '-s'
    #=========================================== IO
        




    #key
    p,q,e,d,n,phi_n = key_setup()





    if enc_dec == '-e' or enc_dec == '-s':
    #=================================== encryption
        #convert text to dec
        ord_str = char_2ord(txt_data)
        
        #enc file name
        if flag_not_s == 1:
            name_f = '[ENC-'+str(p)+'_'+str(q)+'_'+str(e)+']'
            encrypt = open(name_f,'w')
            
        #enc core
        enc_data = ''.join(enc(ord_str,e,n))
        #dec_str
        the_data = enc_chr(enc_data)
        
        
        if flag_not_s == 1:
        #write to IO
            #print the_data
            encrypt.write(the_data)
            print "Encrypted Text: %s\n"%name_f
            encrypt.close()
            md5 = os.popen("md5sum "+name_f).read()
            print 'MD5SUM CHECK: ' + md5[:32]
        else:
            print "Encrypted:\n%s"%the_data #enc text
    #=================================== encryption






    #=================================== condition
    if flag_not_s == 0:
        txt_data = the_data
    print '\n'
    #=================================== condition






    if  enc_dec == '-d' or enc_dec == '-s':    
    #=================================== decryption
        #convert text to dec
        ord_str = [ord(txt_data[a]) for a in range(len(txt_data))]
        #print ord_str
        #dec file name
        if flag_not_s == 1:
            name_f = '[DEC-'+str(p)+'_'+str(q)+'_'+str(e)+']'
            dencrypt = open(name_f,'w')

        #dec core
        dec_data = dec_ord(ord_str) #decript string into dec
        the_data = ''.join(ord_2str(dec(dec_data,d,n)))
        #print "%s"%the_data #dec text
        
        if flag_not_s == 1:
        #write to IO
            #print the_data
            dencrypt.write(the_data)
            print "Decrypted Text: %s\n"%name_f
            dencrypt.close()
            md5 = os.popen("md5sum "+name_f).read()
            print 'MD5SUM CHECK: ' + md5[:32]
        else:
            print "Decrypted:\n%s"%the_data #dec text
    #=================================== encryption

    ord_str  = []
    the_data = []
    print "======= RESET =======\n"
