// Funzione per calcolare il codice fiscale
function calculateCodiceFiscale(name, surname, dob, gender, placeOfBirth) {
    const [year, month, day] = dob.split("-");
    const surnameCode = getSurnameCode(surname);
    const nameCode = getNameCode(name);
    const yearCode = getYearCode(year);
    const monthCode = getMonthCode(month);
    const dayAndGenderCode = getDayAndGenderCode(day, gender);
    const comuneCode = getComuneCode(placeOfBirth);
    const controlCharacter = getControlCharacter(
        surnameCode + nameCode + yearCode + monthCode + dayAndGenderCode + comuneCode
    );

    return surnameCode + nameCode + yearCode + monthCode + dayAndGenderCode + comuneCode + controlCharacter;
}

// Funzioni di supporto per il calcolo del codice fiscale
function getSurnameCode(surname) {
    let consonants = surname.replace(/[aeiou]/gi, '');
    let vowels = surname.replace(/[^aeiou]/gi, '');
    return (consonants + vowels + 'XXX').substring(0, 3).toUpperCase();
}

function getNameCode(name) {
    let consonants = name.replace(/[aeiou]/gi, '');
    if (consonants.length >= 4) {
        return (consonants[0] + consonants[2] + consonants[3]).toUpperCase();
    } else {
        let vowels = name.replace(/[^aeiou]/gi, '');
        return (consonants + vowels + 'XXX').substring(0, 3).toUpperCase();
    }
}

function getYearCode(year) {
    return year.slice(-2);  // Ultime due cifre dell'anno
}

function getMonthCode(month) {
    const monthMap = { "01": "A", "02": "B", "03": "C", "04": "D", "05": "E", "06": "H", "07": "L", "08": "M", "09": "P", "10": "R", "11": "S", "12": "T" };
    return monthMap[month];
}

function getDayAndGenderCode(day, gender) {
    let dayCode = parseInt(day, 10);
    if (gender === "F") {
        dayCode += 40;  // Aggiungi 40 per le donne
    }
    return dayCode.toString().padStart(2, '0');
}

function getComuneCode(placeOfBirth) {
    // Logica di mappatura dei codici del comune
    return "H501";  // Placeholder per Roma, sostituisci con il codice effettivo del comune
}

function getControlCharacter(codiceFiscale) {
    // Implementazione per il carattere di controllo
    return "X";  // Placeholder, implementa la logica effettiva per il carattere di controllo
}

// Aggiornamento automatico del codice fiscale
document.getElementById("age-form").addEventListener("input", function() {
    const name = document.getElementById("name").value;
    const surname = document.getElementById("surname").value;
    const dob = document.getElementById("dob").value;
    const gender = document.getElementById("gender").value;
    const placeOfBirth = document.getElementById("place_of_birth").value;

    if (name && surname && dob && gender && placeOfBirth) {
        const codiceFiscale = calculateCodiceFiscale(name, surname, dob, gender, placeOfBirth);
        document.getElementById("codice_fiscale").value = codiceFiscale;
    }
});