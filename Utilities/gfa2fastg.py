#!/usr/bin/env python
"""This script converts a gfa (Graphical Fragment Assembly) file into a fastg file"""
import sys
import os
path_of_this_script = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(path_of_this_script, ".."))
from Library.seq_parser import *
path_of_this_script = os.path.split(os.path.realpath(__file__))[0]


direction = {'+': True, '-': False}


def read_gfa_as_fastg(gfa_file):
    edges = {}
    count_edge = 0
    for line in open(gfa_file, 'rU'):
        line_split = line.rstrip().split('\t')
        if line_split[0] == 'S':
            count_edge += 1
            seq_len = int(line_split[3].split(':')[-1])
            coverage = round(float(line_split[4].split(':')[-1])/seq_len, 5)
            edges[line_split[1]] = {'name': 'EDGE_'+str(count_edge)+'_length_'+str(seq_len)+'_cov_'+str(coverage),
                                    ('seq', True): line_split[2],
                                    ('seq', False): complementary_seq(line_split[2]),
                                    True: [],
                                    False: []}
        elif line_split[0] == 'L':
            edges[line_split[1]][direction[line_split[2]]].append((line_split[3], direction[line_split[4]]))
            edges[line_split[3]][not direction[line_split[4]]].append((line_split[1], not direction[line_split[2]]))
    fasta_matrix = [[], [], 70]
    for original_edge_name in edges:
        for this_direction in [True, False]:
            if edges[original_edge_name][this_direction]:
                seq_name = edges[original_edge_name]['name']+(not this_direction)*'\''+':'
                list_next_edge = []
                for next_edge, next_direction in edges[original_edge_name][this_direction]:
                    list_next_edge.append(edges[next_edge]['name']+(not next_direction)*'\'')
                seq_name += ','.join(list_next_edge)+';'
            else:
                seq_name = edges[original_edge_name]['name']+(not this_direction)*'\''+';'
            fasta_matrix[0].append(seq_name)
            fasta_matrix[1].append(edges[original_edge_name][('seq', this_direction)])
    return fasta_matrix


def main():
    if len(sys.argv) > 1:
        for i in sys.argv:
            if '-h' in i or 'help' in i:
                print("Usage: gfa2fastg.py *.gfa")
                break
        else:
            for gfa_file in sys.argv[1:]:
                write_fasta(gfa_file + '.fastg', read_gfa_as_fastg(gfa_file), False)
    else:
        if type(2/1) == float:
            gfa_file = input('Please input gfa file:').strip()
        else:
            gfa_file = raw_input('Please input gfa file:').strip()
        if gfa_file.strip():
            write_fasta(gfa_file+'.fastg', read_gfa_as_fastg(gfa_file), False)


if __name__ == '__main__':
    main()


"""Copyright 2016 Jianjun Jin

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License."""