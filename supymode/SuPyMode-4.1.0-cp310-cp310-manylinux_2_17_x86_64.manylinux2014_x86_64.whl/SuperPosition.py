#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

from MPSPlots.Render2D import Axis, Mesh, Line


class SuperPosition():
    def __init__(self, SuperSet, InitialAmplitudes: list):
        self.SuperSet = SuperSet
        self.InitialAmplitudes = numpy.asarray(InitialAmplitudes).astype(complex)
        self._CouplerLength = None
        self._Amplitudes = None
        self.Init()

    def Init(self) -> None:
        shape = [len(self.InitialAmplitudes)] + list(self.SuperSet[0].FullFields.shape)

        self.Fields = numpy.zeros(shape)
        for n, mode in enumerate(self.SuperSet.SuperModes):
            self.Fields[n] = mode.FullFields

    def Propagate(self, rTol: float = 1e-8, aTol: float = 1e-7, MaxStep: float = numpy.inf) -> None:
        Matrix = self.SuperSet.GetPropagationMatrix()

        Z_vs_itr_Interp = interp1d(self.Distance, self.itrProfile, axis=-1)

        self.itr_vs_Matrix_Interp = interp1d(self.itrList, Matrix, axis=-1, fill_value='extrapolate')

        def foo(z, y):
            itr = Z_vs_itr_Interp(z)
            return 1j * self.itr_vs_Matrix_Interp(itr).dot(y)

        sol = solve_ivp(foo,
                        y0=self.InitialAmplitudes,
                        t_span=[0, self.CouplerLength],
                        method='RK45',
                        rtol=rTol,
                        atol=aTol,
                        max_step=MaxStep)

        self.RawAmplitudes, self.RawDistances = sol.y, sol.t

        self.AmplitudeInterpolation = interp1d(self.RawDistances, self.RawAmplitudes, axis=-1)

        self.Slice_vs_itr_Interp = interp1d(self.RawDistances, numpy.arange(self.RawDistances.size), axis=-1)

    def CreateitrProfile(self, CouplerLength: float,
                               itrf: float,
                               Type: str = 'linear',
                               itri: float = 1,
                               Sigma: float = None,
                               Num: int = 100) -> None:

        self.CouplerLength = CouplerLength
        self.Distance = numpy.linspace(0, self.CouplerLength, Num)

        if Type.lower() in ['lin', 'linear']:
            segment = numpy.linspace(itri, itrf, Num // 2)
            self.itrProfile = numpy.concatenate([segment, segment[::-1]])

        if Type.lower() in ['exp', 'exponential']:
            # TODO: add slope computing.
            segment = numpy.exp(- numpy.linspace(0, self.CouplerLength, Num // 2) / 100)
            self.itrProfile = numpy.concatenate([segment, segment[::-1]])
            Scale = abs(self.itrProfile.max() - self.itrProfile.min())
            self.itrProfile /= Scale / abs(itri - itrf)
            self.itrProfile -= self.itrProfile.max() - itri

        if Type.lower() in ['gauss', 'gaussian']:
            assert Sigma is not None, "You must provide a value for Gaussian standard deviation, [Sigma]."
            self.itrProfile = numpy.exp(((self.Distance - self.Distance.mean()) / Sigma)**2)
            Scale = abs(self.itrProfile.max() - self.itrProfile.min())
            self.itrProfile /= Scale / abs(itri - itrf)
            self.itrProfile -= self.itrProfile.max() - itri

    @property
    def itrList(self):
        return self.SuperSet.itrList

    def itr2Slice(self, itr: float) -> int:
        return int(self.Slice_vs_itr_Interp(itr))

    def Amplitudes(self, Slice: int, itr: float = None):
        amplitudes = self.RawAmplitudes[:, Slice]
        return amplitudes

    def PlotAmplitudes(self):
        Fig = Plots.Scene(Title='SuPyMode Figure', UnitSize=(10, 4))

        ax0 = Axis(Row=0,
                   Col=0,
                   xLabel='Z-propagation distance',
                   yLabel=r'Mode amplitude',
                   Grid=True,
                   Legend=True,
                   WaterMark='SuPyMode')

        ax1 = Axis(Row=1,
                   Col=0,
                   xLabel='Z-propagation distance',
                   yLabel=r'itr profile',
                   Grid=True,
                   Legend=True,
                   WaterMark='SuPyMode')

        A = self.InitialAmplitudes.dot(self.RawAmplitudes)

        artist0 = Line(X=self.RawDistances, Y=A.real, Label='real part', Fill=False)
        artist1 = Line(X=self.RawDistances, Y=A.imag, Label='imag part', Fill=False)
        artist2 = Line(X=self.Distance, Y=self.itrProfile, Label='', Fill=False)

        ax0.AddArtist(artist0, artist1)
        ax1.AddArtist(artist2)

        Fig.AddAxes(ax0, ax1)

        return Fig

    def PlotField(self, itr: list):

        Slices = [self.itr2Slice(itr) for itr in ToList(itr)]

        Fig = Plots.Scene(Title='SuPyMode Figure', UnitSize=(4, 4))

        amplitudes = self.Amplitudes(0)

        Colorbar = Plots.ColorBar(Discreet=False, Position='bottom')

        for n, slice in enumerate(Slices):

            ax = Axis(Row=0,
                      Col=n,
                      xLabel=r'x [$\mu m$]',
                      yLabel=r'y [$\mu m$]',
                      Title=f'Mode field  [itr: {self.itrList[slice]:.2f}]',
                      Legend=False,
                      Grid=False,
                      Equal=True,
                      Colorbar=Colorbar,
                      xScale='linear',
                      yScale='linear')

            artist = Mesh(X=self.SuperSet.FullxAxis,
                          Y=self.SuperSet.FullyAxis,
                          Scalar=self.Fields[0, slice, ...],
                          ColorMap=FieldMap)

            ax.AddArtist(artist)

            Fig.AddAxes(ax)

        return Fig

    def PlotPropagation(self):
        if self._Amplitudes is None:
            self.ComputeAmpltiudes()

        y = self.AmplitudeInterpolation(self.Distance)

        z = self.Distance

        Field = self.SuperSet[0].FullFields.astype(complex) * 0.

        for mode, _ in enumerate(self.InitialAmplitudes):
            a = y[mode].astype(complex)
            field = self.SuperSet[mode].FullFields.astype(complex)
            Field += numpy.einsum('i, ijk->ijk', a, field)

        surface = mlab.surf(numpy.abs(Field[0]), warp_scale="auto")

        @mlab.animate(delay=100)
        def anim_loc():
            for n, _ in enumerate(self.Distance):
                surface.mlab_source.scalars = numpy.abs(numpy.abs(Field[n]))

                yield

        anim_loc()
        mlab.show()
