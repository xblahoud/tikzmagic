# tikzmagic

A Jupyter extension for compiling and displaying images described by the [TikZ](http://www.texample.net/tikz/) language.

## Requirements

- IPython/Jupyter
- LaTeX distribution in your path
- ImageMagick
- [Wand library](http://docs.wand-py.org/)

## Installation

```pip install git+git://github.com/robjstan/tikzmagic.git```

## Usage

In an iPython notebook cell: `import tikzmagic` or `%load_ext tikzmagic`.

## Optional arguments

- `-p` or `--latex_packages`
- `-x` or `--latex_preamble`
- `-l` or `--tikz_libraries`
- `-i` or `--input_file`
- `-s` or `--scale`, default=1 (corresponding to 300dpi)
- `-b` or `--border`, default=4
- `--engine`, path to LaTeX engine to run, default `xelatex`

## Example

[Example iPython notebook](example.ipynb)
