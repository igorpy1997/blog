
var post_id
var likeState = {};

    function getCurrentPage() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('page') || 1;
    }

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

async function updatePosts(pageNumber) {
    try {
        // Получаем новый список постов с сервера
         const response = await fetch(`/main/?ajax=true&page=${pageNumber}`); // URL для получения JSON-данных
        if (response.ok) {
            const data = await response.json(); // Получаем JSON-данные
            const posts_t = data.posts
            const numberOfPostsToAdd = posts_t[0].paginate_by;
            // Обновляем содержимое на странице
            const postsContainer = document.querySelector('.posts-container');

            postsContainer.innerHTML = ''; // Очищаем контейнер


            console.log(numberOfPostsToAdd)
            console.log("Hello")


         const maxIndex = Math.min(numberOfPostsToAdd, data.posts.length);
            const numberOfElements = Object.keys(data.posts).length;
            var lim;
            if (numberOfElements < maxIndex*pageNumber){
                lim = numberOfElements;
            }
            else {
                lim = maxIndex*pageNumber;
            }

        for (let i = numberOfPostsToAdd*(pageNumber-1); i < lim; i++) {

            console.log("this is i:", i)

            console.log("Number of elements:", numberOfElements);
            const post = data.posts[i];
            console.log("This is the post", post)
            const postElement = document.createElement('div');
            postElement.classList.add('post', 'card');
            postElement.dataset.postId = post.id;

            const createdAt = document.createElement('div');
            createdAt.classList.add('created-at');
            createdAt.textContent = post.created_at;

            const author = document.createElement('div');
            author.classList.add('author');

            const authorPhotoContainer = document.createElement('div');
            authorPhotoContainer.classList.add('author-photo-container');

            if (post.author.photo_url) {
                const authorPhoto = document.createElement('img');
                authorPhoto.src = post.author.photo_url; // Замените на фактический путь к изображению
                authorPhoto.alt = 'User Icon';
                authorPhoto.classList.add('user-icon');
                authorPhotoContainer.appendChild(authorPhoto);

            }
            author.appendChild(authorPhotoContainer);

            const authorName = document.createElement('span');
            authorName.textContent = post.author.username;

            author.appendChild(authorName);

             const postTitle = document.createElement('h2');
            postTitle.classList.add('card-title');
            postTitle.textContent = post.title; // Добавляем название поста
            console.log(postTitle)

            const descriptionLabel = document.createElement('div');
            descriptionLabel.classList.add('description-label');
            descriptionLabel.textContent = 'description'; // Добавляем метку "description"

            const description = document.createElement('div');
            description.classList.add('description');
            description.textContent = post.description; // Добавляем

            const postPhotoContainer = document.createElement('div');
            postPhotoContainer.classList.add('post-photo-container');


            const postPhoto = document.createElement('img');
            postPhoto.src = post.photo_url; // Замените на фактический путь к изображению поста
            postPhoto.alt = 'Post Photo';
            postPhoto.classList.add('post-photo');


            postPhotoContainer.appendChild(postPhoto);



            const text = document.createElement('div');
            text.classList.add('text');
            text.textContent = post.text;
            text.textContent = post.text.slice(0, post.text.indexOf(' ', 160)) + '...';

            const viewMore = document.createElement('p');
            viewMore.classList.add('view-more');
            viewMore.textContent = 'Click "View" for reading full text';


            const postDetails = document.createElement('div');
            postDetails.classList.add('post-details');



            const likeDiv = document.createElement('div');
            likeDiv.classList.add('likes');

            const likeCount = document.createElement('span');
            likeCount.classList.add('like-count', 'badge', 'badge-pill', 'badge-danger', 'post-likes');
            likeCount.textContent = post.likes_count;

            const likeIcon = document.createElement('i');
            likeIcon.classList.add('like-icon', 'fa', 'fa-heart');
            if (post.is_liked_by_current_user) {
                likeIcon.classList.add('liked');
            }
            likeIcon.title = post.likes_count;

            const commentsDiv = document.createElement('div');
            commentsDiv.classList.add('comments');

            const commentCountBadge = document.createElement('span');
            commentCountBadge.classList.add('badge', 'badge-pill', 'badge-primary');
            commentCountBadge.textContent = post.comment_count;

            const commentIcon = document.createElement('i');
            commentIcon.classList.add('fa', 'fa-comments', 'comment-icon2');

            commentsDiv.appendChild(commentCountBadge);
            commentsDiv.appendChild(commentIcon);


            const editButton = document.createElement('button');
            editButton.classList.add('edit-post-button');
            editButton.id = 'edit-post-button';
            editButton.innerHTML = '<i class="fa fa-edit edit-icon"></i>';


            const deleteButton = document.createElement('button');
            deleteButton.classList.add('delete-post-button');
            deleteButton.id = 'delete-post-button';
            deleteButton.innerHTML = '<i class="fa fa-trash delete-icon"></i>';

            if (post.is_current_user_author) {
                postDetails.appendChild(deleteButton);
                postDetails.appendChild(editButton);
            }

            // Элемент "View"
            const viewLink = document.createElement('a');
            viewLink.href = '#';
            viewLink.classList.add('view-post');
            viewLink.textContent = 'View';

            // Добавляем элементы "Comments" и "View" к postDetails


            const likeUsersList = document.createElement('ul');
            likeUsersList.classList.add('like-users-list');
            likeUsersList.style.display = 'none';



            // Добавьте элементы для комментариев и кнопки "View"

            likeDiv.appendChild(likeCount);
            likeDiv.appendChild(likeIcon);
            likeDiv.appendChild(likeUsersList);

            postDetails.appendChild(likeDiv);
            // Добавьте элементы для комментариев и кнопки "View"

            postElement.appendChild(createdAt);
            postElement.appendChild(author);
            postElement.appendChild(postTitle); // Добавляем название поста

            postElement.appendChild(postPhotoContainer);
            postElement.appendChild(descriptionLabel);
            postElement.appendChild(description);
            postElement.appendChild(document.createElement('hr'));
            postElement.appendChild(text);
            postElement.appendChild(viewMore);
            postElement.appendChild(document.createElement('hr'));
            postElement.appendChild(postDetails);
            postDetails.appendChild(commentsDiv);
            postDetails.appendChild(viewLink);


            // Добавьте postElement в контейнер постов
            const postsContainer = document.getElementById('posts-container');
            postsContainer.appendChild(postElement);
}

    const paginationDiv = document.createElement('div');
    paginationDiv.classList.add('pagination', 'justify-content-center'); // Добавляем классы для стилизации


    if (data.posts[0].is_paginated) {
        const stepLinksSpan = document.createElement('span');
        stepLinksSpan.classList.add('step-links', 'page-link');
        console.log(data.posts[numberOfElements-1].page_obj.has_previous)
        if (data.posts[numberOfElements-1].page_obj.has_previous) {

            const firstPageLink = document.createElement('a');
            firstPageLink.href = `?page=1`;
            firstPageLink.textContent = '\u00AB first';
            firstPageLink.classList.add('page-link'); // Добавляем класс для стилизации
            stepLinksSpan.appendChild(firstPageLink);
            const previousPageLink = document.createElement('a');
            previousPageLink.href = `?page=${pageNumber-1}`;
            previousPageLink.textContent = 'previous';
            previousPageLink.classList.add('page-link'); // Добавляем класс для стилизации
            stepLinksSpan.appendChild(previousPageLink);
        }

        const currentPageSpan = document.createElement('span');
        currentPageSpan.classList.add('page-link', 'current'); // Добавляем классы для стилизации
        currentPageSpan.textContent = `Page ${pageNumber} of ${data.posts[0].page_obj.paginator.num_pages}`;
        stepLinksSpan.appendChild(currentPageSpan);

        if (data.posts[numberOfElements-1].page_obj.has_next) {
            const nextPageLink = document.createElement('a');
            nextPageLink.href = `?page=2`;
            nextPageLink.textContent = 'next';
            nextPageLink.classList.add('page-link'); // Добавляем класс для стилизации

            const lastPageLink = document.createElement('a');
            lastPageLink.href = `?page=${data.posts[0].page_obj.paginator.num_pages}`;
            lastPageLink.textContent = '\u00BB last';
            lastPageLink.classList.add('page-link'); // Добавляем класс для стилизации

            stepLinksSpan.appendChild(nextPageLink);
            stepLinksSpan.appendChild(lastPageLink);
        }

        paginationDiv.appendChild(stepLinksSpan);
        postsContainer.appendChild(paginationDiv);
    }
            } else {
                console.error('Error getting posts:', response.statusText);
            }
        } catch (error) {
            console.error('Fetch error:', error);
        }
}


