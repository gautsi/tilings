# tilings
Experiments with generating tilings https://gautsi.github.io/tilings/

## setup
The front-end of this project is a website built with [jupyter book](https://jupyterbook.org/intro.html) and hosted on github pages. Install jupyter book with
```sh
pip install -U jupyter-book
```
We use the [ghp-import](https://github.com/c-w/ghp-import) package to build and publish the site. Install with
```sh
pip install ghp-import
```
After creating jupyter book configuration (`book/_config.yml`) and table of contents (`book/_toc.yml`) files and building locally with
```sh
jb build book/
```
run
```sh
cd book/
ghp-import -n -p -f _build/html
```

I make the build/publish automatic with commit, I add this a precommit hook to `.git/hooks/pre-commit`:
```sh
jupyter-book clean book/
jupyter-book build book/
ghp-import -n -p -f book/_build/html
```

I use jupytext percent format for notebooks, install with
```sh
pip install jupytext
```
Add to `book/_config.yml`:
```yml
sphinx:
  config:
    nb_custom_formats:
        .py:
            - jupytext.reads
            - fmt: py:percent
```