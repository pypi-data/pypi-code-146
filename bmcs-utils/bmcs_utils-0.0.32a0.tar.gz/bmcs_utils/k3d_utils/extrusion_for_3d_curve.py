"""
This helps in getting a 3D geometry from a 2D/3D curve by providing
the section contour as an array of points and the 3D curve.
See:
https://stackoverflow.com/a/66501381/9277594
and
http://www.songho.ca/opengl/gl_cylinder.html#pipe
for reference
"""
import numpy as np
import k3d


class Extruder:
    def __init__(self, start_contour_points, path_points):
        # path_points should be numpy array with the shape (n, 2), or (n, 3)
        # start_contour_points should be numpy array with the shape (n, 2), or (n, 3)

        path_points, start_contour_points = self.adapt_dimensions(path_points, start_contour_points)

        self.start_contour_points = start_contour_points
        self.path_points = path_points

        self.generate_3d_contours()

    @staticmethod
    def adapt_dimensions(path_points, start_contour_points):
        # If path is 2D, convert it to 3D path ([[x1, y1, 0], [x2, y2, 0].. ])
        if path_points.shape[1] == 2:
            path_points = np.insert(path_points, 2, 0, axis=1)

        # If contour is 2D, convert it to 3D ([[x1, y1, 0], [x2, y2, 0].. ])
        if start_contour_points.shape[1] == 2:
            start_contour_points = np.insert(start_contour_points, 2, 0, axis=1)

        # switch columns 0 and 1
        start_contour_points[:, [0, 1]] = start_contour_points[:, [1, 0]]

        return path_points, start_contour_points

    @staticmethod
    def get_circle_points(r=10, n=100):
        return np.array([(np.cos(2 * np.pi / n * x) * r, np.sin(2 * np.pi / n * x) * r) for x in range(0, n + 1)])

    def get_3d_contours(self):
        return self.contours_3d

    def generate_3d_contours(self):
        path_points = np.copy(self.path_points)
        start_contour_points = np.copy(self.start_contour_points)

        self.transform_first_contour(path_points, start_contour_points)

        contours = [start_contour_points]
        for i in range(int(len(path_points)) - 1):
            #     print('i:i+3 = ', i, ':', str(i+3))
            # if they're almost equal, skip it because adding two contours in same position will damage the algorithm
            if np.allclose(path_points[i + 1],  path_points[i]):
                continue
            path_3p = path_points[i:i + 3]
            #     print('path_3p= ', path_3p)
            con = self._project_contour(start_contour_points, path_3p)
            # print('con:', con)
            start_contour_points = con
            contours.append(con)

        self.contours_3d = np.array(contours)
        return self.contours_3d

    @staticmethod
    def transform_first_contour(path, contour_points, adapt_dimensions=False):

        path = path.astype(np.float32)

        if adapt_dimensions:
            path, contour_points = Extruder.adapt_dimensions(path, contour_points)

        path_count = len(path)
        points_count = len(contour_points)
        matrix = Matrix4()

        if path_count > 0:
            if path_count > 1:
                matrix.look_at(path[1] - path[0])
            matrix.translate(path[0])

            # NOTE: the contour vertices are transformed here
            for i in range(points_count):
                contour_points[i] = matrix.multiply_with_vector(contour_points[i])

            return contour_points

    def _project_contour(self, Q1_contour, path_3p):
        # find direction vectors; v1 and v2
        if len(path_3p) == 2:
            Q1, Q2 = path_3p[0:2]
            Q3 = Q2 + (Q2 - Q1)
        else:
            Q1, Q2, Q3 = path_3p[0:3]  # path_3p should have 3 points, but this to make sure
        v1 = Q2 - Q1
        v2 = Q3 - Q2

        #     print('Q1_contour: ', Q1_contour)

        # normal vector of plane at Q2
        normal = v1 + v2

        # define plane equation at Q2 with normal and point
        plane = Plane(normal, Q2)

        # project each vertex of contour to the plane
        Q2_contour = []
        for i in range(len(Q1_contour)):
            line = Line(v1, Q1_contour[i])  # define line with direction and point
            intersect_point = plane.intersect(line)  # find the intersection point
            Q2_contour.append(intersect_point)

        # return the projected vertices of contour at Q2
        return np.array(Q2_contour)

    def show_in_k3d(self, scale=1):
        plot = k3d.plot(name='points')
        plt_points = k3d.points(positions=self.path_points, point_size=scale * 5)
        plt_points.color = 0xff0000
        plot += plt_points

        plt_points2 = k3d.points(positions=self.contours_3d, point_size=scale * 5)
        plot += plt_points2

        plt_points.shader = '3d'
        plot.display()

    def show_in_k3d_as_surface(self, with_ends=True):
        plot = k3d.plot(name='points')
        vertices, indices = self.get_triangulation_vertices_and_indices(with_ends=with_ends)
        mesh = k3d.mesh(vertices, indices,
                             color=0xc73737,
                             side='double')
        plot += mesh
        plot.display()

    def _get_indices(self):
        # number of contours
        n_c = self.contours_3d.shape[0]

        # number of points in each contour
        n_p = self.contours_3d.shape[1]

        mask = np.arange(n_c * n_p - n_p)
        mask = mask[n_p - 1::n_p]

        indices_1_0 = np.arange(n_c * n_p - n_p)
        indices_1_1 = np.arange(1, n_c * n_p - n_p + 1)
        indices_1_1[mask] = indices_1_1[mask] - n_p
        indices_1_2 = np.arange(n_p, n_c * n_p)
        indices_1 = np.stack((indices_1_0, indices_1_1, indices_1_2), axis=1)

        indices_2_0 = np.arange(n_p, n_c * n_p)
        indices_2_1 = np.arange(n_p + 1, n_c * n_p + 1)
        indices_2_1[mask] = indices_2_1[mask] - n_p
        indices_2_2 = np.arange(1, n_c * n_p - n_p + 1)
        indices_2_2[mask] = indices_2_2[mask] - n_p
        indices_2 = np.stack((indices_2_0, indices_2_1, indices_2_2), axis=1)

        return np.vstack((indices_1, indices_2))

    def _get_vertices(self):
        contours = self.contours_3d
        return np.reshape(contours, (int(contours.shape[0] * contours.shape[1]), 3))

    def get_triangulation_vertices_and_indices(self, with_ends=False):
        if with_ends:
            indices = self._get_indices()
            # add ends indices
            indices = np.vstack((indices, self._get_start_and_end_surfaces_indices()))
            return self._get_vertices(), indices
        else:
            return self._get_vertices(), self._get_indices()

    def _get_start_and_end_surfaces_indices(self):
        # number of points in a contour
        n_p = self.contours_3d.shape[1]
        # number of contours
        n_c = self.contours_3d.shape[0]
        # number of first/last surface indices
        n_i = n_p - 2

        start_surface_indices = self._generate_start_or_end_surface_indices(0, n_i)
        end_surface_indices = self._generate_start_or_end_surface_indices(n_p * n_c - n_p, n_i)

        return np.vstack((start_surface_indices, end_surface_indices))

    def _generate_start_or_end_surface_indices(self, start_i, n_i):
        surface_1 = np.full(n_i, start_i)
        surface_2 = np.arange(start_i + 1, start_i + 1 + n_i)
        surface_3 = np.arange(start_i + 2, start_i + 2 + n_i)
        return np.stack((surface_1, surface_2, surface_3), axis=1)


