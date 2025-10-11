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
    
def find_choreo(state, bars_left, figures, path, all_solutions):
    if bars_left == 0:
        if state == list(range(16)):
            all_solutions.append(path[:])
        return
    
    if bars_left < 0:
        return 
    
    for fig in figures:
        if fig["takte"] <= bars_left:
            new_state = apply_figure(state, fig["permutation"])
            path.append(fig["name"])

            find_choreo(new_state, bars_left - fig["takte"], figures, path, all_solutions)

            path.pop()

   

def evaluate(all_choreographies, figures):
    """Kriterien:
    Möglichst viele unterschiedliche Figuren   werden eingebaut.
    Möglichst viele Figuren werden eingebaut.
    Möglichst wenige Figuren werden eingebaut.
    Die von allen Tanzenden insgesamt zurückgelegte Strecke soll möglichst groß sein.
    Die von allen Tanzenden insgesamt zurückgelegte Strecke soll möglichst klein sein.
    liste der besten Choreographien zurückgeben
    """
    leaderboard = [None, None, None, None, None]
    max_figure_count = 0
    max_diversity = 0
    min_figure_count = 999
    min_distance = 999
    max_distance = 0
    
    for choreo in all_choreographies:
        # Max Figuren
        if len(choreo) > max_figure_count:
            max_figure_count = len(choreo)
            leaderboard[0] = choreo
        
        # Max Diversität
        if len(set(choreo)) > max_diversity:
            max_diversity = len(set(choreo))
            leaderboard[1] = choreo
        
        # Min Figuren
        if len(choreo) < min_figure_count:
            min_figure_count = len(choreo)
            leaderboard[2] = choreo
        
        # Distanz berechnen
        distance = sum(find_distance(fig, figures) for fig in choreo)
        
        if distance < min_distance:
            min_distance = distance
            leaderboard[3] = choreo
        if distance > max_distance:
            max_distance = distance
            leaderboard[4] = choreo
    
    return leaderboard

def find_distance(figure_name, figures):
    fig_data = next(f for f in figures if f["name"] == figure_name)
    perm = parse_figure(fig_data["permutation"])
    return sum(abs(perm[i] - i) for i in range(len(perm)))
    
        


if __name__ == "__main__":
    lines = readfile("choreos/choreo01.txt")
    length = int(lines[0])
    figure_count = int(lines[1])
    figures = []
    
    for i in range(2, 2 + figure_count):
        parts = lines[i].split()
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
    print("\nFiguren:")
    for fig in figures:
        print(f"  {fig['name']}: {fig['takte']} Takte")
    
    # Suche Choreographie
    print("\nSuche Choreographie...")
    start_state = list(range(16))
    solutions = []
    choreography = find_choreo(start_state, length, figures, [], solutions)
    evaluated_solutions = evaluate(solutions, figures)
    choreography = evaluated_solutions[0] if evaluated_solutions else None
    
    evaluated_solutions = evaluate(solutions, figures)

    if solutions:
        for i, leader in enumerate(evaluated_solutions):
            if leader:
                print(f"\nBeste Choreographie nach Kriterium {i+1}:")
                print(" - ".join(leader))
    else:
        print("Keine Lösung gefunden")