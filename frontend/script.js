const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("image-input");
const previewImage = document.getElementById("preview-image");
const resultDiv = document.getElementById("result");

// Display the image preview
function showImagePreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewImage.style.display = "block";
    };
    reader.readAsDataURL(file);
}

// Handle file selection
fileInput.onchange = () => {
    const file = fileInput.files[0];
    if (file) {
        showImagePreview(file);
    }
};

// Handle drag-and-drop events
dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.classList.add("highlight");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("highlight");
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("highlight");
    const file = e.dataTransfer.files[0];
    fileInput.files = e.dataTransfer.files;
    if (file) {
        showImagePreview(file);
    }
});

document.getElementById("upload-form").onsubmit = async function (event) {
    event.preventDefault(); // Prevent form submission

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
            resultDiv.innerText = resultText;

            // Send prediction data and image to save on the server
            await fetch("/save_image", {
                method: "POST",
                body: formData.append("prediction", data.prediction).append("confidence", data.accuracy_percentage.toFixed(2))
            });
        } else {
            resultDiv.innerText = "Error: Failed to classify the image.";
        }
    } catch (error) {
        console.error("Error:", error);
        resultDiv.innerText = "Error: Could not classify the image.";
    }

    // Reset file input after submission
    fileInput.value = "";
};
