from Retro3D import *


###############################################################################
#
###############################################################################
class ObjFile:

    TAG_VERTEX = 'v '
    TAG_FACE = 'f '
    TAG_NORMAL = 'vn '

    ###############################################################################
    #
    # loads .obj file created by Wavefront Technologies
    # see https://en.wikipedia.org/wiki/Wavefront_.obj_file
    #
    ###############################################################################
    def __init__(self, fname):

        self.list_vertex = []
        self.list_normal = []
        self.list_face = []
        self.list_face_normal = []

        with open(fname) as f:
            for line in f:

                if line.startswith(ObjFile.TAG_VERTEX):

                    # getting 'v  -3.1215 13.8429 12.0213'
                    # could split it with something like this
                    #   self.list_vertex.append([float(i) for i in line.split()[1:]] + [1])
                    #   err.. no thanks... 

                    list_vals = line.split()
                    list_vals.pop(0)

                    list_float = []
                    for val in list_vals:
                        list_float.append(float(val))
                    list_float.append(1)

                    self.list_vertex.append(list_float)
                        
                elif line.startswith(ObjFile.TAG_NORMAL):     

                    # getting 'vn 0.0000 1.0000 0.0000'

                    list_vals = line.split()
                    list_vals.pop(0)

                    list_float = []
                    for val in list_vals:
                        list_float.append(float(val))
                    list_float.append(1)

                    self.list_normal.append(list_float)

                elif line.startswith(ObjFile.TAG_FACE):     

                    # getting 'f 1/1/1 2/2/1 3/3/1 4/4/1 5/5/1 6/6/1'
                    #   vertex_index/texture_index/normal_index
                    #   so 2/2/1 means
                    #      vertex 2 
                    #      texture index (which we are ignoring)
                    #      normal_index into our list_normal
                    list_vals = line.split()
                    list_vals.pop(0)

                    list_int = []
                    for val in list_vals:
                        # at this point val has something like 1/1/1
                        list_sub = val.split('/')
                
                        if len(list_sub) != 3:
                            SiLog.Error("was expecting exactly 3 elements. got", len(list_sub))

                        # -1 to make index 0 based (into vertices list)
                        list_int.append(int(list_sub[0]) - 1)

                        #NOTE: we are just overlaying face_normal_idx on the assumption that this index stays the same over this face...
                        face_normal_idx = int(list_sub[2]) - 1

                    self.list_face.append(list_int)
                    self.list_face_normal.append(self.list_normal[face_normal_idx])
 
  
   
        
