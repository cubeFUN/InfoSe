# ---------------------------------------------------------------
# SNIPER: Efficient Multi-scale Training
# Licensed under The Apache-2.0 License [see LICENSE for details]
# by Mahyar Najibi
# ---------------------------------------------------------------
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random
import numpy as np
import os

def transform_im(im, pixel_means):
    im = im.copy()
    # put channel back
    im = im.transpose((1, 2, 0))
    im += pixel_means
    return im.astype(np.uint8)


def visualize_dets(im, dets, scale, pixel_means, class_names, threshold=0.5, save_path='debug.png',
                   transform=True, addtxtpath=None, dpi=80):
    #issave = False

    if transform:
        im = transform_im(im, np.array(pixel_means)[[2, 1, 0]])
    #print('>>>>>>>> save_path {}'.format(save_path))
    # Create a canvas the same size of the image
    height, width, _ = im.shape
    out_size = width/float(dpi), height/float(dpi)
    #fig = plt.figure(figsize=out_size)
    #ax = fig.add_axes([0, 0, 1, 1])
    #ax.axis('off')

    # Display the image
    #ax.imshow(im, interpolation='nearest')
    #print('>>>>>>>> addtxtpath {}'.format(addtxtpath))

    #print('>>>>>>> dets size {} class_names {}'.format(len(dets), class_names))
    
    # Display Detections
    # yujie and j < len(dets)
    #threshold = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    #print('>>>> dets {}'.format(dets))
    fobj = open(save_path, 'a')
    for j, name in enumerate(class_names):
        #if j >= len(dets): continue
        #if name == '__background__': continue
        if not j == 1: continue
        
        #color = (random.random(), random.random(), random.random())
        #color = [(0.5, 0.5, 0.5), (0.3, 0.5, 0.5), (0.5, 0.8, 0.5), (0.5, 0.5, 0.8), (0.5, 0.5, 0.3), (0.3, 0.5, 0.8), (0.8, 0.5, 0.3), (0.5, 0.2, 0.5)]
        for det in dets[j]:
            bbox = det[:4] # * scale
            score = det[-1]
            #print('>>>>>   score {}'.format(score))
            if score < threshold:
                continue
            #issave = True
            # add person box annotation
            
            fobj.write(str(int(bbox[0])) + ' ' + str(int(bbox[1])) + ' ' + str(int(bbox[2])) + ' ' + str(int(bbox[3])) + ' ' + str(0) + ' person\n')

            '''
            rect = plt.Rectangle((bbox[0], bbox[1]),
                                 bbox[2] - bbox[0],
                                 bbox[3] - bbox[1], fill=False,
                                 edgecolor=color, linewidth=3.5)
            ax.add_patch(rect)
            ax.text(bbox[0], bbox[1] - 2 if bbox[1]-2 > 15 else bbox[1]+15, '{:s} {:.1f}'.format(name, score),
                    bbox=dict(facecolor=color, alpha=0.5), fontsize=10, color='white')
            '''
    
    fobj.close()

    #ax.set(xlim=[0, width], ylim=[height, 0], aspect=1)
    #if issave:
    #fig.savefig(save_path, dpi=dpi, transparent=True)
    #plt.cla()
    #plt.clf()
    #plt.close()


def vis_polys(polys, im_path, crop, scale):
    import scipy.misc as misc
    im = misc.imread(im_path)
    im = im[:, ::-1, :]
    for obj in range(len(polys)):
        plt.imshow(im)
        n_seg = len(polys[obj])
        for j in range(n_seg):
            cur_len = len(polys[obj][j])
            for k in range(cur_len/2):
                point = plt.Circle((polys[obj][j][2*k], polys[obj][j][2*k+1]), radius=1, color='red')
                plt.gca().add_patch(point)
        num = np.random.randint(0,100000)
        plt.savefig('debug/visualization/debug_{}_{}.png'.format(num, obj))
        plt.clf()
        plt.cla()
        plt.close()
        imc = im[int(crop[1]):int(crop[3]), int(crop[0]):int(crop[2])]
        imc2 = misc.imresize(imc, scale)
        plt.imshow(imc2)
        h,w,_ = np.shape(imc2)
        n_seg = len(polys[obj])
        for j in range(n_seg):
            cur_len = len(polys[obj][j])
            for k in range(cur_len/2):
                x1 = (polys[obj][j][2*k]-crop[0])*scale
                y1 = scale*(polys[obj][j][2*k+1]-crop[1])
                x1 = min(max(0, x1), w)
                y1 = min(max(0, y1), h)
                point = plt.Circle((x1, y1), radius=1, color='red')
                plt.gca().add_patch(point)

        plt.savefig('debug/visualization/debug_{}_{}_c.png'.format(num, obj))
        plt.clf()
        plt.cla()
        plt.close()
