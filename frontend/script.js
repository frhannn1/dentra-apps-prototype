document.getElementById("upload-form").addEventListener("submit", async function (e) {
    e.preventDefault();
  
    const imageInput = document.getElementById("image-input");
    const file = imageInput.files[0];
  
    if (!file) return;
  
    // Tampilkan preview gambar
    const preview = document.getElementById("preview");
    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";
  
    const formData = new FormData();
    formData.append("image", file);
  
    try {
      const response = await fetch("http://localhost:5000/detect", {
        method: "POST",
        body: formData
      });
  
      const data = await response.json();
  
      document.getElementById("detection-result").textContent = JSON.stringify(data);
      document.getElementById("recommendation").textContent = data.recommendation;
  
    } catch (error) {
      alert("Terjadi kesalahan saat memproses gambar.");
      console.error(error);
    }
  });
  