function submitPost(isPublished) {
    return async function(event) {
        event.preventDefault(); // Отменяем стандартное поведение формы

        var formData = new FormData($('#create-post-form')[0]);
        const url = $('#create-post-form').attr('action');

        formData.append('is_published', isPublished);

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json(); // Парсим JSON-ответ
                if (data.status === 'success') {

                    $('#create-post-form')[0].reset();
                    if(isPublished) {
                        updatePosts(1); // Обновляем список постов на странице
                        const newPage = 1;
                        const newUrl = window.location.pathname + '?page=' + newPage;
                        history.pushState({page: newPage}, "", newUrl);
                        toastr.success('Successful post creating!');
                    }
                    else{
                        toastr.success('Your draft was saved!');
                    }
                }
            } else {
                console.error('Error sending form data:', response.statusText);
            }
        } catch (error) {
            console.error('Fetch error:', error);
        }
    };
}



$(document).ready(function() {


        $.get('/post_create/', function(data) {
            // Добавляем полученное содержимое к элементу с id "main-content"
            $("#posts-form").prepend(data);

        }),


                $(document).on('click', "#draft-published", async function (event) {
        event.preventDefault();
        if (confirm("Are you sure you want to publish this post?")) {
            const formData = new FormData($('#edit-post-form2')[0]);
            formData.append('is_published', '1'); // Set is_published to 1 for publishing

            const url = $('#edit-post-form2').attr('action');
            console.log("Url", url);

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    console.log("DataStatus", data.status);
                    if (data.status === 'success') {
                        // Handle success and update page if needed
                        console.log("Post published successfully.");
                        window.location.reload()
                    }
                } else {
                    console.error('Error sending form data:', response.statusText);
                }
            } catch (error) {
                console.error('Fetch error:', error);
            }
        }
    });

    $(document).on('click', "#draft-saved", async function (event) {
        event.preventDefault();
        if (confirm("Are you sure you want to save this post as a draft?")) {
            const formData = new FormData($('#edit-post-form2')[0]);
            formData.append('is_published', '0'); // Set is_published to 0 for saving as draft

            const url = $('#edit-post-form2').attr('action');
            console.log("Url", url);

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    console.log("DataStatus", data.status);
                    if (data.status === 'success') {
                        // Handle success and update page if needed
                        console.log("Post saved as draft successfully.");
                        window.location.reload()
                        toastr.success("Post saved as draft successfully.");

                    }
                } else {
                    console.error('Error sending form data:', response.statusText);
                }
            } catch (error) {
                console.error('Fetch error:', error);
            }
        }
    });

        $(document).on('click', "#delete-post-button", function() {
            if (confirm("Are you sure you want to delete this post?")) {
        var postId = $(this).closest(".post").data("post-id");

        var csrftoken = getCookie('csrftoken');

        // Добавляем CSRF-токен в заголовки запроса
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });
        $.ajax({
            url: `/delete/${postId}/`,
            type: 'DELETE',
            success: function(response) {
                if (response.status === 'success') {
                    // Успешное удаление, выполните необходимые действия
                    // Например, обновите список постов на странице
                    updatePosts(getCurrentPage());
                     toastr.success('Successful deletion');

                } else {
                    alert(response.message); // Вывод сообщения об ошибке
                }
            },
            error: function(error) {
                console.error('Error deleting post:', error);
            }
        });
    }

        });






            $(document).on('click', "#edit-post-button", function() {

        var modal = $("#ModalWindow");
         var postId = $(this).closest(".post").data("post-id");
        modal.find(".modal-body").empty(); // Очистка контента модального окна
        $.get(`/edit/${postId}/`, function(data) {
                $('#ModalWindow .modal-body').html(data);
                $("#ModalWindow").modal("show");
                $('body').addClass('modal-open');
        });
    });

            $(document).on('click', "#contact-us-button2, #contact-us-button", function(event) {
                event.preventDefault();
                var modal = $("#ModalWindow");
                modal.find(".modal-body").empty(); // Очистка контента модального окна
                $.get(`/contact-us/`, function(data) {
                    $('#ModalWindow .modal-body').html(data);
                    $("#ModalWindow").modal("show");
                    $('body').addClass('modal-open');
                });
            });


            $(document).on('click', "#ContactUsSaveButton", async function(event) {
    event.preventDefault();

    var formData = new FormData($('#contac-us-post-form2')[0]);
    const url = $('#contac-us-post-form2').attr('action');

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            if (data.status === 'success') {
                // Обновляем страницу после успешной отправки
                console.log("zaeballlllllll")
                 const newUrl = new URL(location.href);
                newUrl.searchParams.set('contact_us_success', 'true');
                location.href = newUrl.toString();
            }
        } else {
            console.error('Error sending form data:', response.statusText);
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
});




                        $(document).on('click', "#edit-post-button2", function() {

        var modal = $("#ModalWindow");
         var postId = $(this).closest(".post").data("post-id");
        modal.find(".modal-body").empty(); // Очистка контента модального окна
        $.get(`/draft_post/${postId}/`, function(data) {
                $('#ModalWindow .modal-body').html(data);
                $("#ModalWindow").modal("show");
                $('body').addClass('modal-open');
        });
    });


         $(document).on('click', "#saveChangesEditPost", async function(event){
              event.preventDefault();
              if (confirm("Are you sure?")) {
                  var formData = new FormData($('#edit-post-form')[0])
                  const url = $('#edit-post-form').attr('action');
                  console.log("Url", url)
                  try {
                      const response = await fetch(url, {
                          method: 'POST',
                          body: formData
                      });

                      if (response.ok) {
                          const data = await response.json(); // Парсим JSON-ответ
                          console.log("DataStatus", data.status)
                          if (data.status === 'success') {
                              updatePosts(getCurrentPage()); // Обновляем список постов на странице
                                const newPage = getCurrentPage();
                                const newUrl = window.location.pathname + '?page=' + newPage;
                                history.pushState({ page: newPage }, "", newUrl);

                              $("#ModalWindow").modal("hide");
                              $('body').removeClass('modal-open');
                              toastr.success('Successful edition');

                          }
                      } else {
                          console.error('Error sending form data:', response.statusText);
                      }
                  } catch (error) {
                      console.error('Fetch error:', error);
                  }
              }
    });









       $(document).on('click', "#publish-button", submitPost(true));
