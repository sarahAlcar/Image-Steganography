import binascii
import io
from scipy import misc
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
#--------------------------------------------------------------------------------
# Digital Image Steganography 
# evd_pxl.py is responsable for showing image bit pattern in raw RGB colors 
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
# Show modifyed pixel patterns in images 
def evidence_mod_pixels (img_evd, r_ev,g_ev,b_ev,bin_pos_ev):
    index = 7 - bin_pos_ev
    evid_img = np.zeros(shape = img_evd.shape)
    R_ev = conv_channel_matrix_binary (r_ev)
    G_ev = conv_channel_matrix_binary (g_ev)
    B_ev = conv_channel_matrix_binary (b_ev)
    newR_ev = np.zeros(shape = R_ev.shape)
    newG_ev = np.zeros(shape = G_ev.shape)
    newB_ev = np.zeros(shape = B_ev.shape)
    for i in range(R_ev.shape[0]):
        for j in range(R_ev.shape[1]):
            numberR_ev =  R_ev[i,j]
            numberG_ev =  G_ev[i,j]
            numberB_ev =  B_ev[i,j]
            nr_ev = numberR_ev[index]
            ng_ev = numberG_ev[index]
            nb_ev = numberB_ev[index]
            if( nr_ev == '1'):
                newR_ev [i,j] = 255
            else:
                newR_ev [i,j] = 0
            if( ng_ev == '1'):
                newG_ev [i,j] = 255
            else:
                newG_ev [i,j] = 0
            if( nb_ev == '1'):
                newB_ev [i,j] = 255
            else:
                newB_ev [i,j] = 0
    
    newImg_ev = join_channels (evid_img, newR_ev,newG_ev,newB_ev)
    return newImg_ev
#--------------------------------------------------------------------------------
def main ( ):
    #Reads Image
    imgName= raw_input()
    img = misc.imread(imgName+'.png')

    #Reads bit change position
    pos = raw_input()
    bin_pos = int(pos)

    r = img[:,:,0]
    g = img[:,:,1]
    b = img[:,:,2]


    channelEvidence = evidence_mod_pixels (img, r,g,b,bin_pos)
    rin = channelEvidence[:,:,0]
    gin = channelEvidence[:,:,1]
    bbin = channelEvidence[:,:,2]


    evd = join_channels (img,rin,gin,bbin)
    misc.toimage(evd).save(imgName+'_pixel_distribution.png')


     

#-------------------------------------------------------------------------------
main ( )























