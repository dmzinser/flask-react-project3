import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user
from PIL import Image

photo = Blueprint('photos', 'photo', url_prefix='/photos')

@photo.route('', methods=["GET"])
def show_all_photos():
  try:
    photos = [model_to_dict(photo) for photo in models.Photo.select()]
    return jsonify(data=photos, status={"code": 200, "message": "Success"})
  except models.DoesNotExist:
    return jsonify(data={}, status={"code": 401, "message": " There was an error getting the resource"})

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

def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  f_name, f_ext = os.path.splitext(form_picture.filename)
  picture_name = random_hex + f_ext
  file_path_for_avatar = os.path.join(os.getcwd(), 'static/photo_uploads/' + picture_name)
  
  output_size = (250, 250)
  i = Image.open(form_picture)
  i.thumbnail(output_size)
  i.save(file_path_for_avatar)
  return picture_name

# @photo.route('/addphoto', methods=["POST"])
# def add_photo():
#   # HOW DO I SAVE A JSON IMAGE FILE?
#   payload = request.get_json()
#   print(payload, '<== THIS IS THE ADD PHOTO PAYLOAD')
#   print(current_user.get_id())
#   payload['user'] = current_user.get_id()
#   photo = models.Photo.create(**payload)
#   photo_dict = model_to_dict(photo)
#   return jsonify(data=photo_dict, status={"code": 201, "message": "Success"})