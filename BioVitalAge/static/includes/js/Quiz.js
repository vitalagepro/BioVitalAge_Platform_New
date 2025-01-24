const questionsContainer = document.getElementById('quiz-container');
const questions = questionsContainer.querySelectorAll('.question');
const nextBtn = document.getElementById('next-btn');
const prevBtn = document.getElementById('prev-btn');

let currentQuestionIndex = 0;


function nextAnswer() {
    questions[currentQuestionIndex].classList.remove('active');
    
    currentQuestionIndex++;
    if (currentQuestionIndex >= questions.length) {
        currentQuestionIndex = questions.length - 1; 
    }
    
 
    questions[currentQuestionIndex].classList.add('active');
}

function prevAnswer() {
    questions[currentQuestionIndex].classList.remove('active');
    
    currentQuestionIndex--;
    if (currentQuestionIndex < 0) {
        currentQuestionIndex = 0; 
    }
    questions[currentQuestionIndex].classList.add('active');
}


nextBtn.addEventListener('click', nextAnswer);
prevBtn.addEventListener('click', prevAnswer);