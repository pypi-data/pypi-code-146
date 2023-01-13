from .toolbar import Toolbar
from .widgets import HBar

import ipywidgets as ipw
import numpy as np
import pythreejs as p3


class Figure(HBar):

    def __init__(self, figsize=(6., 4.)) -> None:

        self.axes = []
        self._dpi = 96
        self.width = figsize[0] * self._dpi
        self.height = figsize[1] * self._dpi

        # # Make background to enable box zoom
        # self._background_geometry = p3.BoxGeometry(width=200,
        #                                            height=200,
        #                                            widthSegments=1,
        #                                            heightSegments=1)
        # self._background_material = p3.MeshBasicMaterial(
        #     color=self.background_color, side='DoubleSide')
        # self._background_mesh = p3.Mesh(geometry=self._background_geometry,
        #                                 material=self._background_material,
        #                                 position=(0, 0, -100))

        # self._zoom_down_picker = p3.Picker(controlling=self._background_mesh,
        #                                    event='mousedown')
        # self._zoom_up_picker = p3.Picker(controlling=self._background_mesh,
        #                                  event='mouseup')
        # self._zoom_move_picker = p3.Picker(controlling=self._background_mesh,
        #                                    event='mousemove')

        # self._zoom_rect_geometry = p3.BufferGeometry(
        #     attributes={
        #         'position': p3.BufferAttribute(array=np.zeros((5, 3))),
        #     })
        # self._zoom_rect_material = p3.LineBasicMaterial(color='black',
        #                                                 linewidth=1)
        # self._zoom_rect_line = p3.Line(geometry=self._zoom_rect_geometry,
        #                                material=self._zoom_rect_material,
        #                                visible=False)

        # self.width = 600
        # self.height = 400
        # # self.camera = p3.PerspectiveCamera(position=[0.0, 0, 2],
        # #                                    aspect=self.width / self.height)
        # # self.camera = p3.OrthographicCamera(-0.1, 1.1, 1.1, -0.1, -1, 100)
        # self.camera = p3.OrthographicCamera(-0.001, 1.0, 1.0, -0.001, -1, 100)
        # self.scene = p3.Scene(children=[
        #     self.camera, self._background_mesh, self._zoom_rect_line
        # ],
        #                       background=self.background_color)
        # self.controls = p3.OrbitControls(controlling=self.camera,
        #                                  enableZoom=False,
        #                                  enablePan=False)
        # self.renderer = p3.Renderer(
        #     camera=self.camera,
        #     scene=self.scene,
        #     controls=[self.controls],
        #     width=self.width,
        #     height=self.height,
        #     # antialiasing=True
        # )
        self.toolbar = Toolbar()
        self.toolbar._home.on_click(self.home)
        self.toolbar._zoom.observe(self.toggle_pickers, names='value')
        self.toolbar._pan.observe(self.toggle_pan, names='value')
        # self._zoom_mouse_down = False
        # self._zoom_mouse_moved = False

        # self.toolbar.layout = ipw.Layout(grid_area='toolbar')
        # self.renderer.layout = ipw.Layout(grid_area='main')

        # self.left_bar = ipw.VBox(layout=ipw.Layout(grid_area='left'))
        # self.right_bar = ipw.VBox(layout=ipw.Layout(grid_area='right'))
        # self.bottom_bar = ipw.HBox(layout=ipw.Layout(grid_area='bottom'))
        # self.top_bar = ipw.HBox(layout=ipw.Layout(grid_area='top'))

        super().__init__([self.toolbar])

        # super().__init__(
        #     children=[
        #         self.toolbar, self.renderer, self.left_bar, self.right_bar,
        #         self.bottom_bar, self.top_bar
        #     ],
        #     layout=ipw.Layout(
        #         grid_template_rows=f'auto {self.height}px 40px',
        #         # grid_template_columns='5% 5% 85% 5%',
        #         # grid_template_columns='40px 42px auto 0px',
        #         grid_template_columns='40px 65px auto 0px',
        #         grid_template_areas='''
        #     ". . top ."
        #     "toolbar left main right"
        #     ". . bottom ."
        #     ''',
        #         grid_gap='0px 0px'))

    def home(self, *args):
        for ax in self.axes:
            ax.reset()

    def toggle_pickers(self, change):
        for ax in self.axes:
            if change['new']:
                ax._zoom_down_picker.observe(ax.on_mouse_down, names=['point'])
                ax._zoom_up_picker.observe(ax.on_mouse_up, names=['point'])
                ax._zoom_move_picker.observe(ax.on_mouse_move, names=['point'])
                ax.renderer.controls = [
                    ax.controls, ax._zoom_down_picker, ax._zoom_up_picker,
                    ax._zoom_move_picker
                ]
            else:
                ax._zoom_down_picker.unobserve_all()
                ax._zoom_up_picker.unobserve_all()
                ax._zoom_move_picker.unobserve_all()
                ax.renderer.controls = [ax.controls]

    def toggle_pan(self, change):
        for ax in self.axes:
            ax.toggle_pan(change['new'])

    def add_axes(self, ax):
        self.axes.append(ax)
        ax.set_figure(self)
        self.add(ax)
        # self.camera.add(ax)
