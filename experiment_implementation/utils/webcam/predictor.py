import os
import json
import torch
import numpy as np

from torchvision import transforms
from utils.webcam.helper import get_config, shape_to_np

# Read config.ini file
SETTINGS, COLOURS, EYETRACKER, TF = get_config("utils/webcam/config.ini")


class Predictor:
    def __init__(self, model, model_data, config_file=None, gpu=1):
        super().__init__()

        _, ext = os.path.splitext(model_data)
        if ext == ".ckpt":
            self.model = model.load_from_checkpoint(model_data)
        else:
            with open(config_file) as json_file:
                config = json.load(json_file)
            self.model = model(config)
            self.model.load_state_dict(torch.load(model_data))

        self.gpu = gpu
        self.model.double()
        # self.model.cuda(self.gpu)
        # self.model.cuda()
        self.model.eval()

    def predict(self, *img_list, head_angle=None):
        images = []
        for img in img_list:
            if not img.dtype == np.uint8:
                img = img.astype(np.uint8)
            img = transforms.ToTensor()(img).unsqueeze(0)
            img = img.double()
            # img = img.cuda(self.gpu)
            # img = img.cuda()
            images.append(img)

        if head_angle is not None:
            # angle = torch.tensor(head_angle).double().flatten().cuda(self.gpu)
            # angle = torch.tensor(head_angle).double().flatten().cuda(self.gpu)
            # angle = torch.tensor(head_angle).double().flatten().cuda()
            angle = torch.tensor(head_angle).double().flatten()
            images.append(angle)

        with torch.no_grad():
            coords = self.model(*images)
            coords = coords.cpu().numpy()[0]

        return coords[0], coords[1]
