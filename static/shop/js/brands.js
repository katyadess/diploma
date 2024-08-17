const customSelect = document.querySelector('.custom-select');
const customSelectValue = customSelect.querySelector('.custom-select__value');
const customSelectPopup = customSelect.querySelector('.custom-select__popup');
const customSelectItems = customSelectPopup.querySelectorAll('.custom-select__item');
const sortForm = document.querySelector('.main .form')
const chevron = document.querySelector('.bi-chevron-down')
const sortByInput = sortForm.querySelector('input[name="sort_by"]');

customSelect.addEventListener('click', () => {
    const isPopupVisible = customSelectPopup.classList.toggle('show');
    chevron.classList.toggle('bi-chevron-up', isPopupVisible);
    chevron.classList.toggle('bi-chevron-down', !isPopupVisible);
}); 

customSelectItems.forEach(item => {
    item.addEventListener('click', () => {
        customSelectValue.textContent = item.textContent;
        chevron.classList.remove('bi-chevron-up');
        chevron.classList.add('bi-chevron-down');
        sortByInput.value = item.textContent.toLowerCase().replace(' ', '-'); 
        sortForm.submit()
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