import bmcs_utils.api as bu
import k3d

class K3DUtils:

    @staticmethod
    def add_circle(k3d_plot, path, r, wireframe=False):
        n = 100
        #   path = np.array([[-4000, 0, -4000], [4000, 0, -4000]])
        first_contour = bu.Extruder.get_circle_points(r=r, n=n)[int(n / 2):, :]

        extruder = bu.Extruder(first_contour, path)
        vertices, indices = extruder.get_triangulation_vertices_and_indices(with_ends=False)

        # extruder.show_in_k3d_as_surface(with_ends=False)

        mesh = k3d.mesh(vertices,
                        indices,
                        color=0xde2121,
                        opacity=0.2,
                        side='double')
        if wireframe:
            wf = k3d.lines(vertices,
                           indices,
                           width=35,
                           shader='mesh',
                           color=0xde2121)
            k3d_plot += wf
        k3d_plot += mesh

    @staticmethod
    def add_ref_plane(k3d_plot):
        z = -6000
        size = 30000
        ref_plane = k3d.mesh([[size, size, z], [-size, size, z], [-size, -size, z], [size, -size, z]],
                             [[0, 1, 2], [2, 3, 0]],
                             side='double',
                             color=0xe6e6e6)
        k3d_plot += ref_plane
