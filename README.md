# Pets Workshop — Training Sandbox

> ⚠️ **This is a training sandbox, not production code.** It is used for live GitHub Copilot demos and deliberately contains bugs, insecure code and synthetic data. Do not deploy it or reuse its code.

A small website for a fictional dog shelter: a [Flask](https://flask.palletsprojects.com/) + [SQLAlchemy](https://www.sqlalchemy.org/) backend and an [Astro](https://astro.build/) + [Tailwind CSS](https://tailwindcss.com/) frontend.

## Run the server

```bash
cd app/server
pip install -r requirements.txt
python utils/seed_database.py   # create and seed the local SQLite database
python app.py                   # serves on http://localhost:5100
```

## Run the client

```bash
cd app/client
npm install
npm run dev                     # serves on http://localhost:4321
```

## Run the tests

```bash
# Server unit tests
python -m pytest app/server/test_app.py

# Client end-to-end tests
cd app/client && npm run test:e2e
```

## License

Licensed under the MIT license. See [LICENSE](./LICENSE).
