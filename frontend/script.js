document.getElementById('upload-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const fileInput = document.getElementById('image-input');
    const resultDiv = document.getElementById('result');

    if (!fileInput.files.length) {
        resultDiv.textContent = 'No image selected.';
        return;
    }

    const file = fileInput.files[0];
    displayImage(file);

    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (data.error) {
            resultDiv.textContent = `Error: ${data.error}`;
        } else {
            resultDiv.textContent = `Prediction: ${data.prediction}, Confidence: ${data.accuracy_percentage.toFixed(2)}%`;
        }
    } catch (error) {
        resultDiv.textContent = 'An error occurred.';
    }
});

function displayImage(file) {
    const imgPreview = document.getElementById('image-preview');
    const reader = new FileReader();
    reader.onload = function(event) {
        imgPreview.src = event.target.result;
        imgPreview.style.display = 'block';
    };
    reader.readAsDataURL(file);
}
