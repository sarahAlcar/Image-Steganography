import binascii
import io
from scipy import misc
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
#--------------------------------------------------------------------------------
# Digital Image Steganography
# find_msg.py is responsable for decoding the message information from the image 
#--------------------------------------------------------------------------------
def text_bits(text):
    letter = ''
    binary = ''
    bnry = ''
    for i in range(len(text)):
        letter = ord(text[i])
        binary = (bin(letter)[2:]).zfill(8)
        bnry = bnry + binary
    return bnry
#--------------------------------------------------------------------------------

def bits_text(text):
    convert = ''
    ascii =''
    binary = ''
    index = 0
    for i in range(len(text)/8):
        for j in range(8):
            binary = binary + text[index]
            index = index + 1
        ascii = chr(int(binary,2))
        convert = convert + ascii 
        binary = ''  
         
    return convert

#--------------------------------------------------------------------------------
def dec_to_bin(x):
    bnry = '{0:08b}'.format(x)
    return bnry
#--------------------------------------------------------------------------------

def bin_to_dec(x):
    dec = int(x, 2)
    return dec
#--------------------------------------------------------------------------------

def conv_channel_matrix_binary (channel):
    newmat = np.chararray(shape = channel.shape, itemsize=8)
    for i in range(channel.shape[0]):
        for j in range(channel.shape[1]):
                newmat[i,j] = dec_to_bin(channel[i, j])
    return newmat
#--------------------------------------------------------------------------------

def conv_channel_matrix_ascii (channel):
    newmat = np.zeros(shape = channel.shape)
    for i in range(channel.shape[0]):
        for j in range(channel.shape[1]):
                newmat[i,j] = bin_to_dec(channel[i, j])
    return newmat
#--------------------------------------------------------------------------------
def change_bit (binary, bin_pos, letter):
    index = 7-bin_pos
    bit = binary[index]
    s=''
    if (bit != letter):
        if bit == '0' and letter == '1':
            b_s = bytearray(binary)
            b_s[index] = '1'
            s = str(b_s)
            
        elif (bit == '1' and letter == '0'):
            b_s = bytearray(binary)
            b_s[index] = '0'
            s = str(b_s)
    else:
        s = binary
    return s

#--------------------------------------------------------------------------------

def join_channels (img,R,G,B):
    img[:,:,0] = R
    img[:,:,1] = G
    img[:,:,2] = B
    return img

#--------------------------------------------------------------------------------
def find_message (r,g,b,bin_pos):
    R = conv_channel_matrix_binary (r)
    G = conv_channel_matrix_binary (g)
    B = conv_channel_matrix_binary (b)
    channel = 0
    ir = 0
    jr = 0
    ig = 0
    jg = 0
    ib = 0
    jb = 0
    index = 7-bin_pos
    binary = ''
    phrase = ''
    ascii = ''
    while (ascii != chr(26)):
       if (channel%3 == 0):
            if (len(binary) < 8):
                if (jr<(R.shape[1]-1)): 
                    number =  R[ir,jr]
                    binary = binary + number[index]
                    jr = jr+1
                elif(ir < (R.shape[0]-1) and (jr == R.shape[1]-1)):
                    ir = ir+1
                    jr = 0
                    number =  R[ir,jr]
                    binary = binary + number[index]
       if (channel%3 == 1):
            if (len(binary) < 8):
                if (jg<(G.shape[1]-1)): 
                    number =  G[ig,jg]
                    binary = binary + number[index]
                    jg = jg+1
                elif(ig < (G.shape[0]-1) and (jg == G.shape[1]-1)):
                    ig = ig+1
                    jg = 0
                    number =  G[ig,jg]
                    binary = binary + number[index]
       if (channel%3 == 2):
            if (len(binary) < 8):
                if (jb<(B.shape[1]-1)): 
                    number =  B[ib,jb]
                    binary = binary + number[index] 
                    jb = jb+1
                elif(ib < (B.shape[0]-1) and (jb == B.shape[1]-1)):
                    ib = ib+1
                    jb = 0
                    number =  B[ib,jb]
                    binary = binary + number[index]
       channel = channel + 1
       if (len(binary) == 8):
             ascii = chr(int(binary,2))
             phrase = phrase + ascii
             binary = ''
    #left_text = text.partition(chr(26))[0]
    #phrase = left_text
    return phrase

#-Main-------------------------------------------------------------------

#Reads Image
imgName= raw_input()
img = misc.imread(imgName+'.png')

#Reads bit change position
pos = raw_input()
bin_pos = int(pos)

r = img[:,:,0]
g = img[:,:,1]
b = img[:,:,2]

print find_message (r,g,b,bin_pos) 


























