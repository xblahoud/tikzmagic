'''A Jupyter extension for compiling and displaying images described by the
   TikZ language.'''

import subprocess
import shlex
import shutil
import tempfile
from argparse import ArgumentParser
from base64 import b64encode
from os.path import isfile
from os import getcwd

from IPython.core.magic import register_line_cell_magic
from IPython.core.display import Image

from wand.image import Image as wimage

LATEX_TEMPLATE = r'''
\documentclass[tikz,border={border}]{{standalone}}
\usepackage{{tikz,{latex_pkgs}}}
\usetikzlibrary{{{tikz_libs}}}
{latex_pre}
\begin{{document}}
{content}
\end{{document}}'''

@register_line_cell_magic
def tikz(line, cell=''):
    '''Format TikZ commands into a LaTeX document, compile, and convert.'''
    parser = ArgumentParser()
    parser.add_argument('-p', '--latex_packages', default='')
    parser.add_argument('-x', '--latex_preamble', default='')
    parser.add_argument('-l', '--tikz_libraries', default='')
    parser.add_argument('-i', '--input_file', default=None)
    parser.add_argument('-e', '--export_file', default=None)
    parser.add_argument('-s', '--scale', default=1, type=float)
    parser.add_argument('-b', '--border', default=4)
    parser.add_argument('--engine', default='xelatex')
    parser.add_argument('--wrap', dest='wrap_env', action='store_true')
    parser.add_argument('--no-wrap', dest='wrap_env', action='store_false')
    parser.set_defaults(wrap_env=True)
    parser.add_argument('--debug', dest='debug_mode', action='store_true')
    parser.set_defaults(debug_mode=False)
    args = parser.parse_args(shlex.split(line))

    # prepare latex from template
    if args.input_file:
        # add content from input_file before rest of cell
        cell += r'\input{{{cwd}/{file}}}'.format(cwd=getcwd(),
                                                 file=args.input_file)

    if args.wrap_env:
        cell = r'\begin{tikzpicture}' + cell + r'\end{tikzpicture}'

    latex = LATEX_TEMPLATE.format(content=cell,
                                  border=args.border,
                                  latex_pre=args.latex_preamble,
                                  latex_pkgs=args.latex_packages,
                                  tikz_libs=args.tikz_libraries)

    if args.debug_mode:
        print(latex)

    # add current working directory to any export_file path
    if args.export_file:
        args.export_file = getcwd() + '/' + args.export_file

    # compile and convert, returning Image data
    return latex2image(latex, args.scale, args.export_file, args.engine)


def latex2image(latex, scale=1, export_file=None, engine='xelatex'):
    '''Compile LaTeX to PDF, and convert to PNG.'''
    try:
        # make a temp directory, and name temp files
        temp_dir = tempfile.mkdtemp()
        temp_tex = temp_dir + '/tikzfile.tex'
        temp_pdf = temp_dir + '/tikzfile.pdf'

        open(temp_tex, 'w').write(latex)
        # run LaTeX to generate a PDF
        sh_latex(in_file=temp_tex, out_dir=temp_dir, engine=engine)

        if not isfile(temp_pdf):
            raise Exception(f'{engine} did not produce a PDF file.')

        if export_file:
            shutil.copyfile(temp_pdf, export_file)

        return wimage(filename=temp_pdf, resolution=int(300*scale))

    finally:
        # remove temp directory
        shutil.rmtree(temp_dir)


# functions to run command line scripts
def sh_latex(in_file, out_dir, engine='xelatex'):
    '''Compile XeLaTeX to generate a PDF.'''
    subprocess.call([engine, '-output-directory', out_dir, in_file])


def load_ipython_extension(ipython):
    '''Load iPython extension. Empty as we don't need to do anything.'''
    pass
