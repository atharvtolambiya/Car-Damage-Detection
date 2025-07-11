from PIL import Image
import torch
from torch import nn
from torchvision import models,transforms

trained_model = None

class_name = ['F_Breakage', 'F_Crushed', 'F_Normal', 'R_Breakage', 'R_Crushed', 'R_Normal']
class CarclassRESNET(nn.Module):
    def __init__(self, num_class):
        super().__init__()
        self.model = models.resnet50(weights='DEFAULT')

        for param in self.model.parameters():
            param.requires_grad = False

        for param in self.model.layer4.parameters():
            param.requires_grad = True

        self.model.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(self.model.fc.in_features, num_class)
        )

    def forward(self, x):
        x = self.model(x)
        return x

def predict(image_path):

    image = Image.open(image_path).convert('RGB')
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image_tensor = transform(image).unsqueeze(0)

    global  trained_model
    if trained_model is None:
        trained_model = CarclassRESNET(num_class=len(class_name))
        trained_model.load_state_dict(torch.load('model/saved_model.pth'))
        trained_model.eval()

    with torch.no_grad():
        output = trained_model(image_tensor)
        _,predicted = torch.max(output,1)
        return class_name[predicted.item()]
