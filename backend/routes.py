from app import app,db
from models import Friends
from flask import request, jsonify
from validation import FriendInfo
from logger import logger
from pydantic import ValidationError

# Get all friends
@app.route("/api/friends", methods=["GET"])
def get_friends():
    friends = Friends.query.all()
    result = [friend.to_json() for friend in friends]
    return jsonify(result),200


# Create a New Friend
@app.route("/api/friend/create", methods=["POST"])
def create_friend():
        body = request.json
        logger.debug(f"body : {body}")

        # Validate the input data
        try:
              validatore = FriendInfo.parse_obj(body).dict()
              logger.debug(f"Friends Object: {validatore}")
        except ValidationError as ve:
              logger.error(f"Validation error: {ve}")
              return jsonify({"error": str(ve)}), 400
        
        try:
            name = validatore["name"]
            role = validatore["role"]
            description = validatore["description"]
            gender = validatore["gender"]

            # fetch avatar image based on gender
            if gender == "male":
                img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
            elif gender == "female":
                img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
            else:
                img_url = None

            new_friend = Friends(name=name, role=role, description=description, gender=gender, img_url=img_url)

            db.session.add(new_friend)
            db.session.commit()

            return jsonify({"message": "Friend created successfully"}), 201 
        except Exception as e:
              db.session.rollback()
              logger.error(f"Error occurred: {e}")
              return jsonify({"error": str(e)}), 500

#delete friend
@app.route("/api/friend/delete/<int:id>", methods=["DELETE"])
def delete_friend(id):
    try: 
        friend = Friends.query.get(id)
        if not friend:
            return jsonify({"error": "Friend not found"}), 404 

        db.session.delete(friend)
        db.session.commit()
        return jsonify({"message": "Friend deleted successfully"}), 200
    except Exception as e :
         db.session.rollback()
         logger.error(f"Error occurred: {e}") 
         return jsonify({"error": str(e)}), 500

# update friend
@app.route("/api/friend/update/<int:id>", methods=["PATCH"])
def update_friend(id):
    try:
        friend= Friends.query.get(id)
        if not friend:
            return jsonify({"error": "Friend not found"}), 404
        
        body = request.json
        logger.debug(f"body : {body}")
        
        friend.name = body.get("name", friend.name)
        friend.role = body.get("role", friend.role)
        friend.description = body.get("description", friend.description)
        friend.gender = body.get("gender", friend.gender)

        db.session.commit()
        return jsonify(friend.to_json()), 200
    except Exception as e :
         db.session.rollback()
         logger.error(f"Error occurred: {e}")
         return jsonify({"error": str(e)}), 500