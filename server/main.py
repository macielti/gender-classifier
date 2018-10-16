import webapp2
import json
import jinja2
import os
from sklearn import tree

#settings for configurate the render templates html
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def gender_classifier(data):
    X = [[181, 80, 44], [177, 70, 43], [160, 60, 38], [154, 54, 37],
    [166, 65, 40], [190, 90, 47], [175, 64, 39],[177, 70, 40], [159, 55, 37],
    [171, 75, 42], [181, 85, 43]]

    Y = ['Homem', 'Homem', 'Mulher', 'Mulher', 'Homem', 'Homem', 'Mulher', 'Mulher', 'Mulher', 'Homem', 'Homem']

    clf = tree.DecisionTreeClassifier()

    clf = clf.fit(X,Y)

    prediction = clf.predict([[data[0], data[1], data[2]]])

    return prediction

class Gender(webapp2.RequestHandler):
    def get(self):
        t = jinja_env.get_template('home.html')

        self.response.out.write(t.render())

    def post(self):

        #dados no formato json string
        user_inputs_json =  self.request.body
        #conversao do string json para um dicionario
        user_inputs_dict = json.loads(user_inputs_json)

        altura = int(user_inputs_dict['altura'])
        peso = int(user_inputs_dict['peso'])
        pe = int(user_inputs_dict['pe'])

        data = [altura, peso, pe]

        gender = gender_classifier(data)

        t = jinja_env.get_template('home.html')

        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'

        self.response.out.write(json.dumps({'gender':gender[0]}))

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

app = webapp2.WSGIApplication([
    ('/', Gender),
], debug=True)

def main():
    from paste import httpserver
    httpserver.serve(app, host='0.0.0.0', port='8080')

if __name__ == '__main__':
    main()
