# aufgabe choreo

"""
Eingabe:

Liste verfügbarer Figuren 
Gesamtlänge des Musikstücks in Takten 

Choreographie finden:

Eine Folge von Figuren zusammenstellen
Die Gesamtlänge muss exakt der Musiklänge entsprechen
Am Ende müssen alle Tänzer wieder an ihrer Startposition stehen (Permutation = Identität)

Ausgabe:

Keine Lösung: Meldung ausgeben
Mehrere Lösungen: Die "beste" Choreographie nach bestimmten Kriterien ausgeben
"""

import os

def readfile(filepath):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, filepath)
    
    with open(full_path, 'r', encoding='utf-8') as datei:
        lines = [line.strip() for line in datei.readlines()]
    return lines

def parse_figure(figure):
    return [ord(char) - ord('A') for char in figure]

def apply_figure(state, figure):
    new_state = [0] * len(state)
    perm = parse_figure(figure)
    for fig in range(len(perm)):
        old_pos = perm[fig]
        new_state[fig] = state[old_pos]
    return new_state

def check_choreo(state, figures, length):
    length_used = 0
    return
    

if __name__ == "__main__":
    lines = readfile("choreos/choreo01.txt")
    length = int(lines[0])
    figure_count = int(lines[1])
    figures = []
    for i in range(2, 2 + figure_count):
        parts = lines[i].split()  # Teile bei Leerzeichen
        name = parts[0]
        takte = int(parts[1])
        permutation = parts[2]
        
        figures.append({
            'name': name,
            'takte': takte,
            'permutation': permutation
        })
    
    print(f"Musiklänge: {length} Takte")
    print(f"Anzahl Figuren: {figure_count}")
    print("Figuren:")
    for fig in figures:
        print(f"  {fig['name']}: {fig['takte']} Takte, {fig['permutation']}")
    
    