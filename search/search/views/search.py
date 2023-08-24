"""Implements search interface."""
import flask
from flask import request
import requests
import search


@search.app.route('/', methods=['GET'])
def show_search():
    """Implement search interface."""
    query = request.args.get('q')
    weight = request.args.get('w')
    api_url = search.app.config["INDEX_API_URL"]
    context = {}
    if query and weight:
        data = requests.get(api_url, params={'w': weight, 'q': query}).json()
        docid_list = data["hits"]
        if len(docid_list) > 10:
            docid_list = docid_list[:10]
        connection = search.model.get_db()
        results = []
        for doc_id in docid_list:
            cur = connection.execute(
              "SELECT title, summary FROM Documents WHERE docid = " +
              str(doc_id['docid'])
            )
            results.append(cur.fetchall()[0])
        is_empty = False
        if len(results) == 0:
            is_empty = True
        for result in results:
            if len(result['summary']) == 0:
                result['summary'] = 'No summary available'
                # result.update({'summary' : 'No summary available'})
        context = {'results': results, 'is_empty': is_empty}
    return flask.render_template("search.html", **context)
