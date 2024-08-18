const sidebar = document.querySelector('.sidebar');
const navToggle = document.querySelector('.nav-toggle');
const closeSidebar = document.querySelector('.close-sidebar');

navToggle.addEventListener('click', () => {
    sidebar.classList.add('open');
    document.body.classList.add('no-scroll');
});

closeSidebar.addEventListener('click', () => {
    sidebar.classList.remove('open');
    document.body.classList.remove('no-scroll');
});


document.querySelectorAll('.category > a i ').forEach(category => {
    category.addEventListener('click', function (event) {
        
        event.preventDefault();

        const subcategories = this.parentElement.nextElementSibling;
        if (subcategories && subcategories.classList.contains('subcategories')) {
            if (subcategories.style.display === 'block') {
                subcategories.style.display = 'none';
                this.parentElement.parentElement.classList.remove('active');
            } else {
                
                subcategories.style.display = 'block';
                this.parentElement.parentElement.classList.add('active');
            }
        }
    });
});


const notSignedInElement = document.querySelector('.not-signed-in');

if (notSignedInElement) {

    const openLoginContainer = notSignedInElement

    const loginContainer = document.querySelector('.login');
    const closeLoginContainer = document.querySelector('.close-login');
    
    
    openLoginContainer.addEventListener('click', () => {
        loginContainer.classList.add('open');
        document.body.classList.add('no-scroll');
    });
    
    closeLoginContainer.addEventListener('click', () => {
        loginContainer.classList.remove('open');
        document.body.classList.remove('no-scroll');
    });
    
    document.addEventListener('click', (e) => {
        if (!loginContainer.contains(e.target) && !openLoginContainer.contains(e.target)) {
            loginContainer.classList.remove('open');
            document.body.classList.remove('no-scroll');
        }
    });
}

