import numpy as np
import sys
import os
import shutil

from simassis.general import u_rotate, mases, angle, mases_to_symbols, charges
#vnbrbvdrvbdrviu

def path_restart(fpath):
    if os.path.exists(fpath):
        shutil.rmtree(fpath, ignore_errors=True)
        os.makedirs(fpath)
    else:
        os.makedirs(fpath)

def list_of_files(fpath):
    return [f for f in os.listdir(fpath) if os.path.isfile(os.path.join(fpath, f))]

def list_of_directories(fpath):
    return list(set(os.listdir(fpath))-set(list_of_files(fpath)))

def subpaths_in_folder(path):
    paths = [x[0] for x in os.walk(path)]
    pas = []
    for p in range(len(paths)):
        g = True
        for pt in range(len(paths)):
            if p is not pt:
                if paths[p] in paths[pt]:
                    g = False
        if g:
            pas.append(paths[p]+'/')
    return pas

def list_of_out_directories(fpath):
    dire = list_of_directories(fpath)
    number = [int(n[30:]) for n in dire]
    idx = np.argsort(number)
    dire = np.array(dire)[idx]
    dire = dire.tolist()
    return dire

def _parsing_poscar(lines):
        name = lines[0]
        lattice_cons = float(lines[1])
        basex = np.array([float(l)*lattice_cons for l in lines[2].split()])
        basey = np.array([float(l)*lattice_cons for l in lines[3].split()])
        basez = np.array([float(l)*lattice_cons for l in lines[4].split()])
        atoms = [int(l) for l in lines[6].split()]
        atoms_tot = sum(atoms)
        header_tot = 8
        positions = lines[header_tot:]
        positions = [p[:-1] for p in positions[:atoms_tot]]
        
        positions = np.array([p.split() for p in positions], float)
        return name, basex, basey, basez, atoms_tot, positions
    
def _rotating_positions(basex, basey, basez, positions):
    #fixing x    
    if basex[1] != 0 or basex[2] != 0:
        rotation_vecotr = np.cross([1,0,0], basex)
        rotation_angle = angle([1,0,0], basex)
        rotation_matrix = u_rotate(rotation_angle, rotation_vecotr)
        basez = np.dot(basez, rotation_matrix)
        basey = np.dot(basey, rotation_matrix)
        basex = np.dot(basex, rotation_matrix)
        for i in range(len(positions)):
            positions[i, :] = np.dot(positions[i,:], rotation_matrix)
        
    #fixing y
    if basey[2] != 0:
        rotation_vecotr = [1,0,0]
        rotation_angle = -angle([0,1,0], [0, basey[1], basey[2]])
        rotation_matrix = u_rotate(rotation_angle, rotation_vecotr)
        basez = np.dot(basez, rotation_matrix)
        basey = np.dot(basey, rotation_matrix)
        basex = np.dot(basex, rotation_matrix)
        for i in range(len(positions)):
            positions[i, :] = np.dot(positions[i,:], rotation_matrix)

    return basex, basey, basez, positions

def _positive_vectors(basex, basey, basez, positions):
    if basex[0]<0:
        basex = basex*-1
        positions[:, 0] = positions[:, 0]*-1
    if basey[1]<0:
        basey = basey*-1
        positions[:, 1] = positions[:, 1]*-1
    if basez[2]<0:
        basez = basez*-1
        positions[:, 2] = positions[:, 2]*-1
    for i in range(3):
        if np.abs(basex[i])<.00001:
            basex[i] = 0
        if np.abs(basey[i])<.00001:
            basey[i] = 0
        if np.abs(basez[i])<.00001:
            basez[i] = 0
                
    return basex, basey, basez, positions

