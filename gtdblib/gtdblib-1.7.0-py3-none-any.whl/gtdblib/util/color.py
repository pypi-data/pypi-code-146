TABLEAU_10 = ['#4e79a7', '#59a14f', '#9c755f', '#f28e2b', '#edc948', '#bab0ac',
              '#e15759', '#b07aa1', '#76b7b2', '#ff9da7']
TABLEAU_20 = ['#4E79A7', '#A0CBE8', '#F28E2B', '#FFBE7D', '#59A14F', '#8CD17D',
              '#B6992D', '#F1CE63', '#499894', '#86BCB6', '#E15759', '#FF9D9A',
              '#79706E', '#BAB0AC', '#D37295', '#FF9D9A', '#79706E', '#BAB0AC',
              '#D37295', '#FABFD2', '#B07AA1', '#D4A6C8', '#9D7660', '#D7B5A6']


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return "#{:02x}{:02x}{:02x}".format(r, g, b)
