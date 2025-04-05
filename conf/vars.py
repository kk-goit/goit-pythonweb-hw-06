import os
from dotenv import dotenv_values

VARS = {
    **dotenv_values(".env"),
    **os.environ,
}

if "DB_URI" not in VARS:
    VARS["DB_URI"] = (
        f"postgresql+psycopg2://{VARS['DB_USER']}:{VARS['DB_PASS']}@{VARS['DB_HOST']}:{VARS['DB_PORT']}/{VARS['DB_NAME']}"
    )