def poscar_to(file_in, args):
    file = open(file_in)
    lines = file.readlines()
    file.close()
    
    cart_dir = lines[7][:-1]

    name, basex, basey, basez, atoms_tot, positions = _parsing_poscar(lines) 
    atoms_type = list(filter(None,lines[5][:-1].split()))
    atoms_quantity = np.array(list(filter(None,lines[6][:-1].split())), int)
    atoms_variety = len(atoms_quantity)
    if 'Direct' in cart_dir:
        base = np.array([basex, basey, basez]).T
        positions = np.dot(base, positions.T).T

    positions_splited = []
    nl = 0
    for i in range(atoms_variety):
        positions_splited.append(positions[nl:nl+atoms_quantity[i]])
        nl = nl + atoms_quantity[i]
    return configuration(name, basex, basey, basez, cart_dir, atoms_type, atoms_quantity, atoms_variety, positions_splited)

def lammps_to(filein, args):
    file = open(filein)
    lines = file.readlines()
    file.close()
    
    if 'Masses' in lines[9]:
        shift = 0
    elif 'Masses' in lines[10]:
        shift = 1
    else:
        print('something wrong with position of first few lines')
        shift = 1000000

    name = lines[0]
    atoms_quantity_total = int(lines[2].split()[0])
    atoms_variety = int(lines[3].split()[0])
    atoms_type = lines[11+shift:11+shift+atoms_variety]
    atoms_type = [float(a.split()[1]) for a in atoms_type]
    atoms_type = [mases_to_symbols[a] for a in atoms_type]
    
    basis = lines[5:8+shift]
    basis = [b.split() for b in basis]

    xl = np.asanyarray(basis[0][:2],float)
    yl = np.asanyarray(basis[1][:2],float)
    zl = np.asanyarray(basis[2][:2],float)
    if shift == 0:
        xy = 0
        xz = 0
        yz = 0
    if shift == 1:
        xy = float(basis[3][0])
        xz = float(basis[3][1])
        yz = float(basis[3][2])
    
    basex = np.array([xl[1]-xl[0], 0, 0])
    basey = np.array([xy, yl[1]-yl[0], 0])
    basez = np.array([xz, yz, zl[1]-zl[0]])
    
    positions = lines[14+shift+atoms_variety:14+shift+atoms_variety+atoms_quantity_total]
    positions = np.asanyarray([p.split()[:5] for p in positions])
    pos_idx = positions[:,0].astype(int)-1
    pos_type = positions[:,1].astype(int)-1
    positions = positions[:,2:].astype(float)
    pos_type = pos_type[pos_idx]
    positions = positions[pos_idx,:]
    
    positions_splited = []
    atoms_quantity = []
    for a in range(atoms_variety):
        positions_splited.append(positions[pos_type==a,:])
        atoms_quantity.append(np.sum(pos_type==a))
    return configuration(name, basex, basey, basez, 'Cartesian', atoms_type, atoms_quantity, atoms_variety, positions_splited)

def lammps_dump_to(filein, args):
    file = open(filein)
    lines = file.readlines()
    file.close()

    frame = args[0]
    steps = len([l for l in lines if 'ITEM: TIMESTEP' in l])
    step_len = len(lines)/steps
    if frame<0:
        frame = steps+frame
    frame_beg = int(frame*step_len + 9)
    frame_end = int((frame+1)*step_len)
        
    name = 'noname'
    atoms_quantity_total = int(lines[3].split()[0])

    basis = lines[5:8]
    basis = [b.split() for b in basis]

    xl = np.asanyarray(basis[0][:2],float)
    yl = np.asanyarray(basis[1][:2],float)
    zl = np.asanyarray(basis[2][:2],float)

    basex = np.array([xl[1]-xl[0], 0, 0])
    basey = np.array([0, yl[1]-yl[0], 0])
    basez = np.array([0, 0, zl[1]-zl[0]])

    data = lines[frame_beg:frame_end]
    data = np.array([d.split() for d in data], dtype=float)
    atom_types = np.array(data[:,0]-1, dtype=int)
    atom_masses = data[:,1]
    atom_masses_unique = np.unique(atom_masses)
    atoms_variety = len(atom_masses_unique)
    atoms_type = [mases_to_symbols[a] for a in atom_masses_unique]

    positions = data[:,2:]
    positions_splited = []
    atoms_quantity = []
    for a in range(atoms_variety):
        positions_splited.append(positions[atom_types==a,:])
        atoms_quantity.append(np.sum(atom_types==a))
    return configuration(name, basex, basey, basez, 'Cartesian', atoms_type, atoms_quantity, atoms_variety, positions_splited)

