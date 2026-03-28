import torch
import torch.nn as nn

# ─── NEUROSALES ADVANCED DEEP NEURAL ENGINE (PYTORCH) ───
class NeuroSalesNet(nn.Module):
    def __init__(self, input_dim=128):
        super(NeuroSalesNet, self).__init__()
        # Professional-grade architecture for high-accuracy revenue forecasting
        self.network = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.2),
            
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.15),
            
            nn.Linear(128, 64),
            nn.ReLU(),
            
            nn.Linear(64, 32),
            nn.ReLU(),
            
            nn.Linear(32, 1) # Output: Predicted Revenue
        )

    def forward(self, x):
        return self.network(x)
