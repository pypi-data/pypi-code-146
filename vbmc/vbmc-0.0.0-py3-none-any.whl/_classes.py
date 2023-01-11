#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ._kernel import vbmc_kernel

import numpy as np
import matplotlib.pyplot as plt
from abc import ABCMeta, abstractmethod

import datetime,time
import json,pickle,bz2

from .utilities import calTime,set_params,ToJsonEncoder

import gc
#import warnings
#warnings.filterwarnings("ignore", category=RuntimeWarning)

__all__ = [
'vbmc',
]

# =============================================================================
# Base solid model
# =============================================================================

class BaseVoxelMonteCarlo(metaclass = ABCMeta):
    @abstractmethod
    def __init__(self,*,nPh,model,dtype_f=np.float32,dtype=np.int32,
                 beam_type = 'TEM00',w_beam = 0,
                 beam_angle = 0,initial_refrect_by_angle = False,
                 first_layer_clear = False,
                 ):

        def __check_list_name(name,name_list):
            if not(name in name_list):
                raise ValueError('%s is not a permitted for factor. Please choose from %s.'%(name,name_list))

        self.beam_type_list=['TEM00',False]
        __check_list_name(beam_type,self.beam_type_list)
        self.beam_type = beam_type

        self.dtype = dtype
        self.dtype_f = dtype_f
        self.nPh = nPh
        self.w_beam = w_beam

        self.initial_refrect_by_angle = initial_refrect_by_angle
        self.beam_angle = beam_angle

        self.model = model
        self.first_layer_clear=first_layer_clear

    def start(self):
        self.nPh = int(self.nPh)
        self._reset_results()
        self._generate_initial_coodinate(self.nPh)

        self.add = self.add.astype(self.dtype)
        self.p = self.p.astype(self.dtype_f)
        self.v = self.v.astype(self.dtype_f)
        self.w = self.w.astype(self.dtype_f)
        print("")
        print("###### Start ######")
        print("")
        start_ = time.time()
        self.add,self.p,self.v,self.w = vbmc_kernel(
            self.add, self.p,self.v, self.w,
            self.model.ma, self.model.ms, self.model.n, self.model.g,
            self.model.voxel_model.astype(np.uint8), self.model.voxel_space,
            np.int32(self.nPh), np.int8(self.model.end_point)
        )

        self._end_process()
        print("###### End ######")
        self.getRdTtRate()
        calTime(time.time(), start_)
        #del func
        return self

    def _end_process(self):#書き換え
        #index = np.where(~np.isnan(self.w))[0]
        self.v_result = self.v#[:,index]
        self.p_result = self.p#[:,index]
        self.add_result = self.add#[:,index]
        self.w_result = self.w#[index]

    def _reset_results(self):
        self.v_result = np.empty((3,1)).astype(self.dtype_f)
        self.p_result = np.empty((3,1)).astype(self.dtype_f)
        self.add_result = np.empty((3,1)).astype(self.dtype)
        self.w_result = np.empty(1).astype(self.dtype_f)
        return self

    def get_voxel_model(self):
        return self.model.voxel_model

    def _generate_initial_coodinate(self,nPh):
        self._set_inital_add()
        self._set_beam_distribution()
        self._set_inital_vector()
        self._set_inital_w()


    def _set_inital_add(self):
        if self.beam_type == 'TEM00':
            self.add =  np.zeros((3, self.nPh),dtype = self.dtype)
        self.add[0] = self._get_center_add(self.model.voxel_model.shape[0])
        self.add[1] = self._get_center_add(self.model.voxel_model.shape[1])
        if self.first_layer_clear:
            self.add[2] = self.first_layer_clear+1
        else:
            self.add[2] = 1

    def _get_center_add(self,length):
        #addの中心がローカル座標（ボックス内）の中心となるため、
        #ボクセル数が偶数の時は、1/2小さい位置を中心とし光を照射し、
        #逆変換時（_encooder）も同様に1/2小さい位置を中心として元のマクロな座標に戻す。
        return int((length-1)/2)

    def _set_inital_vector(self):
        if self.beam_type == 'TEM00':
            self.v = np.zeros((3,self.nPh)).astype(self.dtype_f)
            self.v[2] = 1
            if self.beam_angle!=0 and self.w_beam==0:
                #ビーム径がある場合はとりあえず無視
                #角度はrad表記
                ni = self.model.n[-1]
                nt = self.model.n[0]
                ai = self.beam_angle
                at = np.arcsin(np.sin(ai)*ni/nt)
                self.v[0] = np.sin(at)
                self.v[2] = np.cos(at)
                if self.initial_refrect_by_angle:
                    Ra = ((np.sin(ai-at)/np.sin(ai+at))**2\
                    +(np.tan(ai-at)/np.tan(ai+at))**2)/2

                    self.inital_del_num = np.count_nonzero(Ra>=np.random.rand(self.nPh))
                    self.v = np.delete(self.v, np.arange(self.inital_del_num), 1)
                    self.p = np.delete(self.p, np.arange(self.inital_del_num), 1)
                    self.add = np.delete(self.add, np.arange(self.inital_del_num), 1)
                    sub_v = np.zeros((3,self.inital_del_num)).astype(self.dtype_f)
                    sub_v[0] = np.sin(ai)
                    sub_v[2] = -np.cos(ai)
                    self.v_result = np.concatenate([self.v_result,
                    sub_v],axis = 1)
                    self.p_result = np.concatenate([self.p_result,
                    self.p[:,:self.inital_del_num]],axis = 1)
                    self.add_result = np.concatenate([self.add_result,
                    self.add[:,:self.inital_del_num]],axis = 1)
        else:
            print("ビームタイプが設定されていません")

    def _set_inital_w(self):
        if self.beam_type == 'TEM00':
            self.w = np.ones(self.nPh).astype(self.dtype_f)
            Rsp = 0
            n1 = self.model.n[-1]
            n2 = self.model.n[0]
            if n1 != n2:
                Rsp = ((n1-n2)/(n1+n2))**2
                if self.beam_angle!=0 and self.w_beam==0:
                    ai = self.beam_angle
                    at = np.arcsin(np.sin(ai)*n1/n2)
                    Rsp = ((np.sin(ai-at)/np.sin(ai+at))**2\
                    +(np.tan(ai-at)/np.tan(ai+at))**2)/2
                elif self.first_layer_clear:
                    n3=self.model.n[1]
                    r2 = ((n3-n2)/(n3+n2))**2
                    Rsp = Rsp+r2*(1-Rsp)**2/(1-Rsp*r2)
                self.w -= Rsp

            if self.beam_angle!=0 and self.w_beam==0:
                if self.initial_refrect_by_angle:
                    self.w[:] = 1
                    self.w = np.delete(self.w, np.arange(self.inital_del_num), 0)
                    self.w_result = np.concatenate([self.w_result,
                    self.w[:self.inital_del_num]],axis = 0)
        else:
            print("ビームタイプが設定されていません")

    def _set_beam_distribution(self):
        if self.beam_type == 'TEM00':
            self.p = np.zeros((3,self.nPh)).astype(self.dtype_f)
            self.p[2] = -self.model.voxel_space/2
            if self.w_beam!= 0:
                print("%sを入力"%self.beam_type)
                #ガウシアン分布を生成
                gb = np.array(self.gaussianBeam(self.w_beam)).astype(self.dtype_f)
                #ガウシアン分布を各アドレスに振り分ける

                l = self.model.voxel_space
                pp = (gb/l).astype("int16")
                ind = np.where(gb<0)
                pp[ind[0].tolist(),ind[1].tolist()] -= 1
                pa = gb - (pp+1/2)*l
                ind = np.where((np.abs(pa)>=l/2))
                pa[ind[0].tolist(),ind[1].tolist()] = \
                    np.sign(pa[ind[0].tolist(),ind[1].tolist()])*(l/2)
                pa += l/2
                self.add[:2] = self.add[:2] + pp
                self.p[:2] = pa.astype(self.dtype_f)
        else:
            print("ビームタイプが設定されていません")

    def _get_beam_dist(self,x,y):
        fig = plt.figure(figsize=(10,6),dpi=70)
        ax = fig.add_subplot(111)
        ax.set_aspect('equal')
        H = ax.hist2d(x,y, bins=100,cmap="plasma")
        ax.set_title('Histogram for laser light intensity')
        ax.set_xlabel('X [mm]')
        ax.set_ylabel('Y [mm]')
        fig.colorbar(H[3],ax=ax)
        plt.show()

    def gaussianBeam(self,w=0.54):
        #TEM00のビームを生成します
        r = np.linspace(-w*2,w*2,100)
        #Ir = 2*np.exp(-2*r**2/(w**2))/(np.pi*(w**2))
        Ir = np.exp(-2*r**2/(w**2))
        x = np.random.normal(loc=0, scale=w/2, size=self.nPh)
        y = np.random.normal(loc=0, scale=w/2, size=self.nPh)

        fig, ax1 = plt.subplots()
        ax1.set_title('Input laser light distribution')
        ax1.hist(x, bins=100, color="C0")
        ax1.set_ylabel('Number of photon')
        ax2 = ax1.twinx()
        ax2.plot(r, Ir, color="k")
        ax2.set_xlabel('X [mm]')
        ax2.set_ylabel('Probability density')
        plt.show()
        self._get_beam_dist(x,y)
        return x,y

    def get_result(self):
        encoded_position = self._encooder(self.p_result,self.add_result)
        df_result = {
            'p':encoded_position.T,
            'v':self.v_result.T,
            'w':self.w_result,
            'nPh':self.nPh
        }
        return df_result

    def get_model_params(self):
        return self.model.get_params()

    def _encooder(self,p,add):
        space = self.model.voxel_space
        center_add_x = self._get_center_add(self.model.voxel_model.shape[0])
        center_add_y = self._get_center_add(self.model.voxel_model.shape[1])
        encoded_position = p.copy()
        encoded_position[0] = space*(add[0]-center_add_x)+p[0]
        encoded_position[1] = space*(add[1]-center_add_y)+p[1]
        encoded_position[2] = np.round(space*(add[2]-1)+p[2]+space/2,6)
        return encoded_position

    def set_monte_params(
            self,*,
            nPh = 5e4, #　Enter the number of photons.
            w_beam = 0, # Enter the beam radius for TEM00. The scale depends on the units of optical properties.
            beam_angle = 0, # Type in radian.
            first_layer_clear = False, # Type the first sequence number of the second layer along the z-axis.
        ):
        self.nPh = nPh
        self.w_beam = w_beam
        self.beam_angle = beam_angle
        self.first_layer_clear = first_layer_clear
        return self

    def build(self,*initial_data, **kwargs):
        if initial_data == () and kwargs == {}:
            pass
        else:
            self.model.set_params(*initial_data, **kwargs)
        self.model.build()

    def getRdTtRate(self):
        self.Tt_index = np.where(self.v_result[2]>0)[0]
        self.Rd_index = np.where(self.v_result[2]<0)[0]
        self.Rdw = self.w_result[self.Rd_index].sum()/self.nPh
        self.Ttw = self.w_result[self.Tt_index].sum()/self.nPh
        print('######')
        print('Mean Rd %0.6f'% self.Rdw)
        print('Mean Td %0.6f'% self.Ttw)
        print()
        return self.Rdw,self.Ttw

    def save_result(self,fname,
    *,coment='',save_monte = True,save_params = True,):
        start_ = time.time()

        if save_monte:
            res = self.get_result()
            save_name = fname+"_LID.pkl.bz2"
            with bz2.open(save_name, 'wb') as fp:
                fp.write(pickle.dumps(res))
            print("Monte Carlo results saved in ")
            print("-> %s" %(save_name))
            print('')

        if save_params :
            info = self._calc_info(coment)
            save_name = fname+"_info.json"
            with open(save_name, 'w') as fp:
                json.dump(info,fp,indent=4,cls= ToJsonEncoder)
            print("Calculation conditions are saved in")
            print("-> %s" %(save_name))
            print('')

        calTime(time.time(), start_)

    def _calc_info(self,coment=''):
        calc_info = {
            'Date':datetime.datetime.now().isoformat(),
            'coment':coment,
            'number_of_photons':self.nPh,
            'calc_dtype':"32 bit",
            'model':{
                'model_name':self.model.model_name,
                'model_params':self.model.params,
            },
            'w_beam':self.w_beam,
            'beam_angle':self.beam_angle,
            'initial_refrect_mode':self.initial_refrect_by_angle,
            'beam_mode':'TEM00',
        }
        return calc_info
