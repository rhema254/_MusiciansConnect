//----!-Function to change page to Login page from the LandingPage-!!---
document.addEventListener("DOMContentLoaded", function(){

    var openLoginPage = document.getElementById("Login");

    openLoginPage.addEventListener("click", function(){

        var targetURL="Login.html";
        window.open(targetURL, "_self");
    });

});



//----!-function to show/hide password on LoginPAge and NOT YET ADDED!!!------
function myFunction() {
    var x = document.getElementById("myInput");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }





// ---!!-Add professions Functionality-!!---




//------Js code to handle the profile-picture part------
function handleImageUpload(event) {
  const placeholderImage = document.querySelector('#cert-add-btn');
  const uploadedImage = document.querySelector('.uploaded-image');
  const uploadInput = event.target;

  // Check if a file is selected
  if (uploadInput.files && uploadInput.files[0]) {
    const reader = new FileReader();

    // Display the selected image as the uploaded image
    reader.onload = function (e) {
      uploadedImage.src = e.target.result;
      uploadedImage.style.display = 'block';
      placeholderImage.style.display = 'none';
    };

    // Read the selected file as a data URL
    reader.readAsDataURL(uploadInput.files[0]);
  }
}





//------Js code to handle the Video Adding part------
function handleVideoUpload(event) {
  const placeholderIcon = document.querySelector('.placeholder-icon');
  const uploadedVideo = document.querySelector('.uploaded-video');
  const uploadInput = event.target;

  // Check if a file is selected
  if (uploadInput.files && uploadInput.files[0]) {
    const reader = new FileReader();

    // Display the selected video as the uploaded video
    reader.onload = function (e) {
      uploadedVideo.src = e.target.result;
      uploadedVideo.style.display = 'block';
      placeholderIcon.style.display = 'none';
    };

    // Read the selected file as a data URL
    reader.readAsDataURL(uploadInput.files[0]);
  }
}

function showPopup() {
  document.getElementById("popup").style.display = "block";
  }

  function hidePopup() {
      document.getElementById("popup").style.display = "none";
  }
