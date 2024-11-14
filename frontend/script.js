document.getElementById('upload-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const fileInput = document.getElementById('image-input');
    const file = fileInput.files[0];
    if (!file) {
        alert("Please select an image.");
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const resultDiv = document.getElementById('result');
        const resultData = await response.json();

        if (response.ok) {
            resultDiv.innerText = `Prediction: ${resultData.prediction}\nConfidence: ${resultData.accuracy_percentage.toFixed(2)}%`;
        } else {
            resultDiv.innerText = "Error: Could not classify the image.";
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById('result').innerText = "An error occurred during classification.";
    }
});

document.getElementById('image-input').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const uploadedImage = document.getElementById('uploaded-image');
            uploadedImage.src = e.target.result;
            uploadedImage.style.display = "block";
        };
        reader.readAsDataURL(file);
    }
});