# =============================================================================
# Modeling class
# =============================================================================
class VoxelModel:
    def __init__(self):
        self.model_name = 'VoxelModel'
        self.dtype_f = np.float32
        self.dtype = np.uint8
        self.params = {
            'voxel_space':0.02,
            'n':[1.],
            'n_air':1.,
            'ma':[10],
            'ms':[90],
            'g':[0.75],
            'end_point':False, #Basically, set it to False.
            }
        self.keys = list(self.params.keys())
        self._param_instantiating()
        self.voxel_model = np.zeros((1000,1000,1),dtype = self.dtype)

    def _param_instantiating(self):
        f = self.dtype_f
        self.n =np.array(self.params['n']+[self.params['n_air']]).astype(f)
        self.ms = np.array(self.params['ms']).astype(f)
        self.ma = np.array(self.params['ma']).astype(f)
        self.g = np.array(self.params['g']).astype(f)
        self.voxel_space = self.params['voxel_space']
        if self.params['end_point']:
            self.end_point = self.params['end_point']
        else:
            self.end_point = len(self.n)-1

    def build(self,outer_model):
        #thickness,xy_size,voxel_space,ma,ms,g,n,n_air
        del self.voxel_model
        gc.collect()
        self.voxel_model = outer_model
        self._make_voxel_model()
        self.getModelSize()

    def set_params(self,*initial_data, **kwargs):
        set_params(self.params,self.keys,*initial_data, **kwargs)
        self._param_instantiating()

    def _add_array(self,X,num_pix,val,dtype):
        # Z方向
        ct = np.zeros((X.shape[0],X.shape[1],num_pix),dtype = dtype)+val
        X = np.concatenate((ct,X),2)
        X = np.concatenate((X,ct),2)
        # X方向
        ct = np.zeros((num_pix,X.shape[1],X.shape[2]),dtype = dtype)+val
        X = np.concatenate((ct,X),0)
        X = np.concatenate((X,ct),0)
        # Y方向
        ct = np.zeros((X.shape[0],num_pix,X.shape[2]),dtype = dtype)+val
        X = np.concatenate((ct,X),1)
        X = np.concatenate((X,ct),1)
        return X

    def _make_voxel_model(self):
        self.voxel_model = self._add_array(self.voxel_model,1,self.end_point,self.dtype)
        print("Shape of voxel_model ->",self.voxel_model.shape)

    def getModelSize(self):
        print("Memory area size for voxel storage: %0.3f Mbyte" % (self.voxel_model.nbytes*1e-6))