def to_poscar(
        name,
        basex, basey, basez,
        cart_dir,
        atoms_type, atoms_quantity, atoms_variety,
        positions_splited,
        fileout,
        ):    
    poscar = [name]
    poscar.append('1.0\n')
    poscar.append('\t'+str(basex[0])+'\t'+str(basex[1]) +'\t' + str(basex[2]) + '\n')
    poscar.append('\t'+str(basey[0])+'\t'+str(basey[1]) +'\t' + str(basey[2]) + '\n')
    poscar.append('\t'+str(basez[0])+'\t'+str(basez[1]) +'\t' + str(basez[2]) + '\n')
    poscar.append('\t'+'\t'.join(atoms_type) + '\n')
    poscar.append('\t'+'\t'.join([str(a) for a in atoms_quantity]) + '\n')
    poscar.append(' '+cart_dir+'\n')
    for positions in positions_splited:
        if len(positions.shape)>1:
            for p in positions:
                poscar.append(str(p[0]) + '\t' + str(p[1]) + '\t' + str(p[2]) + '\t' + '\n')
        else:
            poscar.append(str(positions[0]) + '\t' + str(positions[1]) + '\t' + str(positions[2]) + '\t' + '\n')
    poscar = "".join(poscar)
    
    file = open(fileout, 'w')
    file.write(poscar)
    file.close()
    
def to_lammps(
        name,
        basex, basey, basez,
        cart_dir,
        atoms_type, atoms_quantity, atoms_variety,
        positions_splited,
        fileout,
        args,
        ):

    #rotating bases and positions
    for i in range(len(positions_splited)):
        basex_, basey_, basez_, positions_splited[i] = _rotating_positions(
                basex, basey, basez,
                positions_splited[i],
                )
    basex, basey, basez = basex_, basey_, basez_
    
    for i in range(len(positions_splited)):
        basex_, basey_, basez_, positions_splited[i] = _positive_vectors(
                basex, basey, basez,
                positions_splited[i],)
    basex, basey, basez = basex_, basey_, basez_
    
    if cart_dir=='Cartesian' or cart_dir=='cartesian':
        pass
    if cart_dir=='Direct' or cart_dir=='direct':
        for p in range(len(positions_splited)):
            for a in range(positions_splited[p].shape[0]):
                x_ = positions_splited[p][a][0]
                y_ = positions_splited[p][a][1]
                z_ = positions_splited[p][a][2]
                
                x = x_*basex[0] + y_*basey[0] + z_*basez[0]
                y = x_*basex[1] + y_*basey[1] + z_*basez[1]
                z = x_*basex[2] + y_*basey[2] + z_*basez[2]
                
                positions_splited[p][a][0]  = x
                positions_splited[p][a][1]  = y
                positions_splited[p][a][2]  = z

    text = [name]
    text.append('\n')
    text.append(str(np.sum(atoms_quantity))+' atoms\n')
    text.append(str(atoms_variety)+' atom types\n')
    text.append('\n')
    text.append(
            str(0) + ' ' +
            str(basex[0]) + ' ' +
            'xlo xhi\n'
            )
    text.append(
            str(0) + ' ' +
            str(basey[1]) + ' ' +
            'ylo yhi\n'
            )
    text.append(
            str(0) + ' ' +
            str(basez[2]) + ' ' +
            'zlo zhi\n'
            )
    if 'triclinic' in args:
        text.append(
                str(basey[0]) + ' ' +
                str(basez[0]) + ' ' +
                str(basez[1]) + ' ' +
                'xy xz yz\n'
                )
    text.append('\n')
    text.append('Masses\n')
    text.append('\n')
    for a in range(len(atoms_type)):
        text.append(str(a+1) + ' ' + str(mases[atoms_type[a]]) + '\n')
    text.append('\n')
    text.append('Atoms\n')
    text.append('\n')

    if 'charge' in args:
        n = 1
        for at in range(len(atoms_type)):
            for a in positions_splited[at]:
                text.append(
                        '   ' +
                        str(n) + ' ' +
                        str(at+1) + ' ' +
                        str(charges[atoms_type[at]]) + ' ' +
                        str(a[0]) + ' ' + 
                        str(a[1]) + ' ' + 
                        str(a[2]) + ' ' + 
                        '\n'
                        )
                n += 1
    else:
        n = 1
        for at in range(len(atoms_type)):
            for a in positions_splited[at]:
                text.append(
                        '   ' +
                        str(n) + ' ' +
                        str(at+1) + ' ' +
                        str(a[0]) + ' ' + 
                        str(a[1]) + ' ' + 
                        str(a[2]) + ' ' + 
                        '\n'
                        )
                n += 1

    text = "".join(text)
    file = open(fileout, 'w')
    file.write(text)
    file.close()

