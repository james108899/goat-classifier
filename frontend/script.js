function handleImageUpload(event) {
    const file = event.target.files[0];
    document.getElementById('imageInput').file = file;
}

function submitImage() {
    const file = document.getElementById('imageInput').file;
    if (!file) {
        alert("Please upload an image first!");
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    fetch(' https://goat-classifier-185569743902.us-west2.run.app/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const resultElement = document.getElementById('result');
        if (data.error) {
            resultElement.textContent = `Error: ${data.error}`;
        } else {
            resultElement.textContent = `Prediction: ${data.prediction} (Accuracy: ${data.accuracy_percentage.toFixed(2)}%)`;
        }
    })
    .catch(error => {
        document.getElementById('result').textContent = "An error occurred. Please try again.";
        console.error('Error:', error);
    });
}
