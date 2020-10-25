var player = document.getElementById('player');
var snapshotCanvas = document.getElementById('snapshot');
var captureButton = document.getElementById('capture');
var identifiedName = document.getElementById('identified');

$("#player").on("loadeddata", function() {
    snapshotCanvas.setAttribute("height", $('#player').height());
    snapshotCanvas.setAttribute("width", $('#player').width());
  });  

captureButton.onclick = function() {
    var context = snapshot.getContext('2d');
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            identifiedName.innerHTML = JSON.parse(xhr.responseText).response;
        }
    }
    xhr.open("POST", "/analyze_photo_data_url");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    context.drawImage(player, 0, 0, snapshotCanvas.width,
        snapshotCanvas.height);
    xhr.send(JSON.stringify({ image: context.canvas.toDataURL() }));
};

var handleSuccess = function(stream) {
  // Attach the video stream to the video element and autoplay.
  player.srcObject = stream;
};

navigator.mediaDevices.getUserMedia({video: true})
    .then(handleSuccess);