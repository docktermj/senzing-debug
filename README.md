# senzing-debug

1. Clone [senzing-debug](https://github.com/docktermj/senzing-debug) Git repository.

1. Make repository the current working directory.
   Example:

    ```console
    cd senzing-debug
    ```

1. Checkout the branch containing the bug recreation.

    ```console
    git checkout 1-dockter-1
    ```

1. Copy Sqlite database with Senzing schema and configuration.

    ```console
    cp testdata/sqlite/G2C.db /tmp/sqlite/G2C.db
    ```

1. Create python virtual environment.

    ```console
    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install -r requirements.txt
    ```

1. Create Senzing environment.

    ```console
    export SENZING_ENGINE_CONFIGURATION_JSON='
    {
        "PIPELINE": {
            "CONFIGPATH": "/etc/opt/senzing",
            "RESOURCEPATH": "/opt/senzing/er/resources",
            "SUPPORTPATH": "/opt/senzing/data"
        },
        "SQL": {
            "CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"
        }
    }
    '
    ```

    ```console
    export LD_LIBRARY_PATH=/opt/senzing/er/lib
    ```

1. Run program.

    ```console
    ./show_bug.py
    ```
