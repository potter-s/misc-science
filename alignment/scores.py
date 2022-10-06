class SubstitutionMatrix():
    def __init__(self, match, mismatch, indel):
        self.match = match
        self.mismatch = mismatch
        self.indel = indel
        def base_match():
            return self.match
        def base_mismatch():
            return self.mismatch
        def indel():
            return self.indel
