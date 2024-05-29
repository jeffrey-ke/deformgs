#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use 
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

import torch
from torch import nn
import numpy as np
from utils.graphics_utils import getWorld2View2, getProjectionMatrix, getProjectionMatrixPanopto, getWorld2View2Panopto

class Camera(nn.Module):
    def __init__(self, colmap_id, R, T, FoVx, FoVy, image, gt_alpha_mask,
                 image_name, uid,
                 trans=np.array([0.0, 0.0, 0.0]), scale=1.0, data_device = "cuda", time = 0,
                 view_id = None, time_id = None, flow = None, c_x = None, c_y = None, f_x = None, f_y = None, width=None, height=None,image_path=None,
                 mask=None
                 ):
        super(Camera, self).__init__()

        self.uid = uid
        self.colmap_id = colmap_id
        self.R = R
        self.T = T
        self.FoVx = FoVx
        self.FoVy = FoVy
        self.image_name = image_name
        self.time = time
        self.view_id = view_id
        self.time_id = time_id
        self.flow = flow

        self.f_x = f_x
        self.f_y = f_y
        self.c_x = c_x
        self.c_y = c_y
        self.width = width
        self.height = height
        self.image_path = image_path

        try:
            self.data_device = torch.device(data_device)
        except Exception as e:
            print(e)
            print(f"[Warning] Custom device {data_device} failed, fallback to default cuda device" )
            self.data_device = torch.device("cuda")
        
        self.original_image = image.clamp(0.0, 1.0)
        self.mask = mask
        # .to(self.data_device)
        if self.width is None:
            self.image_width = self.original_image.shape[2]
        else:
            self.image_width = self.width
        
        if self.height is None:
            self.image_height = self.original_image.shape[1]
        else:   
            self.image_height = self.height

        if gt_alpha_mask is not None:
            self.original_image *= gt_alpha_mask
            # .to(self.data_device)
        else:
            self.original_image *= torch.ones((1, self.image_height, self.image_width))
                                                #   , device=self.data_device)

            
        self.zfar = 100.0
        self.znear = 1.0 # DEBUG

        self.trans = trans
        self.scale = scale
        
    
        if self.f_x is None:
            self.world_view_transform = torch.tensor(getWorld2View2(R, T, trans, scale)).transpose(0, 1)
        else:
            self.world_view_transform = torch.tensor(getWorld2View2Panopto(R,T)).transpose(0,1)
        
        # if view_id is not None:
        #     breakpoint()
        # .cuda()
        if f_x is None:
            self.projection_matrix = getProjectionMatrix(znear=self.znear, zfar=self.zfar, fovX=self.FoVx, fovY=self.FoVy)
        else:
            self.projection_matrix = getProjectionMatrixPanopto(f_x=f_x,f_y=f_y,c_x=c_x,c_y=c_y,width=width,height=height,znear=self.znear,zfar=self.zfar)
        # print(self.projection_matrix)
        # print(self.projection_matrix.shape)

        # .cuda()
        self.full_proj_transform = (self.world_view_transform.unsqueeze(0).bmm(self.projection_matrix)).squeeze(0)
        self.camera_center = self.world_view_transform.inverse()[3, :3]
 


class MiniCam:
    def __init__(self, width, height, fovy, fovx, znear, zfar, world_view_transform, full_proj_transform, time):
        self.image_width = width
        self.image_height = height    
        self.FoVy = fovy
        self.FoVx = fovx
        self.znear = znear
        self.zfar = zfar
        self.world_view_transform = world_view_transform
        self.full_proj_transform = full_proj_transform
        view_inv = torch.inverse(self.world_view_transform)
        self.camera_center = view_inv[3][:3]
        self.time = time

