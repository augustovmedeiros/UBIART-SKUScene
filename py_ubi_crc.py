# python ubiart (?) crc32 implementation by github.com/InvoxiPlayGames
# function usage - crc(bytearray), if using a string, crc(bytearray(uppercasestring, "utf8"))
# code licensing: don't be a dick with it, credit for general usage would be nice but not required
#                 if you use parts of this python script in your own project, credit is required
import math

def shifter(a, b, c):
    # the masks are because python likes to get excited with bit shifting
    d = 0
    a = (a - b - c) ^ (c >> 0xd)
    a = a & 0xffffffff
    b = (b - a - c) ^ (a << 0x8)
    b = b & 0xffffffff
    c = (c - a - b) ^ (b >> 0xd)
    c = c & 0xffffffff
    a = (a - c - b) ^ (c >> 0xc)
    a = a & 0xffffffff
    d = (b - a - c) ^ (a << 0x10)
    d = d & 0xffffffff
    c = (c - a - d) ^ (d >> 0x5)
    c = c & 0xffffffff
    a = (a - c - d) ^ (c >> 0x3)
    a = a & 0xffffffff
    b = (d - a - c) ^ (a << 0xa)
    b = b & 0xffffffff
    c = (c - a - b) ^ (b >> 0xf)
    c = c & 0xffffffff
    return a, b, c

def crc(data):
    i = 0
    a = 0x9E3779B9
    b = 0x9E3779B9
    c = 0
    length = len(data)
    
    if length > 0xc:
        while i < math.floor(length / 0xc):
            a += (((((data[i * 0xc + 0x3] << 8) + data[i * 0xc + 0x2]) << 8) + data[i * 0xc + 0x1]) << 8) + data[i * 0xc];
            b += (((((data[i * 0xc + 0x7] << 8) + data[i * 0xc + 0x6]) << 8) + data[i * 0xc + 0x5]) << 8) + data[i * 0xc + 0x4];
            c += (((((data[i * 0xc + 0xb] << 8) + data[i * 0xc + 0xa]) << 8) + data[i * 0xc + 0x9]) << 8) + data[i * 0xc + 0x8];
            i += 1
            a, b, c = shifter(a, b, c)
    
    c += length;
    i = length - (length % 0xc);
    
    decide = (length % 0xc) - 1
    if decide >= 0xa: c += data[i + 0xa] << 0x18;
    if decide >= 0x9: c += data[i + 0x9] << 0x10;
    if decide >= 0x8: c += data[i + 0x8] << 0x8;
    if decide >= 0x7: b += data[i + 0x7] << 0x18;
    if decide >= 0x6: b += data[i + 0x6] << 0x10;
    if decide >= 0x5: b += data[i + 0x5] << 0x8;
    if decide >= 0x4: b += data[i + 0x4];
    if decide >= 0x3: a += data[i + 0x3] << 0x18;
    if decide >= 0x2: a += data[i + 0x2] << 0x10;
    if decide >= 0x1: a += data[i + 0x1] << 0x8;
    if decide >= 0x0: a += data[i + 0x0];
    
    a, b, c = shifter(a, b, c)
    
    return c

def getCrc(string):
    return crc(bytearray(string.upper(), "utf8"))