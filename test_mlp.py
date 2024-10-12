import os
import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'mlp')))

# from mlp.api_mlp import Train


# Train()


# import os
# from models.classification import ClassificationModel
# from models.detection import DetectionModel
# from utils.data_loader import get_data_loaders
# from utils.train_helper import save_model
# import json

from utils.data_loader import get_data_loaders
from utils.train_helper import save_model
import json
# from models.classification import ClassificationModel
# from models.detection import DetectionModel


from . import models


models.classification.ClassificationModel
