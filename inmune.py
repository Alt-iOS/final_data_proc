import random
from bitarray import bitarray

class Lymphocyte:
    def __init__(self, antibody):
        self.antibody = bitarray(antibody)
        self.search_table = self.build_table()
        self.age = 0
        self.stimulation = 0

    def build_table(self):
        result = [-1, 0] + [0] * (len(self.antibody) - 2)
        pos = 2
        cnd = 0
        while pos < len(self.antibody):
            if self.antibody[pos - 1] == self.antibody[cnd]:
                cnd += 1
                result[pos] = cnd
                pos += 1
            elif cnd > 0:
                cnd = result[cnd]
            else:
                result[pos] = 0
                pos += 1
        return result

    def detects(self, pattern):
        m = 0
        i = 0
        while m + i < len(pattern):
            if self.antibody[i] == pattern[m + i]:
                if i == len(self.antibody) - 1:
                    return True
                i += 1
            else:
                m = m + i - self.search_table[i]
                if self.search_table[i] > -1:
                    i = self.search_table[i]
                else:
                    i = 0
        return False

    def __str__(self):
        antibody_str = ''.join(['1 ' if bit else '0 ' for bit in self.antibody])
        return f"antibody = {antibody_str}age = {self.age} stimulation = {self.stimulation}"

def random_bitarray(num_bits):
    return bitarray([random.choice([False, True]) for _ in range(num_bits)])

def bitarray_as_string(ba):
    return ''.join(['1 ' if bit else '0 ' for bit in ba])

def load_self_set():
    result = []
    self_data = [
        [True, False, False, True, False, True, True, False, True, False, False, True],
        [False, False, True, False, True, False, True, False, False, True, False, False]
    ]
    for data in self_data:
        result.append(bitarray(data))
    return result

def create_lymphocyte_set(self_set, num_antibody_bits, num_lymphocytes):
    result = []
    contents = {}
    while len(result) < num_lymphocytes:
        antibody = random_bitarray(num_antibody_bits)
        lymphocyte = Lymphocyte(antibody)
        hash_code = hash(antibody.tobytes())
        if not any(lymphocyte.detects(self_pattern) for self_pattern in self_set) and hash_code not in contents:
            result.append(lymphocyte)
            contents[hash_code] = True
    return result

def show_set(items):
    for i, item in enumerate(items):
        print(f"{i}: {item}")

def run():
    print("\nBegin Artificial Immune System for Intrusion Detection demo\n")
    random.seed(1)
    num_pattern_bits = 12
    num_antibody_bits = 4
    num_lymphocytes = 3
    stimulation_threshold = 3

    print("Loading self-antigen set ('normal' historical patterns)")
    self_set = load_self_set()
    show_set(self_set)

    print("\nCreating lymphocyte set using negative selection and r-chunks detection")
    lymphocyte_set = create_lymphocyte_set(self_set, num_antibody_bits, num_lymphocytes)
    show_set(lymphocyte_set)

    print("\nBegin AIS intrusion detection simulation\n")
    time = 0
    max_time = 6
    while time < max_time:
        print("============================================")
        incoming = random_bitarray(num_pattern_bits)
        print("Incoming pattern = " + bitarray_as_string(incoming) + "\n")
        for i, lymphocyte in enumerate(lymphocyte_set):
            if lymphocyte.detects(incoming):
                print(f"Incoming pattern detected by lymphocyte {i}")
                lymphocyte.stimulation += 1
                if lymphocyte.stimulation >= stimulation_threshold:
                    print(f"Lymphocyte {i} stimulated! Check incoming as possible intrusion!")
                else:
                    print(f"Lymphocyte {i} not over stimulation threshold")
            else:
                print(f"Incoming pattern not detected by lymphocyte {i}")
        time += 1
        print("============================================")
    print("\nEnd AIS IDS demo\n")
