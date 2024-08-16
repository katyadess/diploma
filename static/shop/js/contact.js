document.getElementById('file-upload').addEventListener('change', function() {
    var fileNames = [];
    for (var i = 0; i < this.files.length; i++) {
        fileNames.push(this.files[i].name);
    }
    document.getElementById('file-names').textContent = fileNames.join(', ');
});