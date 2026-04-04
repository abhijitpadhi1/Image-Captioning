import torch
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights

class EncoderCNN(nn.Module):
    def __init__(self, pretrained=True):
        super().__init__()

        if pretrained:
            resnet = resnet50(weights=ResNet50_Weights.DEFAULT)
        else:
            resnet = resnet50(weights=None)

        modules = list(resnet.children())[:-2]
        self.resnet = nn.Sequential(*modules)

        if pretrained:
            for param in self.resnet.parameters():
                param.requires_grad = False

    def forward(self, images):
        features = self.resnet(images)  # (B, 2048, 7, 7)
        B, C, H, W = features.shape
        features = features.view(B, C, -1).permute(0, 2, 1)
        return features