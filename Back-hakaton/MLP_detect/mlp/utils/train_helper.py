import torch

def save_model(model, path):
    torch.save(model.state_dict(), path)

def load_model(model_class, path, config):
    model = model_class(config)
    model.load_state_dict(torch.load(path))
    model.eval()
    return model
