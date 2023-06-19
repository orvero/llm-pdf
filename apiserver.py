from flask import Flask, request, session, Response, jsonify
from flask_cors import CORS
from pdfquery import query_Pdf
from flask_sse import sse
from os import path, makedirs

app = Flask(__name__)
app.register_blueprint(sse, url_prefix="/stream")
CORS(
    app,
    origins=["*"],
    supports_credentials=True,
)


@app.route("/")
def hello_world():
    print(f'test sessing name {session.get("name")}')
    session["name"] = "test1"
    return "heart beat!"


@app.route("/tst", methods=["GET", "POST"])
def tst():
    print(f'test sessing name {session.get("name")}')
    return "heart beat tst!"


@app.route("/uploader", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        f = request.files["file"]
        file_path = path.join("queryfiles", f.filename)
        if not path.exists("queryfiles"):
            makedirs("queryfiles")
        f.save(file_path)
        print(f"upload file name {session.get('uploadFile')}")

        return jsonify(
            {"message": "file uploaded successfully", "fileName": f.filename}
        )


@app.route("/query")
def query():
    args = request.args
    fName = args.get("f")
    print(f"query file name {fName}")
    if fName is None:
        fName = "Austal Limited.pdf"
    answer = query_Pdf(args.get("q"), fName)
    return answer


@app.route("/events")
def events():
    def generate_events():
        yield "data: Event 1\n\n"
        yield "data: Event 2\n\n"

    return Response(generate_events(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.secret_key = "super secret key"
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = True
    app.run(host="0.0.0.0", port=5000)
