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

const urlParams = new URLSearchParams(window.location.search);
const showSection = urlParams.get('show');

if (showSection) {
    
    let targetId;

    if (showSection === 'favourites') {
        targetId = '4'; 
    } else if (showSection === 'orders') {
        targetId = '3';
    }else if (showSection === 'addresses') {
        targetId = '2';
    } else {
        targetId = showSection;
    }
    const targetElement = document.getElementById(targetId);

    if (targetElement) {
        navLinks.forEach(nav => nav.classList.remove('active'));
        subsections.forEach(sub => sub.classList.remove('active'));

        document.querySelector(`.sidebar-menu .nav-link[data-rel="${targetId}"]`).classList.add('active');
        targetElement.classList.add('active');
        
        targetElement.scrollIntoView({ behavior: 'smooth' });
    }
}

document.querySelectorAll('.delete-button').forEach(button => {
    button.addEventListener('click', (e) => {
        if (!confirm('Are you sure you want to delete this address?')) {
            e.preventDefault();
        }
    })
})