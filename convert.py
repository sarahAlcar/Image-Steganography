import binascii
import io
from scipy import misc
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt

#--------------------------------------------------------------------------------
# Digital Image Steganography 
# convert.py is responsable for hiding the message information in the image 
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

def conv_matrix_int (channel):
    return channel.astype(int)
#--------------------------------------------------------------------------------

def get_binary (channel, i, j):
    binary = ''
    for i in range(channel.shape[0]):
        for j in range(channel.shape[1]):
                binary = channel[i, j]
    return binary
#--------------------------------------------------------------------------------

def join_channels (img,R,G,B):
    img[:,:,0] = R
    img[:,:,1] = G
    img[:,:,2] = B
    return img

#--------------------------------------------------------------------------------
def steganography (text_steg,R_steg,G_steg,B_steg, bp_steg,imG_steg):
    Rnew_steg = conv_channel_matrix_binary (R_steg)
    Gnew_steg = conv_channel_matrix_binary (G_steg)
    Bnew_steg = conv_channel_matrix_binary (B_steg)
    channel_steg = 0
    irs = 0
    jrs = 0
    igs = 0
    jgs = 0
    ibs = 0
    jbs = 0
    binary = ''

    for i in range(len(text_steg)):
        numberBin = text_steg[i]
        if (channel_steg%3 == 0):
            if (jrs < (Rnew_steg.shape[1]-1)):
                binary_steg = Rnew_steg[irs, jrs]
                Rnew_steg[irs, jrs] = change_bit (binary_steg, bp_steg, numberBin)
                jrs = jrs+1
            elif(irs < (Rnew_steg.shape[0]-1) and (jrs == Rnew_steg.shape[1]-1)):
                jrs=0
                irs=irs+1
                binary_steg = Rnew_steg[irs, jrs]
                Rnew_steg[irs, jrs] = change_bit (binary_steg, bp_steg, numberBin)  
        elif (channel_steg%3 == 1):
            if (jgs < (Gnew_steg.shape[1]-1)):
                binary_steg = Gnew_steg[igs, jgs]
                Gnew_steg[igs, jgs] = change_bit (binary_steg, bp_steg, numberBin)
                jgs = jgs+1
            elif(igs < (Gnew_steg.shape[0]-1) and (jgs == Gnew_steg.shape[1]-1)):
                jgs=0
                igs=igs+1
                binary_steg = Gnew_steg[igs, jgs]
                Gnew_steg[igs, jgs] = change_bit (binary_steg, bp_steg, numberBin)
        elif (channel_steg%3 == 2):
            if (jbs < (Bnew_steg.shape[1]-1)):
                binary_steg = Bnew_steg[ibs, jbs]
                Bnew_steg[ibs, jbs] = change_bit (binary_steg, bp_steg, numberBin)
                jbs = jbs+1
            elif(ibs < (Bnew_steg.shape[0]-1) and (jbs == Bnew_steg.shape[1]-1)):
                jbs=0
                ibs = ibs+1
                binary_steg = Bnew_steg[ibs, jbs]
                Bnew_steg[ibs, jbs] = change_bit (binary_steg, bp_steg, numberBin)
        channel_steg = channel_steg + 1

    R1ste = conv_channel_matrix_ascii (Rnew_steg)    
    G1ste = conv_channel_matrix_ascii (Gnew_steg)
    B1ste = conv_channel_matrix_ascii (Bnew_steg)
    newImG_steg = np.zeros(shape = imG_steg.shape)
    newImG_steg = join_channels (newImG_steg,R1ste,G1ste,B1ste) 
    return newImG_steg  



#--------------------------------------------------------------------------------
def main ( ):
    #Reads Image
    imgName= raw_input()
    img = misc.imread(imgName+'.png')

    #Reads File
    filename= raw_input()
    with io.open(filename+".txt",'r',encoding='utf8',errors="ignore") as f:
        text = f.read()
    text = text+chr(26)

    #Reads bit change position
    pos = raw_input()
    bin_pos = int(pos)
    t = text_bits(text)

    r = img[:,:,0]
    g = img[:,:,1]
    b = img[:,:,2]

    newImg = conv_matrix_int (steganography (t,r,g,b,bin_pos,img))
    misc.toimage(newImg).save(imgName+'_outfile.png')


#-------------------------------------------------------------------------------
main ( )























