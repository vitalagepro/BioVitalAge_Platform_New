document.querySelectorAll('input[type="range"]').forEach(slider => {
    slider.addEventListener('input', function() {
        const value = (this.value - this.min) / (this.max - this.min) * 100;
        this.style.setProperty('--value', `${value}%`);
    });
});