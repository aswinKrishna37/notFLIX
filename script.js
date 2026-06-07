window.addEventListener('scroll', () => {
    const h6 = document.querySelector('.container h6');
    if (window.scrollY > 10) {
        h6.style.opacity = '0';
        h6.style.pointerEvents = 'none'; // Prevent interaction
    } else {
        h6.style.opacity = '1';
        h6.style.pointerEvents = 'auto';
    }
});