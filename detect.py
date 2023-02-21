import argparse
import os
import sys
import os.path as osp

import torch

ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from yolov6.utils.events import LOGGER
from yolov6.core.inferer import Inferer


@torch.no_grad()
def run(source,model_name):
    img_size=640
    conf_thres=0.4
    iou_thres=0.45
    max_det=1000
    device=''
    save_txt=False
    save_img=True
    save_dir=None
    view_img=True
    classes=None
    agnostic_nms=False
    project=osp.join(ROOT, '')
    name=''
    hide_labels=False 
    hide_conf=False
    half=False
    if save_dir is None:
        save_dir = osp.join(project, name)
        save_txt_path = osp.join(save_dir, 'labels')
    else:
        save_txt_path = save_dir
    if (save_img or save_txt) and not osp.exists(save_dir):
        os.makedirs(save_dir)
    else:
        LOGGER.warning('Save directory already existed')
    if save_txt:
        save_txt_path = osp.join(save_dir, 'labels')
        if not osp.exists(save_txt_path):
            os.makedirs(save_txt_path)

    # Inference
    # source = 'input.jpg'
    weights =   os.path.join(ROOT, "weights", model_name)
    device = 0
    yaml =   os.path.join(ROOT, "data", "data.yaml")
    img_size = [640, 640]
    # half = 'store_true'
    inferer = Inferer(source, weights, device, yaml, img_size, half)
    result_file,count = inferer.infer(conf_thres, iou_thres, classes, agnostic_nms, max_det, save_dir, save_txt, save_img, hide_labels, hide_conf, view_img)
    print(count)
    return result_file,count
    
# print(run("input.jpg","best_ckpt.pt"))

# for filename in os.listdir("input"):
#     f = os.path.join("input", filename)
#     # checking if it is a file
#     if os.path.isfile(f):
#         run(f)

# run("input.png")
# os.path.join(ROOT, "weights", "kinnow.pt")

