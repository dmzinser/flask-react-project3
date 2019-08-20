import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
# from PIL import Image

photo = Blueprint('photos', 'photo', url_prefix='/user/<id>/photo') # I NEED HELP WITH THIS PREFIX