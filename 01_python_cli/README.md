# Python task CLI

A small command-line task manager. It stores tasks in `data.json`, so tasks survive after the program exits.

## Run it

```bash
make setup
make run
```

At the prompt, enter one of these commands:

```text
add Buy milk
list
complete 1
delete 1
exit
```

Run the tests with:

```bash
make test
```

## How it is organized

- `src/main.py` reads commands and calls the task manager.
- `src/taskManager.py` creates, completes, and removes tasks.
- `src/storage.py` reads and writes `data.json`.
- `src/task.py` defines a task with an ID, name, and status.
