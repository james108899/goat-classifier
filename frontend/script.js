// script.js

document.addEventListener("DOMContentLoaded", function() {
    const uploadForm = document.getElementById("upload-form");
    const imageInput = document.getElementById("image-input");
    const dropArea = document.getElementById("drop-area");
    const imagePreview = document.getElementById("image-preview");
    const resultDiv = document.getElementById("result");

    // Handle form submission
    uploadForm.addEventListener("submit", function(event) {
        event.preventDefault();

        if (imageInput.files.length === 0) {
            resultDiv.textContent = "No image selected.";
            return;
        }

        const file = imageInput.files[0];
        classifyImage(file);
    });

    // Drag and drop functionality
    dropArea.addEventListener("dragover", (event) => {
        event.preventDefault();
        dropArea.classList.add("highlight");
    });

    dropArea.addEventListener("dragleave", () => {
        dropArea.classList.remove("highlight");
    });

    dropArea.addEventListener("drop", (event) => {
        event.preventDefault();
        dropArea.classList.remove("highlight");

        const file = event.dataTransfer.files[0];
        if (file && file.type.startsWith("image/")) {
            imageInput.files = event.dataTransfer.files;
            previewImage(file);
        }
    });

    // Click to open file selector
    dropArea.addEventListener("click", () => {
        imageInput.click();
    });

    // Preview the selected image
    imageInput.addEventListener("change", () => {
        const file = imageInput.files[0];
        if (file) {
            previewImage(file);
        }
    });

    function previewImage(file) {
        const reader = new FileReader();
        reader.onload = (event) => {
            imagePreview.src = event.target.result;
            imagePreview.style.display = "block";
        };
        reader.readAsDataURL(file);
    }

    async function classifyImage(file) {
        const formData = new FormData();
        formData.append("image", file);

        resultDiv.textContent = "Classifying...";

        try {
            const response = await fetch("/predict", {
                method: "POST",
                body: formData,
            });

            const result = await response.json();
            if (response.ok) {
                resultDiv.innerHTML = `<strong>Prediction:</strong> ${result.prediction}<br><strong>Confidence:</strong> ${result.accuracy_percentage.toFixed(2)}%`;
            } else {
                resultDiv.textContent = "Error: " + result.error;
            }
        } catch (error) {
            resultDiv.textContent = "An error occurred while classifying the image.";
            console.error("Error:", error);
        }
    }
});
