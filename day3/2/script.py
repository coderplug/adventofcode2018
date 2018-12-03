def input(filename):
    with open(filename, "r", encoding="utf-8") as f_in:
        lines = f_in.read().splitlines()
        return lines

def parse_claims(lines):
    claims = []
    for line in lines:
        claim = parse_claim(line)
        claims.append(claim)
    return claims

def parse_claim(line):
    parts = line.split(' ')

    fabric_type = parts[0][0]

    id_list = parts[0][1:]
    id = ''.join(id_list)

    (left_margin_str, top_margin_str) = parts[2].split(',')
    left_margin = int(left_margin_str)
    top_margin = int(top_margin_str[:-1])

    (width_str, height_str) = parts[3].split('x')
    width = int(width_str)
    height = int(height_str)

    return Claim(fabric_type, id, left_margin,
    top_margin, width, height)

class Claim:
    def __init__(self, fabric_type, id, left_margin, 
        top_margin, width, height):
        self.fabric_type = fabric_type
        self.id = id
        self.left_margin = left_margin
        self.top_margin = top_margin
        self.width = width
        self.height = height

    #List calls repr instead of str
    def __repr__(self):
        return "{}{} @ {},{}: {}x{}".format(self.fabric_type, self.id, self.left_margin, self.top_margin, self.width, self.height)

    def __str__(self):
        return "{}{} @ {},{}: {}x{}".format(self.fabric_type, self.id, self.left_margin, self.top_margin, self.width, self.height)

def fill_map(claims):
    claim_map = [[0] * 1000 for i in range(1000)]
    temp = claim_map[0][0]
    for claim in claims:
        for i in range(claim.left_margin, claim.left_margin + claim.width):
            for j in range(claim.top_margin, claim.top_margin + claim.height):
                claim_map[i][j] += 1
    return claim_map

def find_non_overlapping_claim(claims, claim_map):
    for claim in claims:
        if is_claim_non_overlapping(claim, claim_map):
            return claim

def is_claim_non_overlapping(claim, claim_map):
    for i in range(claim.left_margin, claim.left_margin + claim.width):
        for j in range(claim.top_margin, claim.top_margin + claim.height):
            if claim_map[i][j] != 1:
                return False
    return True

def output(filename, text):
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write(text)

def main():
    lines = input("input.txt")
    claims = parse_claims(lines)
    claim_map = fill_map(claims)
    non_overlapping_claim = find_non_overlapping_claim(claims, claim_map)
    non_overlapping_claim_id = non_overlapping_claim.id
    output("output.txt", non_overlapping_claim_id)

main()