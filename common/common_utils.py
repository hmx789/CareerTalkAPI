from sqlalchemy.sql import text


def run_script(filename, conn):
    with open(filename, 'r') as f:
        sql_file = f.read()
    sql_commands = sql_file.split(';')

    for command in sql_commands:
        if command != '\n':
            new_string = command.strip()
            print(new_string)
            conn.execute(text(new_string))
