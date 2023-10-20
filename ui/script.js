document.getElementById("fileInput").addEventListener("change", function() {
    uploadFiles();
});

function uploadFiles() {
    const fileInput = document.getElementById('fileInput');
    const files = fileInput.files;

    if (files.length === 0) {
        alert('Please select a file to upload.');
        return;
    }

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }

    fetch('/api/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        alert('Files uploaded successfully.');
        // Reset the input field after successful upload
        fileInput.value = "";
    })
    .catch(error => {
        console.error('Error uploading files:', error);
        alert('Failed to upload files. See console for more details.');
    });
}
