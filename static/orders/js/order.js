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



function formatPhoneNumber(value) {
    if (!value) return value;
    const phoneNumber = value.replace(/[^\d]/g, '');
    const phoneNumberLength = phoneNumber.length;
    if (phoneNumberLength < 4) return phoneNumber;
    if (phoneNumberLength < 7) {
        return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3)}`;
    }
 
    return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3, 6)} ${phoneNumber.slice(6, 9)}`
}
function phoneNumberFormatter() {
    const telInput = document.getElementById('phone');
    console.log(telInput)
    const formattedTelInput = formatPhoneNumber(telInput.value);
    telInput.value = formattedTelInput; 
}