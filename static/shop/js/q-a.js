const navLinks = document.querySelectorAll('.sidebar-menu .nav-link');
const subsections = document.querySelectorAll('.section .sub-section');

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        const targetId = link.getAttribute('data-rel');

        navLinks.forEach(nav => nav.classList.remove('active'));
        subsections.forEach(sub => sub.classList.remove('active'));

        link.classList.add('active');
        document.getElementById(targetId).classList.add('active');
    });
});
