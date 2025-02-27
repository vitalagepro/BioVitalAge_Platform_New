const monthLayoutBtn = document.getElementById('monthLayout');
const weekLayoutBtn = document.getElementById('weekLayout');

const headWeek = document.getElementById('week-head');
const weekLayout = document.getElementById('week-layout');

const monthWeek = document.getElementById('month-head');
const monthLayout = document.getElementById('month-layout');

/* RESET FUNCTION */
function resetMonthLayout() {
    monthLayout.style.display = 'grid'; 
    monthWeek.style.display = 'flex';
    document.querySelectorAll('.cella').forEach(cella => {
        cella.style.display = 'block'; 
    });
}

/* SETTING WEEK LAYOUT */
weekLayoutBtn.addEventListener('click', ()=> {
    monthLayoutBtn.classList.remove('active');
    weekLayoutBtn.classList.add('active');

    monthWeek.style.display = 'none';
    monthLayout.style.display = 'none';

    headWeek.style.display = 'block';
    weekLayout.style.display = 'block';
});

/* SETTING MONTH LAYOUT */
monthLayoutBtn.addEventListener('click', ()=> {
    weekLayoutBtn.classList.remove('active');
    monthLayoutBtn.classList.add('active');

    headWeek.style.display = 'none';
    weekLayout.style.display = 'none';

    resetMonthLayout(); 
});
