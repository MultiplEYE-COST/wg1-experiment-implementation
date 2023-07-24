import math
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import pytorch_lightning as pl

from collections import OrderedDict
from PIL import Image
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms


class FullModel(pl.LightningModule):
    def __init__(self, config):
        """
        I really really really wish pytorch had a way to calculate layer output sizes during init...
        """
        super().__init__()
        self.save_hyperparameters()  # stores hparams in saved checkpoint files

        feat_size = 64
        self.lr = config["lr"]

        # Example input for graph logging
        graph_example = [torch.rand(1, 3, feat_size, feat_size)] * 3
        graph_example.append(torch.rand(1, 1, feat_size, feat_size))
        graph_example.append(torch.rand(1))
        self.example_input_array = graph_example

        # Face input
        self.face_conv_input = nn.Conv2d(
            3, config["n_face_filt"], config["face_filt_size"]
        )
        face_feat_size = feat_size - (config["face_filt_size"] - 1)

        self.face_convs = nn.ModuleList()
        n_out_face = config["n_face_filt"]
        for _ in range(config["n_face_conv"]):
            n_in_face = n_out_face
            n_out_face = n_in_face * config["face_filt_grow"]

            self.face_convs.append(
                self.conv_block(n_in_face, n_out_face, config["face_filt_size"], "face")
            )

            # Calculate input feature size reductions due to conv and pooling
            face_feat_size = (face_feat_size - (config["face_filt_size"] - 1)) // 2

        face_feat_shape = (
            n_out_face,
            face_feat_size,
            face_feat_size,
        )
        face_feat_len = math.prod(face_feat_shape)

        # Eye inputs
        self.l_conv_input = nn.Conv2d(3, config["n_eye_filt"], config["eye_filt_size"])
        self.l_convs = nn.ModuleList()

        self.r_conv_input = nn.Conv2d(3, config["n_eye_filt"], config["eye_filt_size"])
        self.r_convs = nn.ModuleList()

        eye_feat_size = feat_size - (config["eye_filt_size"] - 1)

        n_out_eye = config["n_eye_filt"]
        for _ in range(config["n_eye_conv"]):
            n_in_eye = n_out_eye
            n_out_eye = n_in_eye * config["eye_filt_grow"]

            self.l_convs.append(
                self.conv_block(n_in_eye, n_out_eye, config["eye_filt_size"], "l")
            )
            self.r_convs.append(
                self.conv_block(n_in_eye, n_out_eye, config["eye_filt_size"], "r")
            )

            # Calculate input feature size reductions due to conv and pooling
            eye_feat_size = (eye_feat_size - (config["eye_filt_size"] - 1)) // 2

        eye_feat_shape = (
            n_out_eye,
            eye_feat_size,
            eye_feat_size,
        )
        eye_feat_len = math.prod(eye_feat_shape)

        # Head pos input
        self.head_pos_conv_input = nn.Conv2d(
            1, config["n_head_pos_filt"], config["head_pos_filt_size"]
        )
        head_pos_feat_size = feat_size - (config["head_pos_filt_size"] - 1)

        self.head_pos_convs = nn.ModuleList()
        n_out_head_pos = config["n_head_pos_filt"]
        for _ in range(config["n_head_pos_conv"]):
            n_in_head_pos = n_out_head_pos
            n_out_head_pos = n_in_head_pos * config["head_pos_filt_grow"]

            self.head_pos_convs.append(
                self.conv_block(
                    n_in_head_pos,
                    n_out_head_pos,
                    config["head_pos_filt_size"],
                    "head_pos",
                )
            )

            # Calculate input feature size reductions due to conv and pooling
            head_pos_feat_size = (
                head_pos_feat_size - (config["head_pos_filt_size"] - 1)
            ) // 2

        head_pos_feat_shape = (
            n_out_head_pos,
            head_pos_feat_size,
            head_pos_feat_size,
        )
        head_pos_feat_len = math.prod(head_pos_feat_shape)

        # FC layers -> output
        self.drop1 = nn.Dropout(0.2)
        self.fc1 = nn.Linear(
            face_feat_len + eye_feat_len * 2 + head_pos_feat_len + 1,
            config["dense_nodes"],
        )
        self.drop2 = nn.Dropout(0.2)
        self.fc2 = nn.Linear(config["dense_nodes"], config["dense_nodes"] // 2)
        self.fc3 = nn.Linear(config["dense_nodes"] // 2, 2)

    def forward(self, face, l_eye, r_eye, head_pos, head_angle):
        face = self.face_conv_input(face)
        for c in self.face_convs:
            face = c(face)
        face = face.flatten(start_dim=1)

        l_eye = self.l_conv_input(l_eye)
        for c in self.l_convs:
            l_eye = c(l_eye)
        l_eye = l_eye.flatten(start_dim=1)

        r_eye = self.r_conv_input(r_eye)
        for c in self.r_convs:
            r_eye = c(r_eye)
        r_eye = r_eye.flatten(start_dim=1)

        head_pos = self.head_pos_conv_input(head_pos)
        for c in self.head_pos_convs:
            head_pos = c(head_pos)
        head_pos = head_pos.flatten(start_dim=1)

        # Combine conv outputs, add head angle
        out = torch.hstack([face, l_eye, r_eye, head_pos])
        out = torch.hstack([out, head_angle.unsqueeze(1)])

        out = self.drop1(F.relu(self.fc1(out)))
        out = self.drop2(F.relu(self.fc2(out)))
        out = self.fc3(out)
        return out

    def conv_block(self, input_size, output_size, filter_size, name):
        block = nn.Sequential(
            OrderedDict(
                [
                    (
                        "{}_conv".format(name),
                        nn.Conv2d(input_size, output_size, filter_size),
                    ),
                    ("{}_relu".format(name), nn.ReLU()),
                    ("{}_norm".format(name), nn.BatchNorm2d(output_size)),
                    ("{}_pool".format(name), nn.MaxPool2d((2, 2))),
                ]
            )
        )
        return block

    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=self.lr)
        return optimizer

    def training_step(self, batch, batch_idx):
        face_aligned, l_eye, r_eye, head_pos, head_angle = (
            batch["face_aligned"],
            batch["l_eye"],
            batch["r_eye"],
            batch["head_pos"],
            batch["head_angle"],
        )
        y_hat = self(face_aligned, l_eye, r_eye, head_pos, head_angle)
        loss = F.mse_loss(y_hat, batch["targets"])
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        face_aligned, l_eye, r_eye, head_pos, head_angle = (
            batch["face_aligned"],
            batch["l_eye"],
            batch["r_eye"],
            batch["head_pos"],
            batch["head_angle"],
        )
        y_hat = self(face_aligned, l_eye, r_eye, head_pos, head_angle)
        val_loss = F.mse_loss(y_hat, batch["targets"])
        self.log("val_loss", val_loss)
        return val_loss

    def test_step(self, batch, batch_idx):
        face_aligned, l_eye, r_eye, head_pos, head_angle = (
            batch["face_aligned"],
            batch["l_eye"],
            batch["r_eye"],
            batch["head_pos"],
            batch["head_angle"],
        )
        y_hat = self(face_aligned, l_eye, r_eye, head_pos, head_angle)
        loss = F.mse_loss(y_hat, batch["targets"])
        self.log("test_loss", loss)
        return loss