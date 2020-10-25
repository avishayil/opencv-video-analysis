var player = document.getElementById('player');
var snapshotCanvas = document.getElementById('snapshot');
var captureButton = document.getElementById('capture');
var trainButton = document.getElementById("train");
var txtName = document.getElementById("name");

$("#player").on("loadeddata", function() {
  snapshotCanvas.setAttribute("height", $('#player').height());
  snapshotCanvas.setAttribute("width", $('#player').width());
});

captureButton.onclick = function() {
    var context = snapshot.getContext('2d');
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);
        }
    }
    xhr.open("POST", "/snapshot");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    context.drawImage(player, 0, 0, snapshotCanvas.width,
        snapshotCanvas.height);
    xhr.send(JSON.stringify({ name: txtName.value, image: context.canvas.toDataURL() }));
};

trainButton.onclick = function() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            alert('Training complete!');
        }
    }
    xhr.open("POST", "/train_model");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send();
};

var handleSuccess = function(stream) {
  // Attach the video stream to the video element and autoplay.
  player.srcObject = stream;
};

navigator.mediaDevices.getUserMedia({video: true})
    .then(handleSuccess);