document.getElementById("start-btn").addEventListener("click", function () {
    fetch("/start_camera", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            if (data.status === "started") {
                document.getElementById("video-stream").innerHTML = `<img src="/video_feed" id="video-feed">`;
            }
        });
});

document.getElementById("stop-btn").addEventListener("click", function () {
    fetch("/stop_camera", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            if (data.status === "stopped") {
                document.getElementById("video-stream").innerHTML = `<div class="video-frame">Nyalakan Kamera</div>`;
            }
        });
});

document.getElementById("capture-btn").addEventListener("click", function () {
    fetch("/capture", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            if (data.status === "saved") {
                let link = document.createElement("a");
                link.href = data.image_url;
                link.download = data.image_url.split('/').pop();
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                alert("Gambar berhasil disimpan!");
            }
        });
});
