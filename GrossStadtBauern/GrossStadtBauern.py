def read_wishlist(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    n_zutaten = int(lines[0])
    zutaten = lines[1:1 + n_zutaten]
    n_wuensche = int(lines[1 + n_zutaten])
    wuensche = lines[2 + n_zutaten : 2 + n_zutaten + n_wuensche]

    return n_zutaten, zutaten, n_wuensche, wuensche

n_zutaten, zutaten, n_wuensche, wuensche = read_wishlist(r"BWINF/InformatikWetbewerb/GrossStadtBauern/Inputs/bauern1.txt")

print("Anzahl Zutaten:", n_zutaten)
print("Zutaten:", zutaten)
print("Anzahl Wünsche:", n_wuensche)
print("Wünsche:", wuensche)
