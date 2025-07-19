document.getElementById("uploadForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    let fileInput = document.getElementById("fileInput");
    let file = fileInput.files[0];

    if (!file) {
        alert("Please upload an image first.");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    try {
        let response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            body: formData
        });

        let result = await response.json();
        
        // Display uploaded image
        let outputImage = document.getElementById("output-image");
        outputImage.src = URL.createObjectURL(file);
        outputImage.style.display = "block";

        // Display predicted digit
        document.getElementById("predicted-digit").textContent = result.digit;

    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong. Check the backend.");
    }
});
