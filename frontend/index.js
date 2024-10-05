document.getElementById("add-video").addEventListener("click", function () {
  fetch("form.html")
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("modal-form").innerHTML = data;
      document.getElementById("modal-form").style.display = "block";
      document
        .getElementById("closeForm")
        .addEventListener("click", function () {
          document.getElementById("modal-form").style.display = "none";
        });

      document
        .getElementById("main-form")
        .addEventListener("submit", async function (e) {
          e.preventDefault();

          const videoFile = document.getElementById("video").files[0];
          const thumbnailFile = document.getElementById("thumbnail").files[0];

          const formData = new FormData();
          formData.append("title", document.getElementById("title").value);
          formData.append(
            "description",
            document.getElementById("description").value
          );
          formData.append(
            "creationDate",
            document.getElementById("creationDate").value
          );
          formData.append("video", videoFile);
          formData.append("thumbnail", thumbnailFile);

          await fetch("http://localhost:8000/add-video/", {
            method: "POST",
            body: formData,
          });
        });
    });
});
