
def adjust_age_glucose(glucose):
    glucose = float(glucose) if glucose else 0  # Conversione a float
    if 70 <= glucose <= 105:
        return 0  # Range normale
    elif 106 <= glucose <= 140:
        return 2  # Glucosio leggermente elevato
    elif glucose > 140:
        return 5  # Alto rischio
    return 0

def adjust_age_creatinine(creatinine):
    creatinine = float(creatinine) if creatinine else 0
    if 0.5 <= creatinine <= 0.9:
        return 0
    elif creatinine > 0.9:
        return 3
    return 0

def adjust_age_ferritin(ferritin):
    ferritin = float(ferritin) if ferritin else 0
    if 13 <= ferritin <= 150:
        return 0
    elif ferritin > 150:
        return 2
    return 0

def adjust_age_albumin(albumin):
    albumin = float(albumin) if albumin else 0
    if 3.5 <= albumin <= 5.2:
        return 0
    elif albumin < 3.5:
        return 2
    return 0

def adjust_age_protein(protein):
    protein = float(protein) if protein else 0
    if 6.6 <= protein <= 8.7:
        return 0
    elif protein < 6.6:
        return 2
    return 0

def adjust_age_bilirubin(bilirubin):
    bilirubin = float(bilirubin) if bilirubin else 0
    if 0 <= bilirubin <= 1.2:
        return 0
    elif bilirubin > 1.2:
        return 2
    return 0

def adjust_age_uric_acid(uric_acid):
    uric_acid = float(uric_acid) if uric_acid else 0
    if 3.5 <= uric_acid <= 7.2:
        return 0
    elif uric_acid > 7.2:
        return 2
    return 0

def adjust_age_obri(obri_index):
    obri_index = float(obri_index) if obri_index else 0
    if 0.8 <= obri_index <= 1.2:
        return 0
    elif 1.3 <= obri_index <= 1.7:
        return 2
    elif 1.8 <= obri_index <= 2.2:
        return 5
    elif obri_index > 2.2:
        return 10
    return 0

def adjust_age_d_roms(d_roms):
    d_roms = float(d_roms) if d_roms else 0
    if 250 <= d_roms <= 300:
        return 0
    elif 301 <= d_roms <= 320:
        return 1
    elif 321 <= d_roms <= 340:
        return 1
    elif 341 <= d_roms <= 400:
        return 3
    elif d_roms > 400:
        return 6
    return 0

def adjust_age_aa_epa(aa_epa):
    aa_epa = float(aa_epa) if aa_epa else 0
    if 1 <= aa_epa <= 3:
        return 0
    elif 3.1 <= aa_epa <= 15:
        return 2
    elif aa_epa > 15:
        return 4
    return 0

def adjust_age_aa_dha(aa_dha):
    aa_dha = float(aa_dha) if aa_dha else 0
    if 1.6 <= aa_dha <= 3.6:
        return 0
    elif 3.7 <= aa_dha <= 4.3:
        return 2
    elif aa_dha > 4.3:
        return 4
    return 0

def adjust_age_homa(homa_test):
    homa_test = float(homa_test) if homa_test else 0
    if 0.23 <= homa_test <= 2.5:
        return 0
    else:
        return 5

def adjust_age_cardio(cardiovascular_risk):
    cardiovascular_risk = float(cardiovascular_risk) if cardiovascular_risk else 0
    if cardiovascular_risk < 3:
        return 0
    elif 3 <= cardiovascular_risk <= 20:
        return 2
    else:
        return 5

def adjust_age_osi(osi):
    osi = float(osi) if osi else 0
    if 0 <= osi <= 40:
        return 0
    elif 41 <= osi <= 65:
        return 2
    elif 66 <= osi <= 120:
        return 5
    else:
        return 10

def adjust_age_pat(pat):
    pat = float(pat) if pat else 0
    if pat < 1800:
        return 10
    elif 1800 <= pat < 2270:
        return 2
    elif 2270 <= pat < 2800:
        return 0
    else:
        return -5

def adjust_age_exams(exams):
    age_adjustment = 0
    normal_values = {
        'glucose': (70, 105),
        'creatinine': (0.5, 0.9),
        'ferritin': (13, 150),
        'albumin': (3.5, 5.2),
        'protein': (6.6, 8.7),
        'bilirubin': (0, 1.2),
        'uric_acid': (3.5, 7.2),
    }
    for key, value in exams.items():
        value = float(value) if value else 0
        if normal_values.get(key) and not (normal_values[key][0] <= value <= normal_values[key][1]):
            age_adjustment += 1  # Incrementa per ogni valore fuori dal range normale
    return age_adjustment

def calculate_biological_age(chronological_age, obri_index, d_roms, aa_epa, aa_dha, homa_test, cardiovascular_risk, osi, pat, exams):
    """Calcola l'età biologica basata sui biomarcatori forniti."""
    biological_age = chronological_age



    # Aggiustamenti basati sui vari parametri
    biological_age += adjust_age_obri(obri_index)
    biological_age += adjust_age_d_roms(d_roms)
    biological_age += adjust_age_aa_epa(aa_epa)
    biological_age += adjust_age_aa_dha(aa_dha)
    biological_age += adjust_age_homa(homa_test)
    biological_age += adjust_age_cardio(cardiovascular_risk)
    biological_age += adjust_age_osi(osi)
    biological_age += adjust_age_pat(pat)

    # Aggiustamenti basati sugli esami specifici
    biological_age += adjust_age_glucose(exams[0])
    biological_age += adjust_age_creatinine(exams[1])
    biological_age += adjust_age_ferritin(exams[2])
    biological_age += adjust_age_albumin(exams[3])
    biological_age += adjust_age_protein(exams[4])
    biological_age += adjust_age_bilirubin(exams[5])
    biological_age += adjust_age_uric_acid(exams[6])


    return biological_age 
