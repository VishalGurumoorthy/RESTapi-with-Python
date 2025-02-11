from flask import Flask, request #request could be used in a resource
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#model to store videos
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    views = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"

# db.create_all()  -> to be done once -> may cause overriding of database
    

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str,help="name of the video is required", required = True)
video_put_args.add_argument("views", type=int,help="views of the video", required = True)
video_put_args.add_argument("likes", type=int,help="likes of the video", required = True)


video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=int,help="name of the video")
video_update_args.add_argument("views", type=int,help="views of the video")
video_update_args.add_argument("likes", type=int,help="likes of the video")


# videos = {}

# def abort_if_video_id_doesnt_exist(video_id):
#     if video_id not in videos:
#         abort(404, message = "Video is not available")

# def abort_if_video_exist(video_id):
#     if video_id in videos:
#         abort(409, message ="Video already exists")

resource_field = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer,

}

class video(Resource):
    @marshal_with(resource_field)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message = "Couldnt find Video of this ID")
        return result
    
    @marshal_with(resource_field)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result= VideoModel.query.filter_by(id = video_id).first()
        if result:
            abort(409, message = "Video ID Taken........")

        video = VideoModel(id = video_id, name = args['name'], views = args["views"],likes = args['likes'])
        #commit into DB
        db.session.add(video)
        db.session.commit()
        return video, 201
    
    @marshal_with(resource_field)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message="Video not found, Cannot update")
        
        if args["name"] :
            result.name = args["name"]
        if args["views"]:
            result.views = args["views"]
        if args["likes"]:
            result.likes = args["likes"]

        db.session.commit()

        return result


    
    def delete(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        del videos[video_id]
        return "", 204 #204 -> deleted successfully

#add parameter
api.add_resource(video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True)