class configuration:
    def __init__(
            self,
            name, 
            basex, basey, basez, 
            cart_dir, 
            atoms_type, atoms_quantity, atoms_variety,
            positions_splited,
            ):
        self.name = name
        self.basex = basex
        self.basey = basey
        self.basez = basez
        self.cart_dir = cart_dir
        self.atoms_type = atoms_type
        self.atoms_quantity = atoms_quantity
        self.atoms_variety = atoms_variety
        self.positions_splited = positions_splited

    def write(self, file_format, fileout, args=[]):
        if file_format=='vasp':
            to_poscar(
                        self.name,
                        self.basex, self.basey, self.basez,
                        self.cart_dir,
                        self.atoms_type, self.atoms_quantity, self.atoms_variety,
                        self.positions_splited,
                        fileout,
                        args,
                    )
        if file_format=='lammps':
            to_lammps(
                        self.name,
                        self.basex, self.basey, self.basez,
                        self.cart_dir,
                        self.atoms_type, self.atoms_quantity, self.atoms_variety,
                        self.positions_splited,
                        fileout,
                        args,
                    )
        if file_format=='lammps-dump':
            to_lammps_dump(
                        self.name,
                        self.basex, self.basey, self.basez,
                        self.cart_dir,
                        self.atoms_type, self.atoms_quantity, self.atoms_variety,
                        self.positions_splited,
                        fileout,
                        args,
                    )

def read_configuration(fname, file_format, args=[]):
    if file_format=='vasp':
        return poscar_to(fname, args)
    elif file_format=='lammps':
        return lammps_to(fname, args)
    elif file_format=='lammps-dump':
        return lammps_dump_to(fname, args)
    else:
        print('wrong file format')
        return 0

def reading_elfacar_file(fname):
    file = open(fname)
    lines = file.readlines()
    file.close()

    basis = lines[2:5]
    basis = np.array([b.split() for b in basis], dtype=float)
    atoms = np.array(lines[6].split(), dtype=int)
    n_na = atoms[0]
    n_bi = atoms[1]
    n_o = atoms[3]
    n_all = np.sum(atoms)
    positions = lines[8:8+n_all]
    positions = np.array([p.split() for p in positions], dtype=float)
    positions_bi = positions[n_na:n_na+n_bi]
    positions_ox = positions[-n_o:]
    
    binning = np.array(lines[8+n_all+1].split(), dtype=int)
    n_lines = int(np.ceil(binning[0]*binning[1]*binning[2]/10))
    data = lines[8+n_all+2:]
    data = [d.split() for d in data]
    data = np.array([item for sublist in data for item in sublist], dtype=float)
    
    M = np.zeros((binning))
    czik = 0
    for z in range(binning[2]):
        for y in range(binning[1]):
            for x in range(binning[0]):
                M[x,y,z] = data[czik]
                czik = czik + 1
    return positions_bi, positions_ox, basis, M, binning, n_lines

