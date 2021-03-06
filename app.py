"""
Import the web flask framework with extensions
Import project constants
Importing module files to request APIs
"""

from constantes import *
from gmaps import *
from parse import Parsing
from wiki import *
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello():
    return render_template('index.html', TITLE=TITLE, MY_NAME=MY_NAME, DICO_IMAGE=DICO_IMAGE, DICO_LINK=DICO_LINK, RANDOM1=RANDOM1, RANDOM2=RANDOM2, KEY_GMAPS = KEY_GMAPS)


@app.route('/response', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        json = request.get_json()
        # Recover user input
        question = json['question']
        print(question)

        # analyze the question with module parse
        parse = Parsing(phrase=question, nb_letter=4)
        print(parse)
        parse = parse.parser()
        print(parse)

        # Location with Google Maps api
        data_maps = RequestMap(parse)
        data_adress = data_maps.get_adress()
        data_location = data_maps.get_location()
        print(data_location)
        lat = data_location[0]
        lng = data_location[1]
        position = str(lat) + str(lng)
        print(position)

        # we use the coordinates to obtain wikipedia information with its API
        data_wiki = RequestWiki(lat=lat, lng=lng)
        data_wiki.geo_search()
        info_api = data_wiki.get_adress()
        result_wiki = data_wiki.resume(url=info_api[0], id_page=info_api[1])

        # We post new answers with the random module
        random_maps = RANDOM()
        random_wiki = RANDOM2()

        parse = ""

        return jsonify(data_adress=data_adress, lat=lat, lng=lng, position=position, random_maps=random_maps, random_wiki=random_wiki, result_wiki=result_wiki, KEY_GMAPS = KEY_GMAPS)


if __name__ == '__main__':
    app.run(debug=True)
