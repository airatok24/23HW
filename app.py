import os
import logging

from flask import Flask, request
logging.basicConfig(filename="basic.log", level=logging.DEBUG)
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def construct_query(iter_obj, cmd, value):
    """
    конструктор запроса с применением фильтров и передаваемых в фильтр значений
    :param iter_obj:
    :param cmd:
    :param value:
    :return:
    """
    result = map(lambda x: x.strip(), iter_obj)

    if cmd == "filter":
        result = filter(lambda x: value in x, result)
    if cmd == "map":
        value = int(value)
        result = map(lambda x: x.split(" ")[value], result)
    if cmd == "unique":
        result = set(result)
    if cmd == "sort":
        value = bool(value)
        result = sorted(result, reverse=value)
    if cmd == "limit":
        value = int(value)
        result = list(result)[:value]

    return result


@app.route("/perform_query")
def perform_query():
    try:
        cmd_1 = request.args.get("cmd_1")
        val_1 = request.args.get("val_1")
        cmd_2 = request.args.get("cmd_2")
        val_2 = request.args.get("val_2")
        file_name = request.args.get("file_name")

        if not cmd_1 or not val_1 or not file_name:
            return {"error": "Missing first parameters pair or file name."}, 400

    except:
        print("here is except for 4 params")
        return {"error": "Bad Request. Check your query parameters."}, 400

    # проверяем, что файл file_name существует в нужной папке DATA_DIR
    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return {"error": "Bad Request. File was not found."}, 400

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            result_first = construct_query(f, cmd_1, val_1)
            result_second = construct_query(result_first, cmd_2, val_2)
            result_final = "\n".join(result_second)
    except:
        return {"error": "Problem with reading file or Operation unsuccessful."}, 405


    logging.debug(f"cmd_1: {cmd_1}, val_1: {val_1}, cmd_2: {cmd_2}, val_2: {val_2}, file_name: {file_name}")

    return app.response_class(result_final, content_type="text/plain")


if __name__ == '__main__':
    app.run(debug=True)