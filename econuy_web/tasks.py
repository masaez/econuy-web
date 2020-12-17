from pathlib import Path
from typing import Union, List

from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy import inspect


def full_update(con: Union[Connection, Engine],
                functions: List, run: int = 0,
                output: List = None) -> List:
    if output is None:
        output = []
    failed = []
    for f in functions:
        print(f"*** RUN: {run} ***")
        try:
            name = f.__name__
            module = f.__module__
        except AttributeError:
            name = f.func.__name__
            module = f.func.__module__
        try:
            print(f"{module}.{name}...")
            output.append(f(update_loc=con, save_loc=con))
            print("SUCCESS")
        except:
            # This exception is intentionally broad.
            # If any function fails, carry on with the next one.
            print("FAIL")
            failed.append(f)
            continue
    if len(failed) > 0 and run < 3:
        run += 1
        full_update(con=con, functions=failed, run=run,
                    output=output)
    return output


def clear_tables(con: Union[Connection, Engine]):
    for table in inspect(con).get_table_names():
        if table.startswith("export_"):
            con.engine.execute(f'DROP TABLE IF EXISTS "{table}"')

    return


def get_project_root() -> Path:
    return Path(__file__).parent
