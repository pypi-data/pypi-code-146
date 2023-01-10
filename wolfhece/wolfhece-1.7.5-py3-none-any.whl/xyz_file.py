# Fichier xyz
import numpy as np
import matplotlib.pyplot as plt
from os.path import normpath,exists,join,basename
from os import listdir,scandir

from .PyTranslate import _

class XYZFile:
    """ Classe pour la gestion des fichiers xyz """
    nblines:int
    x:np.array
    y:np.array
    z:np.array
    filename:str

    def __init__(self, fname,toread=True):
        """ Initialisation du nom du fichier """
        self.filename = fname
        self.nblines=0
        
        self.x = None
        self.y = None
        self.z = None
        self.xyz = None
        
        if toread:
            self.read_from_file()

    def test_bounds(self,bounds):
        
        if bounds is None:
            return True
        
        x1=bounds[0][0]
        x2=bounds[0][1]
        y1=bounds[1][0]
        y2=bounds[1][1]
        
        mybounds = self.get_extent()

        test = not(x2 < mybounds[0][0] or x1 > mybounds[0][1] or y2 < mybounds[1][0] or y1 > mybounds[1][1])
    
        return test

    def read_from_file(self):
        """ Lecture d'un fichier xyz et remplissage de l'objet """
        
        self.xyz = np.genfromtxt(self.filename, delimiter=',',dtype=np.float32)
        self.x = self.xyz[:,0]
        self.y = self.xyz[:,1]
        self.z = self.xyz[:,2]
        self.nblines = len(self.xyz)        
        
        # with open(self.filename, 'r') as f:
        #     self.nblines = sum(1 for line in f)
        #     self.x = np.zeros(self.nblines)
        #     self.y = np.zeros(self.nblines)
        #     self.z = np.zeros(self.nblines)
        #     f.seek(0)
        #     self.nblines = 0
        #     for line in f:
        #         tmp = line.split()
        #         if tmp:
        #             if is_float(tmp[0]):
        #                 self.x[self.nblines] = float(tmp[0])
        #                 self.y[self.nblines] = float(tmp[1])
        #                 self.z[self.nblines] = float(tmp[2])
        #                 self.nblines += 1

    def fill_from_wolf_array(self, myarray,nullvalue=0.):
        """ Création d'un fichier xyz depuis les données d'un WOLF array """
        self.nblines = myarray.nbx * myarray.nby
        self.x = np.zeros(self.nblines)
        self.y = np.zeros(self.nblines)
        self.z = np.zeros(self.nblines)
        self.nblines = 0
        for cury in range(myarray.nby):
            y = cury * myarray.dy + 0.5 * myarray.dy + myarray.origy + myarray.transly
            for curx in range(myarray.nbx):
                z = myarray.array[curx, cury]
                if z != nullvalue:
                    x = curx * myarray.dx + 0.5 * myarray.dx + myarray.origx + myarray.translx
                    self.x[self.nblines] = x
                    self.y[self.nblines] = y
                    self.z[self.nblines] = z
                    self.nblines += 1

    def write_to_file(self):
        """ Ecriture des informations dans un fichier """
        with open(self.filename, 'w') as f:
            for i in range(self.nblines):
                f.write('{:.3f},{:.3f},{:.3f}\n'.format(self.x[i], self.y[i], self.z[i]))

    def get_extent(self):
        """ Retourne les limites du rectangle qui encadre le nuage de points """
        xlim = [np.min(self.x), np.max(self.x)]
        ylim = [np.min(self.y), np.max(self.y)]
        return (xlim, ylim)

    def merge(self, xyz_list):
        """ Merge des fichiers xyz en 1 seul """
        for cur_xyz in xyz_list:
            self.nblines += cur_xyz.nblines
            
        newxyz = np.concatenate([cur.xyz for cur in xyz_list])

        if self.xyz is not None:
            self.xyz = np.concatenate([self.xyz,newxyz])
        else:
            self.xyz = newxyz

        self.x = self.xyz[:,0]
        self.y = self.xyz[:,1]
        self.z = self.xyz[:,2]

    def plot(self):
        """ Représentation graphique des points """
        plt.scatter(self.x, self.y, c=self.z, marker='.', cmap='viridis', edgecolors='none')
        plt.xlabel('x [m]')
        plt.ylabel('y [m]')
        plt.colorbar()
        plt.axis('equal')
        plt.savefig('figure.png',dpi=300)
        plt.ion()
        plt.show()
        plt.pause(0.1)

    def find_points(self,bounds):
        
        if bounds is None:
            return self.xyz
        
        xb=bounds[0]
        yb=bounds[1]
        # Get arrays which indicate invalid X, Y, or Z values.
        X_valid = (xb[0] <= self.x) & (xb[1] > self.x)
        Y_valid = (yb[0] <= self.y) & (yb[1] > self.y)
        good_indices = np.where(X_valid & Y_valid)[0]          
        return self.xyz[good_indices]

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def xyz_scandir(mydir,bounds):
    
    first=[]
    for curfile in listdir(mydir):
        if curfile.endswith('.xyz'):
            mydata = XYZFile(join(mydir,curfile))
            if mydata.test_bounds(bounds):
                print(curfile)
                first.append(mydata.find_points(bounds))

    for entry in scandir(mydir):
        if entry.is_dir():
            locf=xyz_scandir(entry,bounds)
            if len(locf)>0:
                first.append(locf)

    retfirst=[]

    if len(first)>0 :
        retfirst=np.concatenate(first)

    return retfirst