def parsing_elfcar(position_bi, positions_ox, basis, M, binning, dcut):
    positions_bi_binning = np.floor(position_bi*binning)/binning
    positions_bi_shifted = np.mod(position_bi-positions_bi_binning+.5, 1)
    positions_ox_shifted = np.mod(positions_ox-positions_bi_binning+.5, 1)
    
    positions_ox_scaled = np.zeros_like(positions_ox_shifted)
    positions_ox_scaled[:,0] = positions_ox_shifted[:,0]*basis[0,0]
    positions_ox_scaled[:,1] = positions_ox_shifted[:,1]*basis[1,1]
    positions_ox_scaled[:,2] = positions_ox_shifted[:,2]*basis[2,2]
    
    positions_bi_scaled = np.zeros_like(positions_bi_shifted)
    positions_bi_scaled[0] = positions_bi_shifted[0]*basis[0,0]
    positions_bi_scaled[1] = positions_bi_shifted[1]*basis[1,1]
    positions_bi_scaled[2] = positions_bi_shifted[2]*basis[2,2]
    
    d = np.sum((positions_ox_scaled-positions_bi_scaled)**2, 1)**.5
    idx = d < 4
    positions_ox_shifted_near_bi = positions_ox_shifted[idx,:]
    
    #shifting volumetric data
    positions_bi_binning = np.array(positions_bi_binning*binning, dtype=int)
    dx = (int(binning[0]/2) - positions_bi_binning[0]) 
    dy = (int(binning[1]/2) - positions_bi_binning[1])
    dz = (int(binning[2]/2) - positions_bi_binning[2])
    
    if dx**2>0:
        new_M = np.zeros_like(M)
        new_M[dx:,:,:] = M[:-dx,:,:]
        new_M[:dx,:,:] = M[-dx:,:,:]
    
    if dy**2>0:
        M = new_M
        new_M = np.zeros_like(M)
        new_M[:,dy:,:] = M[:,:-dy,:]
        new_M[:,:dy,:] = M[:,-dy:,:]
    
    if dz**2>0:
        M = new_M
        new_M = np.zeros_like(M)
        new_M[:,:,dz:] = M[:,:,:-dz]
        new_M[:,:,:dz] = M[:,:,-dz:]

    position = []
    weight = []
    for z in range(binning[2]):
        for y in range(binning[1]):
            for x in range(binning[0]):
                r = (
                                (x - binning[0]/2)**2 + 
                                (y - binning[1]/2)**2 + 
                                (z - binning[2]/2)**2
                                )**.5
                if r > dcut:
                    new_M[x,y,z] = 0
                if r <= 2:
                    new_M[x,y,z] = new_M[x,y,z]*r/3
                position.append([x,y,z])
                weight.append(new_M[x,y,z])
    position = np.array(position)
    weight = np.array(weight)**20
    
    lp = np.sum(position.T*weight, 1)/np.sum(weight)
    lp = [
          lp[0]/binning[0],
          lp[1]/binning[1],
          lp[2]/binning[2],
          ]
    shifting_factor = (1/binning)/2
    positions_ox_shifted_near_bi = positions_ox_shifted_near_bi+shifting_factor
    positions_bi_shifted = positions_bi_shifted+shifting_factor
    return positions_ox_shifted_near_bi, positions_bi_shifted, new_M, lp

def read_charge(fpath):
    file = open(fpath)
    lines = file.readlines()
    file.close()
    
    brak = [i for i in range(len(lines)) if '---' in lines[i]]
    lines = lines[brak[0]+1:brak[1]]
    return np.array([l.split()[4] for l in lines], dtype=float)