import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user
from PIL import Image

photo = Blueprint('photos', 'photo', url_prefix='/photos')

@photo.route('/<id>', methods=["DELETE"])
def delete_photo(id):
  delete_photo_query = models.Photo.delete().where(models.Photo.id == id)
  delete_photo_query.execute()
  return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

@photo.route('/<id>', methods=["PUT"])
def edit_photo(id):
  payload = request.get_json()
  edit_photo_query = models.Photo.update(**payload).where(models.Photo.id == id)
  edit_photo_query.execute()
  edited_photo = models.Photo.get_by_id(id)
  return jsonify(data=model_to_dict(edited_photo), status={"code": 200, "message": "Success"})

@photo.route('/<id>', methods=["GET"])
def show_one_photo(id):
  photo = models.Photo.get_by_id(id)
  print(photo.__dict__, "<== THIS IS THE PHOTO DICT IN THE SHOW ROUTE")
  return jsonify(data=model_to_dict(photo), status={"code": 200, "message": "Success"})

@photo.route('/addphoto', methods=["POST"])
def add_photo():
  payload = request.get_json()
  print(payload, '<== THIS IS THE ADD PHOTO PAYLOAD')
  print(current_user.get_id())
  payload['user'] = current_user.get_id()
  photo = models.Photo.create(**payload)
  photo_dict = model_to_dict(photo)
  return jsonify(data=photo_dict, status={"code": 201, "message": "Success"})