#!/usr/bin/env python3

from aligner import Aligner
from scores import SubstitutionMatrix

scores = SubstitutionMatrix(1, -1, -1)
aligner = Aligner('GATTACAAGAGA', 'ATTACAAGA', scores, align_type = 'SW', count = 10)
aligner.run()
#aligner.print_scores()
alignments = aligner.alignments()

for i in range(len(alignments)):
    print(alignments[i])
    continue
    score = alignments[i].pop(0)
    t_start = alignments[i].pop(0)
    t_end = alignments[i].pop(0)
    q_start = alignments[i].pop(0)
    q_end = alignments[i].pop(0)
    print(str(i) + ': ' + str(score))
    print('{: 3d} '.format(t_start) + alignments[i][0] + '{: 3d}'.format(t_end))
    print('    ' + alignments[i][1] + '   ')
    print('{: 3d} '.format(q_start) + alignments[i][2] + '{: 3d}'.format(q_end))
