const userImg = document.getElementById('userImg');
const userModal = document.getElementById('userModal');
const userModalBtn = document.getElementById('nav-bar-user-modal-btn');

function showModal(){
    userModal.style.display = 'block';
}

userImg.addEventListener('mouseover', showModal);

userModal.addEventListener('mouseout', () => {
    userModal.style.display = 'none';
});

userModalBtn.addEventListener('mouseover', showModal)





// Access to :root style css
const rootStyles = getComputedStyle(document.documentElement);

// Access to color in the :root
const bgColorDark = rootStyles.getPropertyValue('--bg-color-dark').trim();
const bgColorLight = rootStyles.getPropertyValue('--bg-color-light').trim();
const titleColorDarkLighter = rootStyles.getPropertyValue('--title-color-dark-lighter').trim();
const titleColorDark = rootStyles.getPropertyValue('--title-color-dark').trim();
const titleColorLight = rootStyles.getPropertyValue('--title-color-light').trim();

const darkColor = rootStyles.getPropertyValue('--dark-color').trim();
const lighterTwoColor = rootStyles.getPropertyValue('--lighter-two-color').trim();
const lighterOneColor = rootStyles.getPropertyValue('--lighter-one-color').trim();
const lightColor = rootStyles.getPropertyValue('--light-color').trim();
const mindColor = rootStyles.getPropertyValue('--mind-color').trim();



/* Fill the clock based in % function */
function updateKidneyClock(){
    const kidneyClock = document.getElementById('kidneyClock');
    const kidneyPercentage = document.getElementById('kidneyPercentage');
    
    const percentage = 57;
    const angle = (percentage / 100) * 360;

    kidneyClock.style.background = `conic-gradient(${darkColor} ${angle}deg, #e0e0e0 ${angle}deg)`;

    kidneyPercentage.textContent = `${percentage}%`;
    kidneyPercentage.style.color = darkColor;
}
function updateLipidClock(){
    const lipidClock = document.getElementById('lipidClock');
    const lipidPercentage = document.getElementById('lipidPercentage');
   
    const percentage = 33;
    const angle = (percentage / 100) * 360;

    lipidClock.style.background = `conic-gradient(${bgColorDark} ${angle}deg, #e0e0e0 ${angle}deg)`;

    lipidPercentage.textContent = `${percentage}%`;
    lipidPercentage.style.color = bgColorDark;
}
function updateLiverClock(){
    const liverClock = document.getElementById('liverClock');
    const liverPercentage = document.getElementById('liverPercentage');
   
    const percentage = 73;
    const angle = (percentage / 100) * 360;

    liverClock.style.background = `conic-gradient(${lighterTwoColor} ${angle}deg, #e0e0e0 ${angle}deg)`;

    liverPercentage.textContent = `${percentage}%`;
    liverPercentage.style.color = lighterTwoColor;
}
function updateGlucoseClock(){
    const glucoseClock = document.getElementById('glucoseClock');
    const glucosePercentage = document.getElementById('glucosePercentage');
   
    const percentage = 15;
    const angle = (percentage / 100) * 360;

    glucoseClock.style.background = `conic-gradient(${lightColor} ${angle}deg, #e0e0e0 ${angle}deg)`;

    glucosePercentage.textContent = `${percentage}%`;
    glucosePercentage.style.color = lightColor;
}

updateKidneyClock()
updateLipidClock()
updateLiverClock()
updateGlucoseClock()