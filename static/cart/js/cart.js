quantityInputs = document.querySelectorAll('.quantity-input')

quantityInputs.forEach(input => {
    input.addEventListener('change', function() {
        this.closest('form').submit();
    });
});