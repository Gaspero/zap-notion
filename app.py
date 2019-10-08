import os
import datetime
from notion.client import NotionClient
from notion.collection import NotionDate
from flask import Flask
from flask import request


app = Flask(__name__)


def add_visit(token, clients_url, visits_url, telefon, fio, chto_budem_delat, stoimost, datetime_start, datetime_end):
    client = NotionClient(token)
    clients_collection = client.get_collection_view(clients_url)
    # filter_params = [{
    #     "property": "telefon",
    #     "comparator": "enum_contains",
    #     "value": telefon
    # }]
    # results = clients_collection.build_query(filter=filter_params).execute()
    # if results:
    #     customer = results[0]
    # else:
    #     customer = clients_collection.collection.add_row()
    #     customer.telefon = telefon
    #     customer.fio = fio

    visits_collection = client.get_collection_view(visits_url)
    visit = visits_collection.collection.add_row()
    # visit.klient = customer
    try:
        visit.stoimost = int(stoimost)
    except:
        pass
    visit.chto_budem_delat = chto_budem_delat
    visit.data = NotionDate(start=datetime_start, end=datetime_end)


@app.route('/visit_adder', methods=['GET'])
def visit_adder():
    telefon = request.args.get('telefon')
    fio = request.args.get('fio')
    chto_budem_delat = request.args.get('chto_budem_delat')
    stoimost = request.args.get('stoimost')
    datetime_start = datetime.datetime.strptime(request.args.get('datetime_start'), '%Y-%m-%dT%H:%M:%SZ')
    datetime_end = datetime.datetime.strptime(request.args.get('datetime_end'), '%Y-%m-%dT%H:%M:%SZ')
    token = os.environ.get("TOKEN")
    clients_url = os.environ.get("CLIENTS_URL")
    visits_url = os.environ.get("VISITS_URL")
    add_visit(token, clients_url, visits_url, telefon, fio, chto_budem_delat, stoimost, datetime_start, datetime_end)
    return f'OK'


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
