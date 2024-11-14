document.getElementById('drop-zone').addEventListener('click', () => {
    document.getElementById('image-input').click();
});

document.getElementById('image-input').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const imgPreview = document.getElementById('image-preview');
            imgPreview.src = e.target.result;
            imgPreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('upload-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const fileInput = document.getElementById('image-input');
    const file = fileInput.files[0];
    if (!file) {
        document.getElementById('result').textContent = 'Please select an image.';
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('result').textContent = 
                `Prediction: ${data.prediction}, Confidence: ${data.accuracy_percentage.toFixed(2)}%`;
        } else {
            document.getElementById('result').textContent = 'Error: Unable to classify the image.';
        }
    } catch (error) {
        document.getElementById('result').textContent = 'Error: ' + error.message;
    }
});