$(document).on('click', "#save-as-draft-button", submitPost(false));





$("#posts-container").on("click", ".view-post", function(event) {
    event.preventDefault();

    const postDetails = $(this).closest(".post-details");
    const post = postDetails.closest(".post");
    const postId = post.attr("data-post-id");

    $.ajax({
        url: `/get_post/${postId}/`,
        method: "GET",
        success: function(data) {

                   const modalHeader = `
                <div class="modal-header2">
                    <button type="button" class="close2" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            `;

            // Содержимое модального окна
            const modalContent = `
                <div class="modal-content2">
                    ${modalHeader} <!-- Вставляем заголовок перед содержимым -->
                    <div class="modal-body">
                        ${data} <!-- Содержимое поста -->
                    </div>
                </div>
            `;

            $("#ModalWindow2").html(modalContent);
            $("#ModalWindow2").modal("show");
            $('body').addClass('modal-open');
        },
        error: function(error) {
            console.error("Ошибка при загрузке поста:", error);
        }
    });
});





$(document).on("click", ".comment-icon", function() {
    var post_id = $(this).closest(".post").data("post-id");
    var comment_section = $(this).closest(".post").find(".comment-section");

    if (comment_section.is(":visible")) {
        comment_section.hide();
    } else {
        var currentPage = 1; // Начнем с первой страницы

        function loadComments(page) {
            $.ajax({
                url: '/get_comments/' + post_id + '/',
                data: { page: page }, // Передаем номер страницы на сервер
                type: 'GET',
                dataType: 'json',
                success: function(data) {
                    comment_section.html(data.comments_html);

                    var comment_form = $('<div>').load('/add_comment/' + post_id + '/');
                    comment_form.appendTo(comment_section.find(".Adding"));

                    comment_section.show();

                    // Обновляем кликабельные элементы для пагинации
                    $(".pagination a").click(function(e) {
                        e.preventDefault();
                        var targetPage = $(this).data("page");
                        loadComments(targetPage);
                    });
                },
                error: function() {
                    console.log("Error fetching comments.");
                },
            });
        }

        loadComments(currentPage);
    }
});





    $(document).on('click', '#saveChangesButtonComment', function (event) {
        event.preventDefault();
        var post_id = $(this).closest(".post").data("post-id");
        var form = new FormData($('#add-comment-form')[0]);

        console.log(post_id)
    // Add additional data to formData if needed
        form.append('post_id', post_id);

        $.ajax({
            type: "POST",
            url: $('#add-comment-form').attr('action'),
            data: form,
            processData: false, // Important! Tell jQuery not to process data
            contentType: false,
            dataType: 'json',
            complete: function (data) {
                console.log("Hiiiiiii")
                var newComment = data.new_comment_html;
            $(".comments-list").append(newComment);

            // Очищаем поле ввода комментария или обновляем форму
            $('#add-comment-form')[0].reset();
            toastr.success('Comment sent to moderators');
                $(".comments-list").html(data.comments_html);
                $(".add-comment").html(data.comment_form_html);


            },

        });
    });


