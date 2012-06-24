#!/usr/bin/env python
'graph dependencies in projects'
# From https://gist.github.com/2769821
#  https://gist.github.com/BrianHicks
import json
from subprocess import Popen, PIPE
import sys

HEADER = "digraph dependencies {"
FOOTER = "}"

JSON_START = '['
JSON_END = ']'

def call_taskwarrior(cmd):
    'call taskwarrior, returning output and error'
    tw = Popen(['task'] + cmd.split(), stdout=PIPE, stderr=PIPE)
    return tw.communicate()

def get_json(query):
    'call taskwarrior, returning objects from json'
    result, err = call_taskwarrior('export %s' % query)
    return json.loads(JSON_START + result + JSON_END)

def call_dot(instr):
    'call dot, returning stdout and stdout'
    dot = Popen('dot -T png'.split(), stdout=PIPE, stderr=PIPE, stdin=PIPE)
    return dot.communicate(instr)

if __name__ == '__main__':
    query = sys.argv[1:]
    print 'Calling TaskWarrior'
    data = get_json(' '.join(query))

    # first pass: labels
    lines = [HEADER]
    print 'Printing Labels'
    for datum in data:
        lines.append('"%s"[label="%s"];' % (datum['uuid'], datum['description']))

    # second pass: dependencies
    print 'Resolving Dependencies'
    for datum in data:
        for dep in datum.get('depends', '').split(','):
            if dep != '':
                lines.append('"%s" -> "%s";' % (dep, datum['uuid']))

    lines.append(FOOTER)

    print '\n'.join(lines)

    print 'Calling dot'
    png, err = call_dot('\n'.join(lines))
    if err != '':
        print 'Error calling dot:'
        print err.strip()

    print 'Writing to deps.png'
    with open('deps.png', 'w') as f:
        f.write(png)