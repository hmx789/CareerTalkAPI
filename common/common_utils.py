from sqlalchemy.sql import text
from flask import make_response, jsonify, request


def run_script(filename, conn):
    with open(filename, 'r') as f:
        sql_file = f.read()
    sql_commands = sql_file.split(';')
    stmts_len = 0
    for command in sql_commands:
        if command != '\n':
            new_string = command.strip()
            print("SQL: ", new_string)
            stmts_len += 1
            conn.execute(text(new_string))

    print("Successfully ran {} statements".format(stmts_len))


def _message_builder(message, code):
    return make_response(jsonify({'message:': message}), code)


def _check_identity_header(headers, key):
    """

    :param rq: Flask request object
    :param key: key_header
    :return:
    """
    try:
        val = headers[key]
    except KeyError:
        return _message_builder("key header is missing", 400)
    return val