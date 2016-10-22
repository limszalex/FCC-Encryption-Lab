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

#main

print "mod(17^(21),39) = %d"%a_pow_b_mod_n(17,21,39)
