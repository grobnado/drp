import os
import pandas as pd
import numpy as np
import torch
import torchaudio.transforms as transforms
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from collections import defaultdict
import librosa
from torchvision.models import resnet18
import torchvision.models as models


class PretrainedResNet(nn.Module):
    def __init__(self, num_classes):
        super(PretrainedResNet, self).__init__()
        self.model = models.resnet18(pretrained=True)
        self.model.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)  # Изменение первого слоя для работы с одноканальными изображениями
        
        # Заморозка первых 5 параметров
        for param in list(self.model.parameters())[:10]:
            param.requires_grad = False
        
        # Замена выходного слоя
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, num_classes)

    def forward(self, x):
        return self.model(x)