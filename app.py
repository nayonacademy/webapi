from api import API

app = API()

@app.route("/")
def home(request, response):
    response.text = "Welcome awesome api home page"

@app.route("/about")
def about(request, response):
    response.text = "This framework is build for learning and better understanding about python framework"

@app.route("/flowers")
class FlowerHandler:
    def get(self, req, resp):
        resp.text = "get all flowers"

    def post(self, req, resp):
        resp.text = "enter new flower"