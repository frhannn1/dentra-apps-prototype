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
  
      const classList = data.detection_result.data.map(item => item.class);
      document.getElementById("detection-result").textContent = classList.join(", ");
      // // Misal ini hasil dari server (kalau bukan array, kita split berdasarkan nomor manual)
        // document.getElementById("detection-result").textContent = JSON.stringify(data);
     
const labelImageBase64 = data.detection_result.label_visualization;
const labelImage = document.getElementById("preview");

if (labelImageBase64 && labelImage) {
  // Tanpa tanda kutip di dalam string base64
  labelImage.src = `data:image/jpeg;base64,${labelImageBase64}`;
  labelImage.style.display = "block";
}


const rawRecommendation = data.recommendation;

// Pisahkan berdasarkan nomor (gunakan regex)
const items = rawRecommendation.split(/\d+\.\s/).filter(Boolean); // filter untuk hilangkan string kosong

// Buat list HTML
let html = "<h3>Rekomendasi Berdasarkan Deteksi Kerusakan Gigi</h3><ol>";
items.forEach(item => {
  html += `<li>${item.trim()}</li>`;
});
html += "</ol>";

document.getElementById("recommendation").innerHTML = html;

  
    } catch (error) {
      alert("Terjadi kesalahan saat memproses gambar.");
      console.error(error);
    }
  });
  