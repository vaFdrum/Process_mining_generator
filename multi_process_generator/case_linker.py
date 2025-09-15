import hashlib
from datetime import datetime
import random

class CaseLinker:
    def __init__(self):
        pass

    def link_cases(self, case_ids):
        seed = str(sorted(case_ids)) + str(datetime.utcnow().isoformat()) + str(random.random())
        link_id = hashlib.md5(seed.encode()).hexdigest()[:12]
        return {cid: link_id for cid in case_ids}
