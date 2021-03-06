# Godot Q&A API generator

Generates a static REST API that returns the 10 most popular questions for
predefined tags.

This API integrates with the `godot_questions_answers` Sphinx extension which
acts as a frontend.

The list of tags to search for is specified in [`tags.conf`](/tags.conf).

## Installation

### With Docker

Python dependencies are installed automatically when building the container.
Use one of the commands below depending on your use case (development or production):

#### Development

```bash
docker-compose up
```

A local web server will be hosted at `http://localhost:8080`
(example URL: `http://localhost:8080/animation.json`).
Generated JSON files will also be available in `output/` for inspection.

#### Production

```bash
docker-compose -f docker-compose.yml up
```

No local web server will be hosted. Instead, a web server on the same system is
expected to be used to serve the JSON API files. Files will be stored in the
`api-files` Docker volume and won't be available in `output/` for inspection.

### Without Docker

- Install [Python](https://python.org) 3.7 or later.
- Open a terminal, `cd` to the cloned repository and run
  `pip3 install --user -r requirements.txt`.
  - You can also use a Python virtualenv to scope the package installation to
    the application. In this case, remove `--user` from the above command.
- In the terminal, run `./main.py` to fetch questions and save them to JSON files
  in the `output/` folder.
- Using any web server, make the files in `output/` publicly accessible with
  the `Access-Control-Allow-Origin: *` header to allow cross-origin resource
  sharing (CORS). Otherwise, the documentation website won't be allowed to fetch
  the JSON files as they'll be hosted on a different origin.

### Update the API data periodically

In a production environment, you'll want to make sure the API remains up-to-date.
You can skip this step during development.

Set up a cron job to run `main.py` at regular intervals. The crontab line
below will update the JSON files every day at midnight:

```cron
0 0 * * * /path/to/godot-qa-api-generator/main.py
```

Alternatively, you can set up a systemd timer to run `main.py` at regular intervals.

## Python version compatibility

The production code runs on Python 3.7, so make sure not to use features that
only run on more recent Python versions.

## License

Copyright © 2020-2021 Hugo Locurcio and contributors

Unless otherwise specified, files in this repository are licensed under
the MIT license. See [LICENSE.md](LICENSE.md) for more information.
