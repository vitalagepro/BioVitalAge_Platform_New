
ranges_normali = {
        "Colesterolo Totale": (125, 200),
        "Colesterolo LDL": (0, 100),
        "Colesterolo HDL": (40, 60),
        "Trigliceridi": (0, 150),
        "PCR": (0, 1),
        "NT-proBNP": (0, 125),
        "Omocisteina": (0, 12),
        "Glicemia": (70, 99),
        "Insulina": (2, 25),
        "HOMA Test": (0.5, 2.5),
        "IR Test": (0.5, 2.5),
        "Creatinina": (0.6, 1.3),
        "Stress Ossidativo": (0, 300),
        "Omega Screening": (8, 12),
        "Azotemia": (10, 50),
        "Sodio": (135, 145),
        "Potassio": (3.5, 5.1),
        "Cloruri": (95, 105),
        "Fosforo": (2.5, 4.5),
        "Calcio": (8.5, 10.5),
        "Esame delle Urine": (0, 1),  
        "Transaminasi GOT": (0, 40),
        "Transaminasi GPT": (0, 41),
        "Gamma-GT": (0, 50),
        "Bilirubina Totale": (0.1, 1.2),
        "Bilirubina Diretta": (0, 0.3),
        "Bilirubina Indiretta": (0.2, 1.0),
        "Fosfatasi Alcalina": (30, 120),
        "Albumina": (3.5, 5.2),
        "Proteine Totali": (6, 8.3),
        "Vitamina B12": (200, 900),
        "Vitamina D": (20, 50),
        "DHEA": (70, 495),
        "TSH": (0.4, 4.0),
        "FT3": (2.3, 4.2),
        "FT4": (0.8, 1.8),
        "Omega-3 Index": (8, 12),
        "EPA": (0.5, 2.5),
        "DHA": (2, 5),
        "Stress Ossidativo dROMS": (0, 300),
        "Stress Ossidativo PAT": (0, 300),
        "Stress Ossidativo OSI REDOX": (0, 300),
        "Testosterone": (300, 1000),
        "17B-Estradiolo": (30, 400),
        "Progesterone": (0.1, 25),
        "SHBG": (10, 57),
        "Emocromo": (12, 18),
        "Ferritina": (30, 400),
        "Sideremia": (60, 170),
        "Transferrina": (200, 360),
        "TNF-A": (0, 8),
        "IL-6": (0, 5),
        "IL-10": (0, 10),
    }

# 3. Funzione per normalizzare un valore rispetto al suo range
def normalizza(valore, minimo, massimo):

    if valore < minimo:
        ratio = valore / minimo
    elif valore > massimo:
        ratio = massimo / valore
    else:
        ratio = 1.0
    return max(ratio, 0.0)
    

# 4. Funzione per calcolare lo score di ciascun organo
def calcola_score_organi(valori_esami, organi_esami_pesi):
    punteggi = {}

    for organo, pesi in organi_esami_pesi.items():
        # elenco test effettivamente presenti nei valori e con peso non None
        valid_tests = [
            (test, pesi[test])
            for test in pesi
            if test in valori_esami and pesi[test] is not None
        ]
        # se non c'è nessun test valido, il punteggio è 0
        if not valid_tests:
            punteggi[organo] = 0
            continue

        total_weight = sum(p for _, p in valid_tests)

        # SE total_weight è 0, salta la divisione e metti 0
        if total_weight == 0:
            punteggi[organo] = 0
            continue

        weighted_sum = 0.0
        for test, peso in valid_tests:
            minimo, massimo = ranges_normali[test]
            norm = normalizza(valori_esami[test], minimo, massimo)
            weighted_sum += norm * peso

        # ora total_weight > 0, la divisione è sicura
        fraction = weighted_sum / total_weight
        percent = int(round(fraction * 100))
        punteggi[organo] = max(0, min(100, percent))

    return punteggi



