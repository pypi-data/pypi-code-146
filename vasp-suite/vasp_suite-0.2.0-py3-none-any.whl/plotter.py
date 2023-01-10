# A module for plotting the density of states and projected density of states for a given material using the DOSCAR file from vasp
# Imports
"""
A module for plotting the density of states and projected density of states for a given material using the DOSCAR file from vasp
"""
import matplotlib.pyplot as plt
import numpy as np

# Functions
def plot_dos(dos_type, orbitals):
    """
    Plots the density of states for a given material
    
    Parameters
    ----------
    dos_type : str  
    orbitals : str

    Returns
    -------
    Plot of density of states
    """
    
    DOSCAR = []
    with open('DOSCAR','r') as f:
        for lines in f:
            stripped_lines = lines.strip()
            split_lines = stripped_lines.split()
            DOSCAR.append(split_lines)
    
    len_dos = []
    for i in range(len(DOSCAR)):
        if DOSCAR[5][0] in DOSCAR[i]:
            len_dos.append(i)

    
    fig,ax = plt.subplots()

    if dos_type == 'total':
        # TOTAL DOS
        dos_data = np.float_(DOSCAR[len_dos[0]+1:len_dos[1]])
        energy = dos_data[:,0]
        dos = dos_data[:,1]
        ax.plot(energy,dos,'r-')

    if dos_type == 'orbital':
        del len_dos[0]

        # PLOT d orbitals
        if orbitals == 'd': 
            dos_data = np.float_(DOSCAR[len_dos[1]+1:len_dos[2]]) #Finds location of the selected atom - needs extra code to do the location (use POSCAR for atoms)
            energy = dos_data[:,0]
            dos = dos_data[:,6]
            ax.plot(energy,dos,'r-',label='dyz')
            dos = dos_data[:,8]
            ax.plot(energy,dos,'b-',label=f'dxz')
            dos = dos_data[:,5]
            ax.plot(energy,dos,'g-',label='dxy')
            dos = dos_data[:,4]
            ax.plot(energy,dos,'c-',label='$dx^{2}-y^{2}$')
            dos = dos_data[:,7]
            ax.plot(energy,dos,'m-',label=f'$dz^2$ ')   

        #PLOT f orbitals
        if orbitals == 'f':
            dos_data = np.float_(DOSCAR[len_dos[1]+1:len_dos[2]]) #Finds location of the selected atom - needs extra code to do the location (use POSCAR for atoms)
            energy = dos_data[:,0]
            dos = dos_data[:,9]
            ax.plot(energy,dos,'r-',label='f1')
            dos = dos_data[:,10]
            ax.plot(energy,dos,'b-',label='f2')
            dos = dos_data[:11]
            ax.plot(energy,dos,'g-',label='f3')
            dos = dos_data[:,12]
            ax.plot(energy,dos,'c-',label='f4')
            dos = dos_data[:,13]
            ax.plot(energy,dos,'m-',label='f5')
            dos = dos_data[:,14]
            ax.plot(energy,dos,'m-',label='f6')
            dos = dos_data[:,15]
            ax.plot(energy,dos,'m-',label='f7')
    

    ax.set_xlabel('Energy/ eV')
    ax.set_ylabel('Density of states')
    ax.grid(color = 'grey', linestyle = '--')
    ax.legend()
    fig.tight_layout()
    #plt.show()
    plt.savefig('DOS.png')
