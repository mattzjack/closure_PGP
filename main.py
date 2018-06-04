import random

def int2bin_str(d):
    return bin(d)[2:]

def txt2int(s):
    result = ''
    for c in s:
        result += '{:03d}'.format(ord(c))
    if result.startswith('0'):
        result = '999' + result
    return int(result)

def int2txt(d):
    s = str(d)
    if len(s) % 3 != 0:
        print('bad int')
        return
    result = ''
    for i in range(0, len(s), 3):
        sub = s[i : i + 3]
        if sub == '999': continue
        result += chr(int(sub))
    return result

def gen_one_time_pad(M2):
    result = ''
    bits = ['0', '1']
    for _ in range(len(M2)):
        result += random.choice(bits)
    return result

def one_time_pad(x, y):
    result = ''
    for i in range(len(x)):
        if x[i] != y[i]:
            result += '1'
        else:
            result += '0'
    return result

def extended_euc(a, b):
    if a == 0: return b
    if b == 0: return a
    r0 = a
    r1 = b
    s0 = 1
    s1 = 0
    t0 = 0
    t1 = 1
    q1 = r0 // r1
    r2 = r0 - q1 * r1
    s2 = s0 - q1 * s1
    t2 = t0 - q1 * t1
    while r2 != 0:
        r0, r1 = r1, r2
        s0, s1 = s1, s2
        t0, t1 = t1, t2
        q1 = r0 // r1
        r2 = r0 - q1 * r1
        s2 = s0 - q1 * s1
        t2 = t0 - q1 * t1
    return (r1, s1, t1)

def discrete_exponentiation(N, b, e):
    d = {1: b}
    last_e = 1
    next_e = 2
    while next_e <= e:
        d[next_e] = (d[last_e] ** 2) % N
        last_e = next_e
        next_e *= 2
    binary = list(bin(e))
    result = 1
    curr = 1
    while binary[-1] != 'b':
        if binary.pop() == '1':
            result = (result * d[curr]) % N
        curr *= 2
    return result

def gen_pub_pri_key(P, Q):
    N = P * Q
    phi = (P - 1) * (Q - 1)
    D = random.randrange(phi)
    (one, E, t) = extended_euc(D, phi)
    while (one != 1):
        D = random.randrange(phi)
        (one, E, t) = extended_euc(D, phi)
    return (N, D, E)

def pub_key_encr(N, E, M):
    (valid, s, t) = extended_euc(M, N)
    if not (valid == 1 and M < N):
        print('bad message')
        return
    raised_to_public = discrete_exponentiation(N, M, E)
    return raised_to_public

def pri_key_decr(N, D, code):
    return discrete_exponentiation(N, code, D)

def closure_PGP(N, E, plaintext):
    M_bin = int2bin_str(txt2int(plaintext))
    pad_bin = gen_one_time_pad(M_bin)
    padded_bin = one_time_pad(M_bin, pad_bin)
    padded_dec = int(padded_bin, 2)
    pad_dec = int(pad_bin, 2)
    pad_encr = pub_key_encr(N, E, pad_dec)
    return (padded_dec, pad_encr)

def closure_PGP_decode(N, D, X):
    (padded_dec, pad_encr) = X
    pad_dec = pri_key_decr(N, D, pad_encr)
    pad_bin = int2bin_str(pad_dec)
    padded_bin = int2bin_str(padded_dec)
    while len(padded_bin) < len(pad_bin):
        padded_bin = '0' + padded_bin
    while len(pad_bin) < len(padded_bin):
        pad_bin = '0' + pad_bin
    M_bin = one_time_pad(padded_bin, pad_bin)
    M_dec = int(M_bin, 2)
    plaintext = int2txt(M_dec)
    return plaintext
