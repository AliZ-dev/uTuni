
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import sys
sys.path.append("./modules")
import cv2 as cv
import tensorflow as tf
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Flatten
import glob
import os

#path = os.getcwd().replace("/script", "/data/") +  \
#                        self._color[self._channel-1] + "_" + str(int(self._rotor.get_position()/80) + 90).zfill(4) + \
#                        "_step_" + str(self.mfasession).zfill(3) + "_" + str(dt.now())[:-4].replace(":", ".") + ".tiff"

class image_scan():
    def __init__(self, extention = ".tiff", window_size = 10):
        #self._add = image_repository
        self._ext = extention
        self._width = 2456
        self._height = 2054
        self._window_size = window_size
        self._data_path = os.getcwd().replace("/script", "/data/")

    def data_set(self):
        red_add = sorted( filter( os.path.isfile, glob.glob(self._data_path + "r_*.tiff") ) )
        green_add = sorted( filter( os.path.isfile, glob.glob(self._data_path + "g_*.tiff") ) )
        blue_add = sorted( filter( os.path.isfile, glob.glob(self._data_path + "b_*.tiff") ) )

        red_set = []
        green_set = []
        blue_set = []
        for img_add in red_add:
            img = cv.imread(img_add, cv.IMREAD_GRAYSCALE)
            Hline = int(img.shape[0]/2)
            Vline = int(img.shape[1]/2)
            margin = 200
            red_set.append(np.array(img[Hline-margin:Hline+margin,Vline-2*margin:Vline], dtype=float))

        for img_add in green_add:
            img = cv.imread(img_add, cv.IMREAD_GRAYSCALE)
            green_set.append(np.array(img[Hline-margin:Hline+margin,Vline-2*margin:Vline], dtype=float))

        for img_add in blue_add:
            img = cv.imread(img_add, cv.IMREAD_GRAYSCALE)
            blue_set.append(np.array(img[Hline-margin:Hline+margin,Vline-2*margin:Vline], dtype=float))


        return np.array(red_set), np.array(green_set), np.array(blue_set)

    def mean_walk(self, input=None):
        avg_pool = AveragePooling2D(pool_size=(self._window_size,self._window_size), strides=(self._window_size,self._window_size), padding = 'valid')
        if input is None:
            r, g, b = self.data_set()
            print(r.shape)
            r = np.expand_dims(r, axis=3)
            g = np.expand_dims(g, axis=3)
            b = np.expand_dims(b, axis=3)

            r_out = avg_pool(r)
            g_out = avg_pool(g)
            b_out = avg_pool(b)

            out = [np.squeeze(r_out), np.squeeze(g_out), np.squeeze(b_out)]

        else: out = np.squeeze(avg_pool(np.expand_dims(np.expand_dims(np.array(input, dtype=float), axis=0), axis=3)))

        return out

    def uniformity(self, input=None):
        if input is None:
            [r_test, g_test, b_test] = self.mean_walk()#self.data_set()
            z = {'red':r_test[0], 'green':g_test[0], 'blue':b_test[0]}
        else: z = {'input': input}
        #print(input)
        x = np.array( range( list(z.values())[0].shape[1] ) )
        y = np.array( range( list(z.values())[0].shape[0] ) )
        X, Y = np.meshgrid(x, y)
        #pov = {1:-90, 2:45}

        fig = plt.figure(figsize=(8,4))
        i = 0
        file = open(os.path.join(self._data_path, 'x_uniformity.txt'), 'a')
        for k, Z in z.items():
            ax = fig.add_subplot(1, len(z), i+1, projection='3d')
            ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                            cmap='viridis', edgecolor='none')
            #ax.view_init(elev=20, azim=-105)#elev=20, azim=-105
            start, end = ax.get_zlim()
            ax.set_zticks(np.arange(start, end, float(abs(end-start)/6)))
            ax.set_title(k + ' light uniformity')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Intensity')

            i += 1
            file.write("\nIntensity's max of " + k + ": \n")
            file.write(str(np.max( np.max( Z ) ) ))
            file.write("\nIntensity's min of " + k + ": \n")
            file.write(str(np.min( np.min( Z, axis=0 ), axis=0 )))
            file.write("\nIntensity's mean of " + k + ": \n")
            file.write(str(np.mean( np.mean( Z ) ) ))
            file.write("\nIntensity's std of " + k + ": \n")
            file.write(str(np.std( np.std( Z, axis=0 ), axis=0 )))
        file.close()
        plt.savefig(os.path.join(self._data_path, 'x_uniformity'), format='tiff', dpi=200)
        plt.close()
        fig = plt.figure(figsize=(8,4))
        i = 0
        #file = open(os.path.join(self._data_path, 'x_uniformity.txt'), 'a')
        for k, Z in z.items():
            ax = fig.add_subplot(1, len(z), i+1, projection='3d')
            ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                            cmap='viridis', edgecolor='none')
            ax.view_init(elev=-90, azim=-90)#elev=20, azim=-90
            #start, end = ax.get_zlim()
            #ax.set_zticks(np.arange(start, end, 5))
            ax.set_title(k + ' heat map')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Intensity')

            i += 1
        plt.savefig(os.path.join(self._data_path, 'x_heatmap'), format='tiff', dpi=200)
        plt.close()
        return fig

    def polarization(self, pol_step = 5):
        
        I_mat = self.mean_walk()
        rows, cols, step = I_mat[0].shape[1], I_mat[0].shape[2], I_mat[0].shape[0]
        print(len(I_mat))
        print(I_mat[0].shape)

        I_r = I_mat[0].reshape((I_mat[0].shape[0], I_mat[0].shape[1] * I_mat[0].shape[2]))
        I_g = I_mat[1].reshape((I_mat[1].shape[0], I_mat[1].shape[1] * I_mat[1].shape[2]))
        I_b = I_mat[2].reshape((I_mat[2].shape[0], I_mat[2].shape[1] * I_mat[2].shape[2]))
        print(I_r.shape)

        y = {'red':I_r[:,200], 'green':I_g[:,200], 'blue':I_b[:,200]}
        x = np.array( range( I_r.shape[0] ) ) * pol_step

        fig0 = plt.figure(figsize=(8,4))
        i = 0
        file = open(os.path.join(self._data_path, 'x_polar_center.txt'), 'a')
        for k, Y in y.items():

            ax = fig0.add_subplot(1, 3, i+1) #, projection='3d'
            ax.plot(x,Y)
            start, end = min(Y), max(Y)
            #startx, endx = ax.get_xlim()
            print([start,end])
            ax.set_yticks(np.arange(start, end, float(abs(end-start)/6)))
            ax.set_xticks(np.arange(0, 180, 45))
            #ax.set_yticks(np.arange(startx, endx, float(abs(endx-startx)/4)))
            ax.grid(visible=True)
            ax.set_title(k + ' light polarization')
            ax.set_xlabel('angle')
            ax.set_ylabel('Intensity')
            i += 1
            file.write("\nIntensity range of " + k + ": \n")
            file.write("Min: " + str(np.min( Y )) + ", Max: " + str(np.max( Y )) )
            file.write("\nNumber of peak values in " + k + ": \n")
            file.write("Min: " + str(np.where( Y == np.min(Y) )) + ", Max: " + str(np.where(Y == np.max(Y))) )

        file.close()
        plt.savefig(os.path.join(self._data_path, 'x_polar_center'), format='tiff', dpi=200)
        plt.close()
        z = {'red':I_r, 'green':I_g, 'blue':I_b}
        x = np.array( range( I_r.shape[1] ) )
        y = np.array( range( I_r.shape[0] ) )
        X, Y = np.meshgrid(x, y)

        fig1 = plt.figure(figsize=(8,4))
        i = 0
        for k, Z in z.items():

            ax = fig1.add_subplot(1, 3, i+1, projection='3d')
            ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                            cmap='viridis', edgecolor='none')
            start, end = ax.get_zlim()
            ax.set_zticks(np.arange(start, end, float(abs(end-start)/6)))
            ax.set_title(k + ' light polarization')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Intensity')
            i += 1

        plt.savefig(os.path.join(self._data_path, 'x_polarization'), format='tiff', dpi=200)
        plt.close()
        color = {'red':0, 'green':1, 'blue':2}
        cos2 = np.zeros( (3, rows, cols) )
        PHI = np.zeros( (3, rows, cols) )
        x = np.array( range( cols ) )
        y = np.array( range( rows ) )
        X, Y = np.meshgrid(x, y)
        fig2 = plt.figure(figsize=(8,4))
        file = open(os.path.join(self._data_path, 'x_PHI.txt'), 'a')
        for c, k in color.items():
            cos2[k] = ( I_mat[k][0] - np.min(I_mat[k], axis=0) ) / ( np.max(I_mat[k], axis=0) - np.min(I_mat[k], axis=0) )
            PHI[k] = np.rad2deg( np.arccos( np.sqrt( cos2[k] ) ) )

            print("PHI's mean of " + c)
            print( np.mean( np.mean( PHI[k] ) ) )
            print("PHI's std of " + c)
            print( np.std( np.std( PHI[k], axis=0 ), axis=0 ) )
            file.write("\nIntensity range of " + c + ": \n")
            file.write("Min: " + str(np.min(np.min(np.min( I_mat[k], axis=0 )))) + ", Max: " + str(np.max(np.max(np.max( I_mat[k], axis=0 )))) )
            file.write("\nPHI's median of " + c + ": \n")
            file.write(str(np.median( PHI[k].flatten() ) ) )
            file.write("\nPHI's mean of " + c + ": \n")
            file.write(str(np.mean( np.mean( PHI[k] ) ) ))
            file.write("\nPHI's std of " + c + ": \n")
            file.write(str(np.std( np.std( PHI[k], axis=0 ), axis=0 )))

            ax = fig2.add_subplot(1, 3, k+1, projection='3d')
            ax.plot_surface(X, Y, PHI[k], rstride=1, cstride=1,
                            cmap='viridis', edgecolor='none')
            start, end = ax.get_zlim()
            ax.set_zticks(np.arange(start, end, float(abs(end-start)/6)))
            ax.set_title(c + ' polarization')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Angle (deg)')

        file.close()
        with open(os.path.join(self._data_path, 'x_I_MAT.npy'), 'wb') as f:
            np.save(f, I_mat, allow_pickle = False)
        with open(os.path.join(self._data_path, 'x_PHI.npy'), 'wb') as f:
            np.save(f, PHI, allow_pickle = False)
        print(PHI.shape)
        plt.savefig(os.path.join(self._data_path, 'x_pol_angle'), format='tiff', dpi=200)
        plt.close()
        lightRange = np.zeros( (3, rows, cols) )
        fig3 = plt.figure(figsize=(8,4))
        file = open(os.path.join(self._data_path, 'x_light_range.txt'), 'a')
        for c, k in color.items():
            lightRange[k] = ( np.max(I_mat[k], axis=0) - np.min(I_mat[k], axis=0) )
            
            ax = fig3.add_subplot(1, 3, k+1, projection='3d')
            ax.plot_surface(X, Y, lightRange[k], rstride=1, cstride=1,
                            cmap='viridis', edgecolor='none')
            start, end = ax.get_zlim()
            ax.set_zticks(np.arange(start, end, float(abs(end-start)/6)))
            ax.set_title(c + ' sinusoidal range')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')

            file.write("\nlight range of " + c + ": \n")
            file.write("Mean: " + str(np.mean( np.mean(lightRange[k]) )) + ", Median: " + str(np.median( np.median(lightRange[k]))) )

        file.close()
        plt.savefig(os.path.join(self._data_path, 'x_light_range'), format='tiff', dpi=200)
        plt.close()
        return fig1, fig2, fig3