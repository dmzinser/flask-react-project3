import models

import os
import sys
import secrets
from PIL import Image

from flask import Blueprint, request, jsonify, url_for, send_file
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user', url_prefix='/user')

@user.route('/<id>', methods=["DELETE"])
def delete_user(id):
  delete_user_query = models.User.delete().where(models.User.id == id)
  delete_user_query.execute()
  return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

@user.route('/<id>/edit', methods=["PUT"])
def edit_user(id):
  payload = request.get_json()
  edit_user_query = models.User.update(**payload).where(models.User.id == id)
  edit_user_query.execute()
  edited_user = models.User.get_by_id(id)
  return jsonify(data=model_to_dict(edited_user), status={"code": 200, "message": "Success"})

@user.route('/<id>/photos', methods=["GET"])
def show_all_user_photos(id):
  user = models.User.get_by_id(id)
  photos = [model_to_dict(photo) for photo in user.photos]
  def delete_key(item, key):
    del item[key]
    return item
  photo_without_user = [delete_key(photo, 'user') for photo in photos]
  return jsonify(data=photo_without_user, status={"code": 200, "message": "Success"})

@user.route('/<id>', methods=["GET"])
def show_one_user(id):
  user = models.User.get_by_id(id)
  print(user.__dict__)
  return jsonify(data=model_to_dict(user), status={"code": 200, "message": "Success"})

@user.route('/login', methods=["POST"])
def login():
  payload = request.form.to_dict()
  print(payload, '<== THIS IS THE LOGIN PAYLOAD')
  try:
    user = models.User.get(models.User.username == payload['username'])
    user_dict = model_to_dict(user)
    if(check_password_hash(user_dict['password'], payload['password'])):
      del user_dict['password']
      login_user(user)
      print(user, "<== THIS IS THE LOGIN USER")
      return jsonify(data=user_dict, status={"code": 200, "message": "Success"})
    else:
      return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
  except models.DoesNotExist:
    return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})

def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  f_name, f_ext = os.path.splitext(form_picture.filename)
  picture_name = random_hex + f_ext
  file_path_for_avatar = os.path.join(os.getcwd(), 'static/profile_pics/' + picture_name)
  
  output_size = (125, 125)
  i = Image.open(form_picture)
  i.thumbnail(output_size)
  i.save(file_path_for_avatar)
  return picture_name

@user.route('/signup', methods=["POST"])
def signup():
  pay_file = request.files
  payload = request.form.to_dict()
  dict_file = pay_file.to_dict()
  print(payload, "<=== THIS IS THE SIGNUP PAYLOAD")
  print(dict_file, "<== THIS IS THE SIGNUP DICT_FILE")
  payload['email'].lower()
  try:
    models.User.get(models.User.email == payload['email'])
    return jsonify(data={}, status={"code": 401, "message": "A User with that name or email already exists"})
  except models.DoesNotExist:
    payload['password'] = generate_password_hash(payload['password'])
    file_picture_path = save_picture(dict_file['file'])
    payload['image'] = file_picture_path
    user = models.User.create(**payload)
    login_user(user)
    current_user.image = file_picture_path
    user_dict = model_to_dict(user)
    print(user_dict)
    print(type(user_dict))

    del user_dict['password']
    return jsonify(data=user_dict, status={"code": 201, "message": "Success"})