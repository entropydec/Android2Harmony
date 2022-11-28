import os.path
from typing import List

import numpy as np
import torch
from PIL import Image
from torch.autograd import Variable

# from sketch_module.utils.data import State
from sketch_module.search.vae import model, myTransform
from sketch_module.search.process_layout import generate_color_image
import importlib.resources
from Model.State import State
from util.FileHelper import FileHelper

model_file = FileHelper.join("models", "Epoch_20_Train_loss_0.0026_Test_loss_0.0027.pth")
model.load_state_dict(torch.load(model_file, map_location='cpu'))
model.eval()


def convert(path):
    data = Image.open(path).convert("RGB")
    data = myTransform(data)
    data = Variable(data)
    return data


def calculate(path1, path2):
    data1 = convert(path1)
    data2 = convert(path2)

    x = model.get_latent_var(data1)
    y = model.get_latent_var(data2)
    num = x[0].dot(y[0].T)
    denom = np.linalg.norm(x[0].detach().numpy()) * np.linalg.norm(y[0].detach().numpy())
    cos = num / denom
    return cos * 0.5 + 0.5


def get_original_score(user_ui, user_ui_num, model_color, states: List[State]):
    model_ui_num = len(states)
    score_array = [[0 for _ in range(model_ui_num)] for _ in range(user_ui_num)]
    generate_color_image([(state.get_state_id(), state.get_layout()) for state in states], model_color)

    for i in range(user_ui_num):
        user_ui_img = os.path.join(user_ui, f"UI_{i}.jpg")
        for j in range(model_ui_num):
            model_ui_img = os.path.join(model_color, f"{j}.jpg")
            score = calculate(user_ui_img, model_ui_img)
            score_array[i][j] = format(score, ".4f")
    return score_array