class Matrix4:
    def __init__(self):
        self.m = np.zeros(([4, 4]))

    # @staticmethod
    # def identity():
    #     matrix = Matrix4()
    #     matrix.m = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    #     return matrix

    def multiply_with_vector(self, vector):
        m = self.m
        return np.array([
            m[0, 0] * vector[0] + m[0, 1] * vector[1] + m[0, 2] * vector[2] + m[0, 3],
            m[1, 0] * vector[0] + m[1, 1] * vector[1] + m[1, 2] * vector[2] + m[1, 3],
            m[2, 0] * vector[0] + m[2, 1] * vector[1] + m[2, 2] * vector[2] + m[2, 3]])

    def normalize(self, a, axis=-1, order=2):
        l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
        l2[l2 == 0] = 1
        return (a / np.expand_dims(l2, axis))[0]

    def look_at(self, target):
        EPSILON = 0.00001
        position = np.array([self.m[0, 3], self.m[1, 3], self.m[2, 3]])
        forward = target - position
        forward = self.normalize(forward)

        # compute temporal up vector
        # if forward vector is near Y-axis, use up vector (0,0,-1) or (0,0,1)
        if abs(forward[0]) < EPSILON and abs(forward[2]) < EPSILON:
            # forward vector is pointing +Y axis
            if forward[1] > 0:
                up = np.array([0, 0, -1])
            # forward vector is pointing -Y axis
            else:
                up = np.array([0, 0, 1])
        else:
            # assume up vector is +Y axis
            up = np.array([0, 1, 0])

        # compute left vector
        left = np.cross(up, forward)
        left = self.normalize(left)

        # re-compute up vector
        up = np.cross(forward, left)

        # NOTE: overwrite rotation and scale info of the current matrix
        # this->setColumn(0, left)
        # this->setColumn(1, up)
        # this->setColumn(2, forward)

        self.m[0:3, 0] = left
        self.m[0:3, 1] = up
        self.m[0:3, 2] = forward

    def translate(self, v):
        m = np.identity(4)
        self.m[0, :] += v[0] * m[3, :]
        self.m[1, :] += v[1] * m[3, :]
        self.m[2, :] += v[2] * m[3, :]


class Line:
    def __init__(self, v, p):
        self.v = v  # /np.sqrt(sum(v*v))
        self.p = p

class Plane:
    def __init__(self, normal, point):
        self.normal = normal  # /np.sqrt(sum(normal*normal))
        self.point = point
        self.d = -np.dot(self.normal, self.point)  # -(a*x0 + b*y0 + c*z0)

    def intersect(self, line):
        # from line = p + t * v
        p = line.p  # (x0, y0, z0)
        v = line.v  # (x,  y,  z)

        # dot products
        dot1 = np.dot(self.normal, p)  # a*x0 + b*y0 + c*z0
        dot2 = np.dot(self.normal, v)  # a*x + b*y + c*z

        # if denominator=0, no intersect
        if dot2 == 0:
            print('dot2 == 0!')
            return np.array([0, 0, 0])

        # find t = -(a*x0 + b*y0 + c*z0 + d) / (a*x + b*y + c*z)
        t = -(dot1 + self.d) / dot2

        # find intersection point
        return p + (v * t)


if __name__ == '__main__':
    path = np.array([[0, 0, 0], [50, 0, 0], [100, 50, 0], [150, 50, 0], [200, 0, 0]])

    ''' Example with circle contour (cross-section) '''
    circle_points = Extruder.get_circle_points(r=25, n=100)
    contours_3d = Extruder.get_3d_contours(circle_points, path)
    # show_in_k3d(path, contours_3d)

    ''' Example with rectangular contour (cross-section) '''
    # rect_width = 250
    # rect_height = 400
    # contour = np.array([[0, rect_width / 2, rect_height / 2], [0, -rect_width / 2, rect_height / 2],
    #                     [0, -rect_width / 2, -rect_height / 2], [0, rect_width / 2, -rect_height / 2]])
    # contours_3d = get_3d_contours(contour, path_xyz=path)
