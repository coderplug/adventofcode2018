def input(filename):
    f = open(filename, "r", encoding="utf-8")
    lines = f.read().splitlines()
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

def count_cells_min(claim_map, count):
    cell_count = 0
    for line in claim_map:
        for cell in line:
            if cell >= count:
                cell_count += 1
    return cell_count

def output(filename, text):
    f = open(filename, "w")
    f.write(text)

def main():
    lines = input("input.txt")
    claims = parse_claims(lines)
    claim_map = fill_map(claims)
    count = count_cells_min(claim_map, 2)
    count_str = str(count)
    output("output.txt", count_str)

main()