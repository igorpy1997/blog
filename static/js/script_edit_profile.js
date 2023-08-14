// script_registration.js
$(document).ready(function () {
    // Function to open the registration modal
    var profilePk;
    function openEditionModal(pk) {
        profilePk = pk;
        $.ajax({
            url: '/edit_profile/' + pk + '/', // Update the URL with your registration URL
            type: 'GET',
            dataType: 'html',
            success: function (data) {
                console.log(data)
                $('#ModalWindow .modal-body').html(data);
                $("#ModalWindow").modal("show");
                $('body').addClass('modal-open');

            },
            error: function () {
                console.log('Failed to load updating form.');
            }
        });
    }

    // Attach click event handler to the registration button
    $("#editProfileButton").click(function () {
        console.log("tutaj")
        var pk = $(this).data("pk");
        console.log("pk:", pk); // Check if the data-pk attribute has a valid value
        openEditionModal(pk);
    });

    // Attach click event handler to the "Save changes" button inside the modal
    $(document).on('click', '#saveChangesButton2', function () {
        // Serialize the form data
    var formData = new FormData($('#edit-profile-form')[0]); // Use FormData to get form data with files

    // Add additional data to formData if needed
    formData.append('pk', profilePk);

    // Submit the form data via AJAX
    $.ajax({
        url: $('#edit-profile-form').attr('action'),
        type: 'POST',
        data: formData,
        processData: false, // Important! Tell jQuery not to process data
        contentType: false,
        dataType: 'json',
        complete: function (data) {
            console.log(data.status)
            if (data.status === 200) {
                // Обработка успешного ответа
                alert("Profile updated successfully.");
                // Возможно, обновление отображаемых данных на странице
            } else if (data.status === 'error') {
                // Обработка ошибок валидации формы
                alert("Form validation failed. Errors: " + data.errors);
            } else {
                // Обработка других ошибок, если таковые могут возникнуть
                alert("Unknown error occurred.");
            }
            $("#ModalWindow").modal("hide");
            $('body').removeClass('modal-open');
            window.location.reload()
        },


        });
    });
});
