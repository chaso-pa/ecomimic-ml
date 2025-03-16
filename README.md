# Fastapi w/ uv package manager

## setup
### docker setup
```zsh
$ docker build -t fastapi-app
$ docker run -p 8000:80 fastapi-app
```

### development
Assume [uv](https://github.com/astral-sh/uv) installed
$
```zsh
$ uv sync
$ uv run fastapi dev
```
