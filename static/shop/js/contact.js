document.getElementById('file-upload').addEventListener('change', function() {
    var fileNames = [];
    var fileLimit = 5;
    var files = this.files;

    if (files.length > fileLimit) {
        document.getElementById('file-names').textContent = `${files.length} files`;
    } else {
        for (var i = 0; i < files.length; i++) {
            fileNames.push(files[i].name);
        }
        document.getElementById('file-names').textContent = fileNames.join(', ');
    }
});