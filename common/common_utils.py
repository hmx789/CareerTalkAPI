from sqlalchemy.sql import text


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