import os
from notion.client import NotionClient
from notion.collection import NotionDate
from flask import Flask
from flask import request


app = Flask(__name__)


def add_visit(token, clients_url, visits_url, telefon, fio, chto_budem_delat, stoimost, datetime_start, datetime_end):
    client = NotionClient(token)
    clients_collection = client.get_collection_view(clients_url)
    filter_params = [{
        "property": "telefon",
        "comparator": "enum_contains",
        "value": telefon
    }]
    results = clients_collection.build_query(filter=filter_params).execute()
    if results:
        client = results[0]
    else:
        client = clients_collection.collection.add_row()
        client.telefon = telefon
        client.fio = fio

    visits_collection = client.get_collection_view(visits_url)
    visit = visits_collection.collection.add_row()
    visit.klient = client
    visit.stoimost = stoimost
    visit.chto_budem_delat = chto_budem_delat
    visit.data = NotionDate(start=datetime_start, end=datetime_end)
z

@app.route('/add_visit', methods=['GET'])
def twitter():
    telefon = request.args.get('telefon')
    fio = request.args.get('fio')
    chto_budem_delat = request.args.get('chto_budem_delat')
    stoimost = request.args.get('stoimost')
    datetime_start = request.args.get('datetime_start')
    datetime_end = request.args.get('datetime_end')
    token = os.environ.get("TOKEN")
    clients_url = os.environ.get("CLIENTS_URL")
    visits_url = os.environ.get("VISITS_URL")
    add_visit(token, clients_url, visits_url, telefon, fio, chto_budem_delat, stoimost, datetime_start, datetime_end)
    return f'OK'


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