# =============================================================================
# Public montecalro model
# =============================================================================

class vbmc(BaseVoxelMonteCarlo):
    def __init__(
            self,*,
            nPh = 5e4, #　Enter the number of photons.
            w_beam = 0, # Enter the beam radius for TEM00. The scale depends on the units of optical properties.
            beam_angle = 0, # Type in radian.
            first_layer_clear = False, # Type the first sequence number of the second layer along the z-axis.
        ):
        beam_type = 'TEM00' # Only TEM00 is supported.
        dtype_f=np.float32
        dtype=np.int32
        model = VoxelModel()

        super().__init__(
            nPh = nPh, model = model,dtype_f=dtype_f,dtype=dtype,
            w_beam=w_beam,beam_angle = beam_angle,beam_type = beam_type,
            initial_refrect_by_angle = False,
            first_layer_clear=first_layer_clear,
        )


    def build(self,*initial_data, **kwargs):
        if initial_data == () and kwargs == {}:
            pass
        else:
            self.model.set_params(*initial_data, **kwargs)
        try:
            self.model.build(self.outer_model)
            del self.outer_model
            gc.collect()
        except:
            print("The default model has been built..")
            self.model._make_voxel_model()
        return self

    def set_model(self,u):
        if (u>255).any():
            print("Set the voxel value to 256 or less")
        else:
            self.outer_model = np.array(u).astype(np.uint8)
        return self

    def set_params(self,*initial_data, **kwargs):
        self.model.set_params(*initial_data, **kwargs)
        return self

    def get_model_fig(self,*,dpi=300,save_path = [False,False],):
        image = self.model.voxel_model
        resol0 = (image.shape[0]+1)*self.model.params['voxel_space']/2-\
        np.array([self.model.params['voxel_space']*i for i in range(image.shape[0]+1)])
        resol1 = (image.shape[1]+1)*self.model.params['voxel_space']/2-\
        np.array([self.model.params['voxel_space']*i for i in range(image.shape[1]+1)])
        resol2 = np.array([self.model.params['voxel_space']*i for i in range(image.shape[2]+1)])

        plt.figure(figsize=(5,5),dpi=100)
        plt.set_cmap(plt.get_cmap('gray'))
        plt.pcolormesh(resol0,resol2,image[:,int(image.shape[1]/2),:].T)
        plt.xlabel('X [mm]')
        plt.ylabel('Z [mm]')
        plt.ylim(resol2[-1],resol2[0])
        if save_path[0]:
            plt.savefig(
                save_path[0],
                dpi=dpi,
                orientation='portrait',
                transparent=False,
                pad_inches=0.0)
        plt.show()

        plt.figure(figsize=(6,5),dpi=100)
        plt.set_cmap(plt.get_cmap('gray'))
        plt.pcolormesh(resol1,resol2,image[int(image.shape[0]/2),:,:].T)
        plt.xlabel('Y [mm]')
        plt.ylabel('Z [mm]')
        plt.ylim(resol2[-1],resol2[0])
        if save_path[1]:
            plt.savefig(
                save_path[1],
                dpi=dpi,
                orientation='portrait',
                transparent=False,
                pad_inches=0.0)
        plt.show()
