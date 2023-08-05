function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function loginUser() {
    var loginInput = $("#login-input").val();
    var passwordInput = $("#password-input").val();
    var csrfToken = getCookie('csrftoken');

    $.ajax({
        url: '/login/',
        type: 'POST',
        data: {
            'username': loginInput,
            'password': passwordInput,
        },
        headers: {
            'X-CSRFToken': csrfToken,
        },
        dataType: 'json',
        complete: function (data) {
            console.log(data);
            if (data.status === 200) {
                // If successfully authenticated, update the content in the logged-in-section block
                if ( data.responseJSON){
                    $("#error-message").text("Invalid username or password.");
                }
                else {
                    var username = data.username;
                    var htmlContent = '<span id="username">' + username + '</span>';
                    console.log(htmlContent)
                    $("#logged-in-section").html(htmlContent);
                    window.location.reload()
                }

            } else {
                alert('Login failed. Please check your credentials.');
            }
        },

    });
}



$(document).ready(function() {
  // Плавное появление для .jumbotron при загрузке страницы



  $("#jumbotron").hide().fadeIn(1500);

  // Анимация растворения для .jumbotron при прокрутке
  $(window).scroll(function() {
    var jumbotron = $("#jumbotron");
    var windowHeight = $(window).height();
    var scrollPosition = $(window).scrollTop();
    var jumbotronOffset = jumbotron.offset().top;
    if (jumbotronOffset < scrollPosition + windowHeight) {
      jumbotron.css("opacity", 1 - (scrollPosition + windowHeight - jumbotronOffset) / windowHeight);
    }
  });

      $("#login-button").click(function () {
        console.log("Privet")
        loginUser();
    });


});



// Function to change the background image of the .jumbotron div
function changeBackgroundImage(imageUrl) {
  const jumbotron = document.getElementById('image-container');
  jumbotron.style.backgroundImage = `url(${imageUrl})`;

}





// Function to fetch the image filenames using Ajax
function fetchImageFilenames() {
  $.ajax({
    url: '/get_image_filenames/', // Замените на ваш URL для получения списка изображений
    type: 'GET',
    dataType: 'json',
    success: function (data) {
      // Array of image filenames to be rotated
      let imageFilenames = data.image_filenames;

      // Index to keep track of the current image
      let currentIndex = 0;

      // Call the rotateImages function every 4 seconds
      setInterval(function () {
        const imageUrl = '/static/images/' + imageFilenames[currentIndex]; // Замените на путь к вашим изображениям
        changeBackgroundImage(imageUrl);
        currentIndex = (currentIndex + 1) % imageFilenames.length;
      }, 4000);
    },
    error: function () {
      console.log('Failed to fetch image filenames via Ajax. Using predefined filenames.');
      // If the Ajax request fails, fallback to using the predefined imageFilenames
      const imageFilenames = ['image1.jpg', 'image2.jpg', 'image3.jpg'];

      // Index to keep track of the current image
      let currentIndex = 0;

      // Call the rotateImages function every 4 seconds
      setInterval(function () {
        const imageUrl = '/static/images/' + imageFilenames[currentIndex]; // Замените на путь к вашим изображениям
        changeBackgroundImage(imageUrl);
        currentIndex = (currentIndex + 1) % imageFilenames.length;
      }, 4000);
    }

  });

}
function animateRunningBorder() {
  const container = document.getElementById('container');
  container.style.animation = 'rotateBorder 5s linear infinite'; // Применяем анимацию
}

// Вызываем функцию при загрузке страницы




animateRunningBorder();

// Fetch the image filenames using Ajax
fetchImageFilenames();
