from IPython.core.interactiveshell import InteractiveShell
from IPython.display import display, SVG
from os import remove
from subprocess import check_output, call, SubprocessError
import platform
from shutil import which
from datetime import date

def diagrams(line: str, cell: str):
    if which('diagrams') is None:
        return 'error: diagrams command not installed'

    drivers = {'flowchart', 'dot', 'sequence', 'railroad'}
    line = line.strip()
    if line not in drivers:
        return 'use as: %%diagrams <driver name>, supported drivers are {:s}'.format(str(drivers))

    now = str(date.today())
    src = now + '-src.txt'
    dest = now + '-dest.svg'

    with open(src, 'w') as desc:
        desc.write(cell)

    tokens = ['diagrams', line, src, dest]
    if platform.system().lower() == 'windows':
        tokens[0] = 'diagrams.cmd'
    if platform.system().lower() == 'linux' and (line == 'flowchart' or line == 'sequence'):
        try:
            DISPLAY = check_output(['echo ${DISPLAY}', '-l'], shell=True).decode('utf-8')
        except SubprocessError as e:
            DISPLAY = ''
        
        if DISPLAY == '\n':
            if which('xvfb-run') is None:
                return 'cannot find (virtual) display, contact the server host for this'
            else:    
                tokens.insert(0, 'xvfb-run')

    # cmd = ' '.join(tokens)
    # system(cmd)
    call(tokens)
    
    with open(dest, 'rb') as pic:
        raw = pic.read()
    remove(src)
    remove(dest)
    
    return display(SVG(raw))

def load_ipython_extension(ipython: InteractiveShell):
    ipython.register_magic_function(diagrams, 'cell')
