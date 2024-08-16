const navLinks = document.querySelectorAll('.sidebar-menu .nav-link');
const subsections = document.querySelectorAll('.sections .sub-section');

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        const targetId = link.getAttribute('data-rel');

        navLinks.forEach(nav => nav.classList.remove('active'));
        subsections.forEach(sub => sub.classList.remove('active'));

        link.classList.add('active');
        document.getElementById(targetId).classList.add('active');

        const url = new URL(window.location.href);
        url.searchParams.delete('show');
        history.replaceState({}, '', url);

    });
});

const editButtons = document.querySelectorAll('#edit-button');

editButtons.forEach(button => {
    button.addEventListener('click', () => {
        const form = button.closest('.edit-address').querySelector('#edit-form');
        
        form.classList.toggle('active')
    });
});

const customSelect = document.querySelector('.custom-select');
const customSelectValue = customSelect.querySelector('.custom-select__value');
const customSelectPopup = customSelect.querySelector('.custom-select__popup');
const customSelectItems = customSelectPopup.querySelectorAll('.custom-select__item');
const hiddenInput = document.getElementById('selected-value');
const chevron = customSelect.querySelector('.bi-chevron-down');

customSelect.addEventListener('click', () => {
    const isPopupVisible = customSelectPopup.classList.toggle('show');
    chevron.classList.toggle('bi-chevron-up', isPopupVisible);
    chevron.classList.toggle('bi-chevron-down', !isPopupVisible);
}); 

customSelectItems.forEach(item => {
    item.addEventListener('click', () => {
        const value = item.getAttribute('data-value');
        customSelectValue.textContent = item.textContent;
        hiddenInput.value = value;
        chevron.classList.remove('bi-chevron-up');
        chevron.classList.add('bi-chevron-down');
    });
    customSelectPopup.classList.remove('show');
});

document.addEventListener('click', (e) => {
    if (!customSelect.contains(e.target)) {
        customSelectPopup.classList.remove('show');
        chevron.classList.remove('bi-chevron-up');
        chevron.classList.add('bi-chevron-down');
    }
});


const toggleOrderContent = document.querySelectorAll('.order-container');

toggleOrderContent.forEach(container => {
    container.addEventListener('click', function() {
        const orderContent = this.closest('.order-item').querySelector('.order-content');
        const totalPrice = this.closest('.order-item').querySelector('.total-price');
        const icon = this.querySelector('i');
        orderContent.classList.toggle('show')



        if (orderContent.classList.contains('show')) {
            totalPrice.classList.add('hidden');
            icon.classList.remove('bi-plus-lg');
            icon.classList.add('bi-dash-lg');
        } else {
            totalPrice.classList.remove('hidden');
            icon.classList.remove('bi-dash-lg');
            icon.classList.add('bi-plus-lg');
        }
    })
})


const backToTopButton = document.getElementById('back-to-top');


window.addEventListener('scroll', function() {
    if (window.scrollY > 300) {
        backToTopButton.style.display = 'block';
    } else {
        backToTopButton.style.display = 'none';
    }
});

backToTopButton.addEventListener('click', function() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});


const urlParams = new URLSearchParams(window.location.search);
const showSection = urlParams.get('show');

if (showSection) {
    const targetId = showSection === 'favourites' ? '4' : showSection; // Adjust this if needed
    const targetElement = document.getElementById(targetId);

    if (targetElement) {
        navLinks.forEach(nav => nav.classList.remove('active'));
        subsections.forEach(sub => sub.classList.remove('active'));

        document.querySelector(`.sidebar-menu .nav-link[data-rel="${targetId}"]`).classList.add('active');
        targetElement.classList.add('active');
        
        targetElement.scrollIntoView({ behavior: 'smooth' });
    }
}


document.addEventListener('DOMContentLoaded', function () {
    new Cleave('#input-phone', {
        phone: true,
        phoneRegionCode: 'UA',
        delimiter: ' ',
        blocks: [0, 3, 3, 2, 2],
        prefix: '+38 '
    });
});