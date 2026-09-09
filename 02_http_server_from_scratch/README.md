# HTTP server from scratch

A basic HTTP server built with Python's `socket` module. It accepts one connection at a time, parses the request, routes it, and sends a raw HTTP response.

## Run it

```bash
make server
```

The server listens at `http://127.0.0.1:8080`.

Try these routes in a browser or with `curl`:

```text
GET  /
GET  /users
POST /echo
```

For example:

```bash
curl -X POST http://127.0.0.1:8080/echo -d 'hello'
```

## How it is organized

- `src/browser_server.py` accepts connections and sends responses.
- `src/request.py` parses the request line, headers, and body.
- `src/router.py` matches a method and path to a response.

This is a learning project. It intentionally handles only a small part of HTTP.
