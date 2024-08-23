const navLinks = document.querySelectorAll('.sidebar-menu .nav-link');
const subsections = document.querySelectorAll('.sections .sub-section');

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        const targetId = link.getAttribute('data-rel');

        navLinks.forEach(nav => nav.classList.remove('active'));
        subsections.forEach(sub => sub.classList.remove('active'));

        link.classList.add('active');
        document.getElementById(targetId).classList.add('active');
    });
});

document.querySelectorAll('#file-upload').forEach((el, index) => {

    el.addEventListener('change', function() {
        var fileNames = [];
        var fileLimit = 5;
        var files = this.files;

        var fileNamesElement = document.querySelectorAll('#file-names')[index];
    
        if (files.length > fileLimit) {
            fileNamesElement.textContent = `${files.length} files`;
        } else {
            for (var i = 0; i < files.length; i++) {
                fileNames.push(files[i].name);
            }
            fileNamesElement.textContent = fileNames.join(', ');
        }
    });
});


const commentContainer = document.querySelector('.add-comment-container');
const replyContainers = document.querySelectorAll('.reply-comment-container');

const addCommentButton = document.querySelector('.comment-section .add-comment')
const addReplyButtons = document.querySelectorAll('.reply-button');

const closeCommentContainer = document.querySelector('.close-comment');
const closeReplyButtons = document.querySelectorAll('.close-reply');


addCommentButton.addEventListener('click', () => {
    commentContainer.classList.add('open');
    document.body.classList.add('no-scroll');
});

closeCommentContainer.addEventListener('click', () => {
    commentContainer.classList.remove('open');
    document.body.classList.remove('no-scroll');
});

addReplyButtons.forEach((replyButton, index) => {
    replyButton.addEventListener('click', () => {
        replyContainers[index].classList.add('open');
        document.body.classList.add('no-scroll');
    })
})


closeReplyButtons.forEach((closeReplyButton, index) => {
    closeReplyButton.addEventListener('click', () => {
    replyContainers[index].classList.remove('open');
    document.body.classList.remove('no-scroll');
    
})

})


commentStars = document.querySelectorAll('.comment-rating .bi-star')

commentStars.forEach((star, index) => {
    star.addEventListener('click', () => {

        commentStars.forEach(s => s.classList.remove('bi-star-fill'));
        commentStars.forEach(s => s.classList.add('bi-star'));
        
        commentStars.forEach((s, i) => {
            if (i <= index) {
                s.classList.remove('bi-star');
                s.classList.add('bi-star-fill');
            }
        })
        
    })
})



const imgBtns = document.querySelectorAll('.img-select a');
let imgId = 1;

imgBtns.forEach(imgItem => {
    imgItem.addEventListener('click', (e) => {
        e.preventDefault();
        imgId = imgItem.dataset.id;
        slideImage();
    })
})

function slideImage() {
    const displayWidth = document.querySelector('.img-showcase img:first-child').clientWidth;
    document.querySelector('.img-showcase').style.transform = `translateX(${- (imgId - 1) * displayWidth}px)`;
}

window.addEventListener('resize', slideImage);
