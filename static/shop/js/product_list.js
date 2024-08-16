const customSelect = document.querySelector('.custom-select');
const customSelectValue = customSelect.querySelector('.custom-select__value');
const customSelectPopup = customSelect.querySelector('.custom-select__popup');
const customSelectItems = customSelectPopup.querySelectorAll('.custom-select__item');


customSelect.addEventListener('click', () => {
    customSelectPopup.classList.toggle('show');
    }); 

customSelectItems.forEach(item => {
    item.addEventListener('click', () => {
        customSelectValue.textContent = item.textContent;
    });
    customSelectPopup.classList.remove('show');
});

document.addEventListener('click', (e) => {
    if (!customSelect.contains(e.target)) {
        customSelectPopup.classList.remove('show');
    }
});



const customFilterValue = document.querySelector('.custom-filter__value');
const priceRange = document.querySelector('.price-range');

customFilterValue.addEventListener('click', () => {
    priceRange.classList.toggle('show');
});

document.addEventListener('click', (e) => {
    if (!customFilterValue.closest('.sort-container').contains(e.target)) {
        priceRange.classList.remove('show');
    }
});
