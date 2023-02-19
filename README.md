# dpy-template

template to make [discord.py](https://github.com/Rapptz/discord.py) dev environment with poetry and pre-commit.

some useful GithubActions are contained.

## Installation

clone this repository and run commands below.

installing poetry and pre-commit is needed.

using VSCode is highly recommended.

```bash
  poetry config virtualenvs.in-project true
  poetry install
  pre-commit install
```

## Environment Variables

see `.env.example`.

you need to set these to `.env` if you want to run bot locally or on Docker.

## Run Locally

set Environment Variables in `.env`.

```bash
  python main.py
```

## Run on Docker with docker-compose

set Environment Variables in `.env`.

```bash
  docker compose up
```