function updateLikeStateInAllPages(post_id, liked) {
    // Переберите все элементы на странице с соответствующим post_id и обновите состояние лайка
    $("[data-post-id='" + post_id + "'] .like-icon").toggleClass('liked', liked);
    // Другие обновления на вашем усмотрение
}

  $("#jumbotron").hide().fadeIn(500);

     $(document).on("click", ".like-icon", function() {
         console.log("Likeicon")
        var csrfToken = getCookie('csrftoken');
        var post_id = $(this).closest(".post").data("post-id");
        var like_icon = $(this);
        var like_count_element = $(this).siblings(".like-count");
        console.log("Hiii")

        $.ajax({
            url: '/like/' + post_id + '/',
            type: 'POST',
            data: {
                'post_id': post_id,
            },
            headers: {
                'X-CSRFToken': csrfToken,
            },
            dataType: 'json',
            success: function(data) {
                console.log("data")
                if (data.status === 'added') {
                    like_icon.addClass('liked');
                } else if (data.status === 'removed') {
                    like_icon.removeClass('liked');
                }
                console.log("priv")
                console.log(post_id)
                 $(".post[data-post-id='" + post_id + "'] .post-likes").html(data.likes_count);
                   likeState[post_id] = data.status === 'added';
                   updateLikeStateInAllPages(post_id, likeState[post_id]);
                    var modal = $("#ModalWindow2");

    // Обновляем содержимое модального окна (примерный код, адаптируйте под свою структуру)
                    modal.find(".like-count").html(data.likes_count);
                    modal.find(".like-icon").toggleClass('liked', data.status === 'added');

            },
            error: function (){
                toastr.error("Please login")
            }
        });
    });


/*var lastScrollPosition = 0;
  // Анимация растворения для .jumbotron при прокрутке
$(window).scroll(function() {
  var jumbotron = $("#jumbotron");
  var windowHeight = $(window).height();
  var scrollPosition = $(window).scrollTop();
  var jumbotronOffset = jumbotron.offset().top;

  if (jumbotronOffset < scrollPosition + windowHeight) {
    // Здесь вы можете использовать условие для изменения анимации при скроллинге вниз
    var opacity = 1 - (scrollPosition + windowHeight - jumbotronOffset) / windowHeight;

    if (scrollPosition > lastScrollPosition) {
      // Скроллинг вниз
      jumbotron.css("opacity", opacity);
    } else {
      // Возвращение вверх
      jumbotron.css("opacity", 1); // Отменяем анимацию прозрачности при возвращении вверх
    }

    lastScrollPosition = scrollPosition; // Сохраняем текущую позицию прокрутки для следующего сравнения
  }
});
*/
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

