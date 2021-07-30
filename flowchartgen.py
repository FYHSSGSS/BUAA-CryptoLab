import sys
import os

file = str(sys.argv[1])
dir = '\\'.join(file.split('\\')[:-1])

fin = open(file, "r", encoding="utf-8")
fout = open(dir + '\\tmp.py', "w", encoding="utf-8")
destination =  dir + '\\tmp.py'
fout.write('''from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import Config
from pycallgraph import GlobbingFilter
''')
flag = 0
for line in fin:
    if '__main__' in line:
        flag = 1
        fout.write('''if __name__ == "__main__":
    config = Config()
    config.trace_filter = GlobbingFilter(include=[
        'main',
        'draw_chessboard',
        'draw_chessman',
        'draw_chessboard_with_chessman',
        'choose_save',
        'choose_turn',
        'choose_mode',
        'choose_button',
        'save_chess',
        'load_chess',
        'play_chess',
        'pop_window',
        'tip',
        'get_score',
        'max_score',
        'win',
        'key_control'
    ])
    config.trace_filter = GlobbingFilter(exclude=[
        'pycallgraph.*',
        '*.secret_function',
        'FileFinder.*',
        'ModuleLockManager.*',
        'SourceFilLoader.*'
    ])
    graphviz = GraphvizOutput()
    graphviz.output_file = 'graph.png'
    with PyCallGraph(output=graphviz, config=config):
''')
        continue
    elif flag == 1:
        fout.write('    ' + line)
    else:
        fout.write(line)
# print(destination)
# print('cd ' + dir)
# os.system('cd ' + dir)
print('python ' + destination)
os.system('python ' + destination)