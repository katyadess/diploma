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

function HandleFileUpload(fileUploadButton, fileNamesContainer) {
    fileUploadButton.addEventListener('change', function() {
        const fileNames = [];
        const fileLimit = 5;
        const files = this.files;
        
        const fileNamesElement = fileNamesContainer;
    
        if (files.length > fileLimit) {
            fileNamesElement.textContent = `${files.length} files`;
        } else {
            for (let i = 0; i < files.length; i++) {
                fileNames.push(files[i].name);
            }
            fileNamesElement.textContent = fileNames.join(', ');
        }
    });
}

const commentContainer = document.querySelector('.add-comment-container');
const replyContainers = document.querySelectorAll('.reply-comment-container');

const addCommentButton = document.querySelector('.comment-section .add-comment')
const addReplyButtons = document.querySelectorAll('.reply-button');

const closeCommentContainer = document.querySelector('.close-comment');
const closeReplyButtons = document.querySelectorAll('.close-reply');


addCommentButton.addEventListener('click', () => {
    commentContainer.classList.add('open');
    document.body.classList.add('no-scroll');
        
    const fileUploadButton = document.querySelector('.add-comment-container #file-upload');
    const fileNamesContainer = document.querySelector('.add-comment-container #file-names');

    console.log(fileUploadButton, fileUploadButton.parentElement)
    console.log(fileNamesContainer, fileNamesContainer.parentElement)

    HandleFileUpload(fileUploadButton, fileNamesContainer)
});

closeCommentContainer.addEventListener('click', () => {
    commentContainer.classList.remove('open');
    document.body.classList.remove('no-scroll');
});

addReplyButtons.forEach((replyButton, index) => {
    replyButton.addEventListener('click', () => {
        const replyContainer = replyContainers[index]
        replyContainer.classList.add('open');
        document.body.classList.add('no-scroll');

        const fileUploadButton = replyContainer.querySelector('#file-upload');
        const fileNamesContainer = replyContainer.querySelector('#file-names');
        
        HandleFileUpload(fileUploadButton, fileNamesContainer)

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

document.querySelectorAll('.delete-comment-button').forEach(button => {
    button.addEventListener('click', (e) => {
        if (!confirm('Are you sure you want to delete this comment?')) {
            e.preventDefault();
        }
    });
});


toggleRepliesButtons = document.querySelectorAll('.toggle-replies button');
toggleRepliesButtons.forEach(toggleReplyButton => {
    const replies = toggleReplyButton.closest('.toggle-replies').nextElementSibling;
    replies.style.display = 'none'
    console.log(replies)
    toggleReplyButton.addEventListener('click', () => {
        if (replies.style.display === 'none') {
            replies.style.display = 'block';
        } else {
            replies.style.display = 'none';
        }
    });
})