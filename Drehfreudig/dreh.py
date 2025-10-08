import os

def parse_baum(baum):
    """
    Parst einen Klammerausdruck in eine Baumstruktur.
    Jedes Klammerpaar repräsentiert einen Knoten, leere Klammern () = Blatt.
    """
    def helper(s, i):
        children = []
        while i < len(s):
            if s[i] == '(':
                child, i = helper(s, i + 1)
                children.append(child)
            elif s[i] == ')':
                return children, i + 1
            else:
                i += 1
        return children, i
    tree, _ = helper(baum, 0)
    if len(tree) == 1:
        return tree[0]
    return tree

def berechne_breiten(node):
    """
    Berechnet die Breite eines Knotens = Anzahl seiner Blätter.
    Ein Blatt hat Breite 1, innere Knoten = Summe der Kinderbreiten.
    """
    if not node:  # Blatt
        return 1
    return sum(berechne_breiten(child) for child in node)

def ist_drehfreudig(node):
    """
    Prüft ob ein Baum drehfreudig ist.
    Bedingung: Die Breiten der Kinder müssen symmetrisch sein (palindromisch).
    Dies muss rekursiv für alle Teilbäume gelten.
    """
    if not node:  # Blatt ist immer drehfreudig
        return True
    
    # Berechne Breiten aller Kinder
    kinderbreiten = [berechne_breiten(child) for child in node]
    n = len(kinderbreiten)
    
    # Prüfe Symmetrie: kinderbreiten[i] == kinderbreiten[n-1-i]
    for i in range(n // 2):
        if kinderbreiten[i] != kinderbreiten[n - 1 - i]:
            return False
    
    # Prüfe rekursiv alle Kinder
    for child in node:
        if not ist_drehfreudig(child):
            return False
    
    return True

def verarbeite_datei(filepath):
    """Liest eine Baumdatei und prüft Drehfreudigkeit."""
    with open(filepath, "r", encoding="utf-8") as file:
        tree_str = file.read().strip()
    
    print(f"\n{'='*60}")
    print(f"Datei: {os.path.basename(filepath)}")
    print(f"Eingabe: {tree_str}")
    
    baum = parse_baum(tree_str)
    drehfreudig = ist_drehfreudig(baum)
    
    # Debug-Informationen ausgeben
    if baum:
        kinderbreiten = [berechne_breiten(child) for child in baum]
        print(f"Wurzel hat {len(baum)} Kinder mit Breiten: {kinderbreiten}")
        print(f"Symmetrisch? {kinderbreiten == kinderbreiten[::-1]}")
    
    print(f"Ergebnis: {'DREHFREUDIG ✓' if drehfreudig else 'NICHT DREHFREUDIG ✗'}")
    
    return drehfreudig

# Hauptprogramm
if __name__ == "__main__":
    folder_path = "trees"
    
    # Teste zuerst das Beispiel aus der Aufgabe
    beispiel_baum = "(((()())(()())(()()))((()())(()()))((()()())(()()()))))"
    print("="*60)
    print("TEST: Beispiel aus Abbildung A")
    print(f"Eingabe: {beispiel_baum}")
    baum = parse_baum(beispiel_baum)
    
    # Detaillierte Analyse
    print(f"\nAnalyse der Wurzel:")
    print(f"  Anzahl Kinder: {len(baum)}")
    kinderbreiten = [berechne_breiten(child) for child in baum]
    print(f"  Breiten der Kinder: {kinderbreiten}")
    print(f"  Gespiegelt: {kinderbreiten[::-1]}")
    print(f"  Palindrom? {kinderbreiten == kinderbreiten[::-1]}")
    
    ist_drehf = ist_drehfreudig(baum)
    print(f"\nErgebnis: {'DREHFREUDIG' if ist_drehf else 'NICHT DREHFREUDIG'}")
    
    print("\n" + "="*60)
    
    # Verarbeite Dateien aus Ordner
    if os.path.exists(folder_path):
        dateien = sorted([f for f in os.listdir(folder_path) if f.endswith('.txt')])
        
        if dateien:
            ergebnisse = {}
            for filename in dateien:
                filepath = os.path.join(folder_path, filename)
                try:
                    ist_drehf = verarbeite_datei(filepath)
                    ergebnisse[filename] = ist_drehf
                except Exception as e:
                    print(f"Fehler bei {filename}: {e}")
                    import traceback
                    traceback.print_exc()
                    ergebnisse[filename] = None
            
            # Zusammenfassung
            print(f"\n{'='*60}")
            print("ZUSAMMENFASSUNG ALLER DATEIEN")
            print(f"{'='*60}")
            for filename, ergebnis in ergebnisse.items():
                status = "DREHFREUDIG ✓" if ergebnis else "NICHT DREHFREUDIG ✗" if ergebnis is not None else "FEHLER"
                print(f"{filename:30s} -> {status}")
        else:
            print(f"Keine .txt Dateien in '{folder_path}' gefunden.")
    else:
        print(f"\nOrdner '{folder_path}' nicht gefunden. Nur Beispiel getestet.")