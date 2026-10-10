# 🍕 Pizza Machine

A pizza ordering & billing kiosk. The main app is a **Flask web kiosk**; the repository also
contains earlier console and GUI versions of the same idea.

## Which file is which

| File | Type | Description |
|---|---|---|
| `app.py` | **Flask web app (main)** | Web kiosk with live price total and itemised receipt. Routes: `GET /`, `POST /order`. |
| `pizzamachine.py` | Console app | Terminal version of the same order & bill flow. |
| `pizza.py` | Console app | Earliest version — interactive `input()` loop. |
| `compare.py` | Tkinter GUI | Number comparison / random demo. Unrelated to pizza. |
| `function.py` | Tkinter GUI | Math functions demo. Unrelated to pizza. |

## Requirements

- Python 3.10+ (developed and tested on 3.14)
- Flask — see `requirements.txt`

## Run the web kiosk

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

python3 app.py
# then open http://127.0.0.1:5000
```

The console versions need no dependencies:

```sh
python3 pizzamachine.py
```

The Tkinter demos (`compare.py`, `function.py`) need a graphical desktop.

## Prices

| Item | Small | Medium | Large |
|---|---|---|---|
| Pizza | $15 | $20 | $25 |
| Pepperoni topping | $2 | $3 | $3 |
| Extra cheese | $1 | $1 | $1 |
| Pepsi / Iced Tea | $3 | $3 | $3 |

The live total in the browser and the server-side bill use these same figures.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/` | Kiosk order form, the current queue and the live total. |
| `POST` | `/order` | Places an order, appends it to the queue and returns the itemised receipt. Form fields: `size` (`S`/`M`/`L`), `pepperoni` (`Y`), `extra_cheese` (`Y`), `drink` (`pepsi`/`tea`/`none`). |

## Known limitations

- **Orders are held in memory only** (`orders = []`) — restarting the app clears the queue.
- `app.py` ends with `app.run(debug=True, port=5000)`, which is fine for local development but
  must never be exposed publicly: the Werkzeug debugger is an interactive code-execution
  console. For anything reachable by others, serve it with a production WSGI server, e.g.:

  ```sh
  pip install waitress
  waitress-serve --listen=0.0.0.0:5000 app:app
  ```

- There are no automated tests or CI yet.
