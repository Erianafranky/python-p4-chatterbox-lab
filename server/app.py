from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

#returns an array of all messages as JSON
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = []
        for message in Message.query.all():
            message_dict = message.to_dict()
            messages.append(message_dict)

        response = make_response(
            jsonify(messages),
            200
        )

        return response
    
    #creates a new message with a body and username from params
    # returns the newly created post as JSON.
    elif request.method == 'POST':
        new_message = Message(
            body = request.get_json()['body'],
            username = request.get_json()['username']
        )

        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()

        response = make_response(
            jsonify(message_dict),
            201
        )

        return response

#deletes the message from the database.
@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    if request.method == 'DELETE':
            message = Message.query.filter(Message.id == id).first()
            db.session.delete(message)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Message deleted."    
            }

            response = make_response(
                jsonify(response_body),
                200
            )

            return response
    
    #updates the body of the message using params, and returns the updated message as JSON
    elif request.method == 'PATCH':
        message = Message.query.filter(Message.id==id).first()

        for attr in request.get_json():
            setattr(message, attr, request.get_json()[attr])

        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(
            jsonify(message_dict),
            200
        )

        return response


if __name__ == '__main__':
    app.run(port=5555)
