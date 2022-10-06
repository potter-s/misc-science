#!/usr/bin/env python3

from aligner import Aligner
from scores import SubstitutionMatrix

scores = SubstitutionMatrix(1, -1, -1)
#scores = Scoring('ATCG', 'ATACG', matrix)
#scores = Scoring('ATCG', 'ATCG', matrix)
aligner = Aligner('GATTACA', 'CGATTAACGAC', scores)
aligner.run()
#aligner.print_scores()
alignments = aligner.alignments()

print(alignments[0])

