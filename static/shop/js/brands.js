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