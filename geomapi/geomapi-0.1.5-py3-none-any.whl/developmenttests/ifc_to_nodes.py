import multiprocessing
import ifcopenshell
import ifcopenshell.geom
import os.path
import open3d as o3d
import numpy as np

if __name__ == '__main__':

    path= os.path.join(os.getcwd(),"tests",'Samples11')#"D:\\Data\\2018-06 Werfopvolging Academiestraat Gent" 
    ifcPath= os.path.join(path,'ifc_parking.ifc' )    
    print(path)
    try:
        ifc_file = ifcopenshell.open(ifcPath)
        meshes=[]
    except:
        print(ifcopenshell.get_log())
    else:
        settings = ifcopenshell.geom.settings()
        iterator = ifcopenshell.geom.iterator(settings, ifc_file, multiprocessing.cpu_count())
        if iterator.initialize():
            while True:
                shape = iterator.get()
                element = ifc_file.by_guid(shape.guid)
                print(element.id)
                faces = shape.geometry.faces # Indices of vertices per triangle face e.g. [f1v1, f1v2, f1v3, f2v1, f2v2, f2v3, ...]
                verts = shape.geometry.verts # X Y Z of vertices in flattened list e.g. [v1x, v1y, v1z, v2x, v2y, v2z, ...]
                materials = shape.geometry.materials # Material names and colour style information that are relevant to this shape
                material_ids = shape.geometry.material_ids # Indices of material applied per triangle face e.g. [f1m, f2m, ...]

                # Since the lists are flattened, you may prefer to group them per face like so depending on your geometry kernel
                grouped_verts = [[verts[i], verts[i + 1], verts[i + 2]] for i in range(0, len(verts), 3)]
                grouped_faces = [[faces[i], faces[i + 1], faces[i + 2]] for i in range(0, len(faces), 3)]
                
                #THIS IS MINE
                #Convert grouped vertices/faces to Open3D objects 
                o3dVertices = o3d.utility.Vector3dVector(np.asarray(grouped_verts))
                o3dTriangles = o3d.utility.Vector3iVector(np.asarray(grouped_faces))

                # Create the Open3D mesh object
                mesh=o3d.geometry.TriangleMesh(o3dVertices,o3dTriangles)
                if mesh:
                    meshes.append(mesh)
                
                if not iterator.next():
                    break
    print(len(meshes))
            