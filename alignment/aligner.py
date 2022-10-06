class Alignment():

    FORMAT_FULL = 0

    def __init__(self, seq_target, seq_query):
        self.path = []
        self.ftype = None
        self.align_str = []

    def aligned_query(self, s = ''):
        if s:
            self.aligned_query = s
        return self.aligned_query

    def aligned_target(self, s = ''):
        if s:
            self.aligned_target = s
        return self.aligned_target

    def qt_matches(self, s1, s2):
        m = []
        for i in range(len(s1)):
            if s1[i] == s2[i]:
                m.append('|')
            else:
                m.append(' ')
        return ''.join(m)

    def add(self, i, j):
        #self.path.append([i, j])
        self.path[:0] = [[i, j]]

    def format_type(self, ftype):
        self.ftype = ftype

    def __str__(self, ):

        if not self.ftype or self.ftype == FORMAT_FULL:
            self.format_full()
        return '\n'.join(self.format)

    def format_full(self):

        self.format = [
            '{: 3d} '.format(self.target_start) + self.aligned_target + '{: 3d}'.format(self.target_end),
            '    ' + self.aligned_matchstr + '   ',
            '{: 3d} '.format(self.query_start) + self.aligned_query + '{: 3d}'.format(self.query_end)
        ]


class Aligner():
    def __init__(self, seq_target, seq_query, scores, align_type = 'NW', score_threshold = 1, count = 1):
        self.seq_target = seq_target
        self.seq_query = seq_query
        self.scoring_matrix = scores
        self.align_type = align_type
        self.algn = []
        self.score_threshold = score_threshold
        self.count = count
        self.all_scores = []
        self.matrix = []
        self.routes = []

    def run(self):
        self.initialise_matrix()
        self.fill_matrix()
        self.traceback()

    def print_scores(self):
        print('\t\t' + '\t'.join(list(self.seq_query)))
        for i in range(len(self.scores)):
            if i > 0:
                print(self.seq_target[i - 1], end = '\t')
            for j in range(len(self.scores[i])):
                if self.routes[i][j] & 4:
                    print('l', end = '')
                if self.routes[i][j] & 2:
                    print('d', end = '')
                if self.routes[i][j] & 1:
                    print('u', end = '')
                print(' ' + str(self.scores[i][j]) + '\t', end = '')
            print()

    def align_type(self):
        return self.align_type

    def path(self, path = None):
        if path:
            self.path = path
        return self.path

    def add_alignment(self, algn):
        self.algn.append(algn)

    def alignments(self, algn = None):
        if algn:
            self.algn.append(algn)
        return self.algn

    def match(self):
        return self.scoring_matrix.match

    def mismatch(self):
        return self.scoring_matrix.mismatch

    def indel(self):
        return self.scoring_matrix.indel

    def calc_score(self, i, j):
        scores = []
        scores.append(self.scores[i - 1][j] + self.indel())
        if self.seq_target[i - 1] == self.seq_query[j - 1]:
            scores.append(self.scores[i - 1][j - 1] + self.match())
        else:
            scores.append(self.scores[i - 1][j - 1] + self.mismatch())
        scores.append(self.scores[i][j - 1] + self.indel())
        if self.align_type == 'SW':
            scores.append(0)
        max_score = max(scores)
        self.scores[i][j] = max_score

        if scores[0] == max_score:
            self.routes[i][j] |= 1
        if scores[1] == max_score:
            self.routes[i][j] |= 2
        if scores[2] == max_score:
            self.routes[i][j] |= 4

        if self.align_type == 'SW' and self.scores[i][j] > self.score_threshold:
            self.all_scores.append([self.scores[i][j], i, j])

    def initialise_matrix(self):
        self.scores = [ [0] * (len(self.seq_query) + 1) for i in range(len(self.seq_target) + 1) ]
        self.routes = [ [0] * (len(self.seq_query) + 1) for i in range(len(self.seq_target) + 1) ]

    def fill_matrix(self):
        self.scores[0][0] = 0
        if self.align_type == 'NW':
            inc = self.indel()
        else:
            inc = 0
        for j in range(len(self.seq_query)):
            self.scores[0][j + 1] = self.scores[0][j] + inc
        for i in range(len(self.seq_target)):
            self.scores[i + 1][0] = self.scores[i][0] + inc
        for i in range(len(self.seq_target)):
            for j in range(len(self.seq_query)):
                self.calc_score(i + 1, j + 1)

        if self.align_type == 'SW':
            self.all_scores = sorted(self.all_scores, key = lambda x: x[0], reverse = True)

    def traceback(self):
        alignments = []
        if self.align_type == 'NW':
            #alignment = Alignment(self.seq_target, self.seq_query)
            self.algn.append(self.traceback_nw(len(self.seq_target), len(self.seq_query)))
        else:
            while self.all_scores and self.all_scores[0][0] > self.score_threshold and len(self.algn) < self.count:
                score, q_end, t_end = self.all_scores.pop(0)
                self.algn.append(self.traceback_sw(q_end, t_end, score))

    def traceback_nw(self, i, j):

        align_target = []
        align_query = []
        alignment = Alignment(self.seq_target, self.seq_query)

        while True:
            # up
            if not (i or j):
                alignment.target_start = 0
                alignment.target_end = len(self.seq_target)
                alignment.query_start = 0
                alignment.query_end = len(self.seq_query)
                alignment.aligned_target = ''.join(align_target[::-1])
                alignment.aligned_query = ''.join(align_query[::-1])
                alignment.aligned_matchstr = alignment.qt_matches(alignment.aligned_target, alignment.aligned_query)
                alignment.score = self.scores[-1][-1]
                return alignment
          # if self.routes[i][j] == 3 or self.routes[i][j] == 5 or self.routes[i][j] == 6:
          #     print('dupe ' + str(self.routes[i][j]) + ' ' + str(i) + ' ' + str(j))
            if self.routes[i][j] & 1:
                align_target.append(self.seq_target[i - 1])
                align_query.append('-')
                alignment.add(i, j)
                i -= 1
            # diag
            elif self.routes[i][j] & 2:
                align_target.append(self.seq_target[i - 1])
                align_query.append(self.seq_query[j - 1])
                alignment.add(i, j)
                i -= 1
                j -= 1
            # left
            else:
                align_target.append('-')
                align_query.append(self.seq_query[j - 1])
                alignment.add(i, j)
                j -= 1

    def traceback_sw(self, i, j, score):

        alignment = Alignment(self.seq_target, self.seq_query)
        alignment.query_end, alignment.target_end = i, j
        align_target = []
        align_query = []

        alignment.score = score

        while True:
            if self.scores[i][j] == 0:
                alignment.target_start = j
                alignment.query_start = i
                alignment.aligned_target = ''.join(align_target[::-1])
                alignment.aligned_query = ''.join(align_query[::-1])
                alignment.aligned_matchstr = alignment.qt_matches(alignment.aligned_target, alignment.aligned_query)
                return alignment
            # up
          # if self.routes[i][j] == 3 or self.routes[i][j] == 5 or self.routes[i][j] == 6:
          #     print('dupe ' + str(self.routes[i][j]) + ' ' + str(i) + ' ' + str(j))
            if self.routes[i][j] & 1:
                align_target.append(self.seq_target[i - 1])
                align_query.append('-')
                i -= 1
            # diag
            elif self.routes[i][j] & 2:
                align_target.append(self.seq_target[i - 1])
                align_query.append(self.seq_query[j - 1])
                i -= 1
                j -= 1
            # left
            else:
                align_target.append('-')
                align_query.append(self.seq_query[j - 1])
                j -= 1
