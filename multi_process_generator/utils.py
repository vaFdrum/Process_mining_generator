import random
from datetime import datetime, timedelta

def sample_handover(handover_range):
    mn, mx = handover_range
    return random.randint(mn, mx)
