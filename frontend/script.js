document.getElementById('image-input').addEventListener('change', displayImage);

function displayImage(event) {
    const image = document.getElementById('uploaded-image');
    image.src = URL.createObjectURL(event.target.files[0]);
    image.style.display = 'block';
}

document.getElementById('upload-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const fileInput = document.getElementById('image-input');
    const file = fileInput.files[0];

    if (!file) {
        document.getElementById('result').textContent = "No image selected.";
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    const resultDiv = document.getElementById('result');
    resultDiv.textContent = "Classifying...";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        resultDiv.textContent = `Prediction: ${data.prediction}, Confidence: ${data.accuracy_percentage.toFixed(2)}%`;
    } catch (error) {
        resultDiv.textContent = "Error: Could not classify the image.";
        console.error("Error:", error);
    }
});
