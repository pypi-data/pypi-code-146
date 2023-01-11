from numba import njit
import pygame as pg
from engine import *




###############################################################################
#
# Author:  Deepak (I can't belive I'm programming Python) Deo
# Date:    Jan 3, 2023
#
# future updates:
#
#   display lists should hold tris, not objs
#       for better optimization + variety of rendering types within
#       a single object (i.e. solid + transparent, etc)
#
#   need proper clipping. should be adding vertices to show part of the poly.
#
#   use .mtl file along with .obj so that the obj files can have color per face info
#   also, need to use 'materials' so that we can color objs on top of what the .obj file specifies.
#   right now it's just one color per object
#
#   support multiple lights, multiple light types (i.e. point), and light color
#
#   optimize:
#       use njit properly
#           https://numba.readthedocs.io/en/stable/user/performance-tips.html
#       __draw_normals method
#
#       Matrix class should have pre-multipled matrix methods: ie zxyt
#
#   make code more 'pythonic'
#
#   need simpler/cleaner way of doing imports 
#
###############################################################################
class Engine:

    VERSION                 = 1.0

    DISPLAY_LIST_WIREFRAME  = 1
    DISPLAY_LIST_SHADED     = 2



    ###############################################################################
    #
    ###############################################################################
    @staticmethod
    @njit(fastmath=True)
    def AreAllVertsVisible(list_verts: list, screen_res_half_x: float, screen_res_half_y: float):
        # NOTE: verts that are offscreen have had their vals pushed to half_x or half_y
        return not np.any((list_verts == screen_res_half_x) | (list_verts == screen_res_half_y))


    ###############################################################################
    #
    ###############################################################################
    def __init__(self, screen_res: SiVector2, bg_color: pg.Color, light: LightDirectional):

        SiLog.Message("Version", Engine.VERSION)

        # using pygame (pg) for drawing to the screen
        pg.init()
     
        self.screen_res = screen_res

        # NOTE: '//' means floor division 
        #   i.e. 5/2 = 2.5
        #        5//2 = 2
        self.screen_res_half = SiVector2(self.screen_res.x // 2, self.screen_res.y // 2)
        self.screen = pg.display.set_mode([self.screen_res.x, self.screen_res.y])

        self.bg_color = pg.Color(bg_color)

        self.light = light

        self.FPS = 60
        self.clock = pg.time.Clock()

        self.camera = Camera(SiVector3(0, 0, 0))
        self.projection = Projection(self, self.screen_res)

        # must add objects to one of these lists if you want them drawn
        self.display_list_wireframe = list()
        self.display_list_shaded = list()


    ###############################################################################
    #
    ###############################################################################
    def add_display_object(self, obj: Object, display_list_type: int):

        if display_list_type == Engine.DISPLAY_LIST_WIREFRAME:
            self.display_list_wireframe.append(obj)
        elif display_list_type == Engine.DISPLAY_LIST_SHADED:
            self.display_list_shaded.append(obj)
        else:
            SiLog.Error("unsupported display list type [" + display_list_type + "]");
    
            
    ###############################################################################
    #
    ###############################################################################
    def clear_screen(self):

        self.screen.fill(self.bg_color)


    ###############################################################################
    #
    ###############################################################################
    def update(self):
    
        # precalc camera matrix
        camera_matrix = self.camera.calc_camera_matrix()

        if len(self.display_list_wireframe) > 0:
            self.__display(camera_matrix, self.display_list_wireframe, Engine.DISPLAY_LIST_WIREFRAME)

        if len(self.display_list_shaded) > 0:
            self.__display(camera_matrix, self.display_list_shaded, Engine.DISPLAY_LIST_SHADED)


    ###############################################################################
    #
    ###############################################################################
    def __display(self, camera_matrix: Matrix, display_list: list, display_list_type: int):

        for obj in display_list:

            # move verts to world space
            #              
            # NOTE: the mat_world array of arrays looks like this for a pos 0,0,0 and rot 0,0.2,0
            #       array[
            #               [0.99980001,    0,  -0.01999867,    0]
            #               [         0,    1,            0,    0]
            #               [0.01999867,    0,   0.99980001,    0]
            #               [         0,    0,            0,    1]
            #            ]
            #
            #        but should be thought of as transposed to understand the mat mult
            #        [ 0.99980001,      0,  0.01999867,     0]
            #        [          0,      1,           0,     0]
            #        [-0.01999867,      0,  0.99980001,     0]
            #        [          0,      0,           0,     1]
            #
            #        for another example consider this:
            #
            #           vertex    = np.array([2, 0, -2, 0])
            #           world_mat = np.array([[2, 0, -2, 0],
            #                                 [0, 1,  0, 0],
            #                                 [3, 0,  5, 0],
            #                                 [0, 0, 0, 1]])
            #
            #           new_vertex = np.matmul(vertex, world_mat)
            #
            #           in a standard mult - you'd think of the vertex as a vertical col.
            #           but here it's a row - which means we need to mult by the cols of world_mat
            list_vertex = np.matmul(obj.mesh.list_vertex, obj.mat_world)

            # copy the list to keep original world vertices
            list_vertex_world = list_vertex[:]

            # move normals to world space 
            # NOTE: need normals even if not drawing normals since code
            #       is using the normal to cull any polygons that are not
            #       facing the camera. also needed for lighting
            list_normal = np.matmul(obj.mesh.list_face_normal, obj.mat_world)

            # move verts to camera space   
            list_vertex = np.matmul(list_vertex, camera_matrix)

            # move verts to unit cube via perspective projection
            list_vertex = np.matmul(list_vertex, self.projection.projection_matrix)

            # perspective divide
            #       list_vertex is n rows of [x y z w]
            #       the below line of code is just doing this:
            #       for v in list_vertex:
            #           v[0] /= v[3];       # x / w
            #           v[1] /= v[3];       # y / w
            #           v[2] /= v[3];       # z / w
            #           v[3] /= v[3];       # w / w
            list_vertex /= list_vertex[:, -1].reshape(-1, 1)

            # clip verts that are outside of unit cube
            #   the reason we set the vert to 0 is for the next matrix mult
            #   i.e. 0 for x means the matrix mult will not get any of the x component 
            #        but it will get the full y component (which is ie 800).
            #        'pushing' all those values to the borders which makes it 
            #        easier for us to check if any of the 2d polygon verts are outside of the screen
            #        so we won't need to draw them
            #   this below is just doing this:
            #
            #   for i, v in enumerate(list_vertex):
            #       if v[0] > 1.0:
            #        list_vertex[i][0] = 0.0
            #       elif v[1] > 1.0:
            #           list_vertex[i][1] = 0.0
            #       elif v[2] > 1.0:
            #           list_vertex[i][2] = 0.0
            #       elif v[0] < -1.0:
            #           list_vertex[i][0] = 0.0
            #       elif v[1] < -1.0:
            #           list_vertex[i][1] = 0.0
            #       elif v[2] < -1.0:
            #           list_vertex[i][2] = 0.0
            list_vertex[(list_vertex > 1) | (list_vertex < -1)] = 0

            # unit_cube -> screen
            list_vertex = np.matmul(list_vertex, self.projection.to_screen_matrix)

            # create a new list with just the x/y of the verts
            # since, in the end, all we are doing is drawing a 2d image...
            list_vertex = list_vertex[:, :2]
           
            #draw faces
            for face_idx, face_info in enumerate(obj.list_face_info):
                             
                # this below code is just doing this
                # color = face_info[0]
                # face = face_info[1]
                color, list_vertex_index = face_info

                # this below code is just doing this
                # list_verts = []
                # for vert_idx in list_vertex_index:
                #     list_verts.append(list_vertex[vert_idx])
                # list_polygon_vertex = []
                # list_polygon_vertex.append(list_verts)
                list_polygon_vertex = list_vertex[list_vertex_index]

                # any of the 3 vertices will do
                vertex_world = list_vertex_world[list_vertex_index][0]

                if Engine.AreAllVertsVisible(list_polygon_vertex, self.screen_res_half.x, self.screen_res_half.y):

                    # only draw the face if its normal is facing the camera!                  

                    # NOTE: normals are already normalized since we are just rotating a normalized vector
                    v1 = list_normal[face_idx]

                    # get vector from face to the camera
                    v2 = vertex_world - self.camera.pos

                    #normalize
                    v2 = v2/np.linalg.norm(v2)

                    dp = np.dot(v1,v2)
                    if dp < 0.0:

                        # now that we know tri is being drawn, calc dp for lighting
                        dp = v1[0]*self.light.direction[0] + v1[1]*self.light.direction[1] + v1[2]*self.light.direction[2]
                        dp = (1.0 - dp) * 0.5
                        face_color = self.__calc_face_color(color, dp)

                        # convert vertices from 4 components [x y z w] to 2 components [x y]   
                        v0 = [list_polygon_vertex[0][0], list_polygon_vertex[0][1]]
                        v1 = [list_polygon_vertex[1][0], list_polygon_vertex[1][1]]
                        v2 = [list_polygon_vertex[2][0], list_polygon_vertex[2][1]]

                        # NOTE: polygon draw with 0 means fill 0 otherwise it means thickness of line (int)
                        if display_list_type == Engine.DISPLAY_LIST_WIREFRAME:
                            pg.draw.line(self.screen, color, v0, v1, 2)
                            pg.draw.line(self.screen, color, v1, v2, 2)
                            pg.draw.line(self.screen, color, v2, v0, 2)
                        elif display_list_type == Engine.DISPLAY_LIST_SHADED:
                            pg.draw.polygon(self.screen, face_color, list_polygon_vertex, 0)  
                        else:
                            SiLog.Error("unsupported display list type [" + display_list_type + "]");

                    if obj.draw_normals:
                        self.__draw_normals(list_vertex_world, list_vertex_index, list_normal, face_idx)
 
                    if obj.draw_vertices:
                        for vertex in list_vertex:
                            pg.draw.circle(self.screen, pg.Color('white'), vertex, 6)



    ###############################################################################
    #    
    ###############################################################################
    def __calc_face_color(self, face_color: pg.Color, dp: float):

        col = pg.Color(face_color)

        col.r = int(col.r * dp)
        col.g = int(col.g * dp)
        col.b = int(col.b * dp)

        return col



    ###############################################################################
    #    
    ###############################################################################
    def __draw_normals(self, list_vertex_world: list, list_vertex_index: list, list_normal: list, face_idx: int):

        tx = 0.0
        ty = 0.0
        tz = 0.0
 
        for vertex in list_vertex_world[list_vertex_index]: 
            tx += vertex[0]
            ty += vertex[1]
            tz += vertex[2]

        num = list_vertex_world[list_vertex_index].shape[0]
        tx /= num
        ty /= num
        tz /= num

        pos_start = []
        pos_start.append(tx)
        pos_start.append(ty)
        pos_start.append(tz)
        pos_start.append(1.0)

        pos_end = pos_start[:]
        pos_end[0] += (list_normal[face_idx][0] * 1.0)
        pos_end[1] += (list_normal[face_idx][1] * 1.0)
        pos_end[2] += (list_normal[face_idx][2] * 1.0)
        pos_end[3] = 1.0

        pos_start = np.matmul(pos_start, self.camera.calc_camera_matrix())
        pos_start = np.matmul(pos_start, self.projection.projection_matrix)
        pos_start[0] /= pos_start[3]
        pos_start[1] /= pos_start[3]
        pos_start[2] /= pos_start[3]
        pos_start[3] /= pos_start[3]
        pos_start = np.matmul(pos_start, self.projection.to_screen_matrix)
        pos_start = pos_start[:2]

        pos_end = np.matmul(pos_end, self.camera.calc_camera_matrix())
        pos_end = np.matmul(pos_end, self.projection.projection_matrix)
        pos_end[0] /= pos_end[3]
        pos_end[1] /= pos_end[3]
        pos_end[2] /= pos_end[3]
        pos_end[3] /= pos_end[3]
        pos_end = np.matmul(pos_end, self.projection.to_screen_matrix)
        pos_end = pos_end[:2]

        pg.draw.line(self.screen, pg.Color('yellow'), pos_start, pos_end, 3)




    ###############################################################################
    #
    ###############################################################################
    def blit(self):

        pg.display.set_caption(str(self.clock.get_fps()))
        pg.display.flip()
        self.clock.tick(self.FPS)


