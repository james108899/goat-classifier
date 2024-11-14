document.getElementById("upload-form").onsubmit = async function(event) {
    event.preventDefault(); // Prevent form submission

    const fileInput = document.getElementById("image-input");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please choose an image file to classify.");
        return;
    }

    const formData = new FormData();
    formData.append("image", file);

    try {
        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            const resultText = `Prediction: ${data.prediction}, Confidence: ${data.accuracy_percentage.toFixed(2)}%`;
            document.getElementById("result").innerText = resultText;
        } else {
            document.getElementById("result").innerText = "Error: Failed to classify the image.";
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("result").innerText = "Error: Could not classify the image.";
    }

    // Reset file input after submission
    fileInput.value = "";
};
