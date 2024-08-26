quantityInputs = document.querySelectorAll('.quantity-input')

quantityInputs.forEach(input => {
    input.addEventListener('change', function() {
        this.closest('form').submit();
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const addressOptions = document.querySelectorAll('.address-option');
    const addressSelect = document.querySelector('select[name="address"]');
    console.log(addressSelect)

    addressOptions.forEach(option => {
        option.addEventListener('click', function() {
            addressOptions.forEach(opt => opt.classList.remove('selected'));

            option.classList.add('selected');

            const addressId = option.getAttribute('data-address-id');
            addressSelect.value = addressId;
        });
    });
});