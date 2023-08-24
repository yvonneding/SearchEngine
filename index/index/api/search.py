"""Implement index server."""
import re
import pathlib
import math
import flask
import index

index_package_dir = pathlib.Path(__file__).parent.parent
inverted_filename = index_package_dir/"inverted_index.txt"
pagerank_filename = index_package_dir/"pagerank.out"
inverted_dict = {}
pagerank_dict = {}


# open inverted_index file in global
with open(inverted_filename, "r") as inverted:
    for line in inverted:
        term_info = {}
        item = line.split('\t')
        each_num = item[1].split()
        j = 1
        term_info['idf'] = each_num[0]
        doc_info = {}
        while j < len(each_num):
            doc_info[each_num[j]] = each_num[j+1] + ' ' + each_num[j+2]
            j += 3
        term_info["doc_info"] = doc_info
        inverted_dict[item[0]] = term_info
# open page_rank file in global
with open(pagerank_filename, "r") as pagerank:
    for line in pagerank:
        item = line.split(',')
        pagerank_dict[item[0]] = float(item[1])


def preprocess(query_list):
    """Help calculate query freq."""
    target = []
    query_freq = {}
    # preprocess the query
    for word in query_list:
        word = re.sub(r'[^a-zA-Z0-9]+', '', word)
        if word:
            target.append(word.lower())
    # remove all stopwords from query
    stopwords_filename = index_package_dir/"stopwords.txt"
    with open(stopwords_filename, "r") as stopwords:
        for each_line in stopwords:
            for eachword in target:
                if eachword == each_line.strip():
                    target.remove(eachword)
    for word in target:
        # calculate term frequency in query
        if word not in query_freq:
            query_freq[word] = 1
        else:
            query_freq[word] += 1
    return query_freq


def get_docid(query_freq):
    """Help get docid."""
    doc_ids = []
    temp = []
    check = 0
    for key in query_freq:
        terminfo = inverted_dict[key]
        if check == 0:
            check = check+1
            for doc_key in terminfo["doc_info"]:
                doc_ids.append(doc_key)
        else:
            for doc_key in terminfo["doc_info"]:
                temp.append(doc_key)
            doc_ids = list(set(doc_ids).intersection(temp))
        temp = []
    return doc_ids


def calc_wscore(weight, doc_id, tfidf):
    """Help calculate weighted score."""
    weighted_score = float(weight) * pagerank_dict[
                    doc_id] + (1-float(weight)) * tfidf
    doc_dict = {}
    doc_dict['docid'] = int(doc_id)
    doc_dict['score'] = weighted_score
    return doc_dict


def get_docvect(query_freq, doc_id):
    """Help get doc vector."""
    d_vec = []
    for key in query_freq:
        # check if the word is in inverted_dict
        if key in inverted_dict:
            d_vec.append(float(inverted_dict[key][
                         "idf"]) * float(inverted_dict[key]["doc_info"][
                                         doc_id].split()[0]))
    return d_vec


def get_normq(query_vector):
    """Help get normq."""
    norm_q = 0
    for value in query_vector:
        norm_q += value**2
    norm_q = math.sqrt(norm_q)
    return norm_q


def get_tfidf(document_vector, query_vector, doc_id, word, norm_q):
    """Help calculate tfidf."""
    #  calculate tfidf
    total = 0.0
    doc_leng = len(document_vector)
    for i in range(doc_leng):
        total += document_vector[i] * query_vector[i]
    tfidf = total / (norm_q * math.sqrt(float(inverted_dict[
            word]["doc_info"][doc_id].split()[1])))
    return tfidf


@index.app.route('/api/v1/', methods=["GET"])
def get_index():
    """Implement index server."""
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)


@index.app.route('/api/v1/hits/', methods=["GET"])
def get_score():
    """Return the results."""
    empty_list = []
    weight = flask.request.args.get('w')
    query = flask.request.args.get('q')
    query_list = query.split('+')
    query_list = query_list[0].split()
    noresult = False
    query_freq = preprocess(query_list)
    # query vector
    q_vec = []
    word = ''
    for key, value in query_freq.items():
        # check if word is in inverted_dict
        if key in inverted_dict:
            q_vec.append(float(inverted_dict[key]['idf']) * value)
        else:
            noresult = True
        word = key

    if not noresult:
        # query norm factor
        norm_q = get_normq(q_vec)
        # find documents that contain all query words
        doc_ids = get_docid(query_freq)
        if len(doc_ids) == 0:
            noresult = True
        if not noresult:
            doc_scores = []
            for doc_id in doc_ids:
                doc_scores.append(calc_wscore(weight, doc_id,
                                  get_tfidf(get_docvect(query_freq, doc_id),
                                            q_vec, doc_id, word, norm_q)))
            doc_scores = sorted(doc_scores, key=lambda i: (-i[
                        'score'], i['docid']))
            context = {
                "hits": doc_scores
            }
            return flask.jsonify(**context)
        context = {
            "hits": empty_list
        }
        return flask.jsonify(**context)
    context = {
        "hits": empty_list
    }
    return flask.jsonify(**context)
