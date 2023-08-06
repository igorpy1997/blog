// script_registration.js
$(document).ready(function () {
    // Function to open the registration modal
    function openRegistrationModal() {
        $.ajax({
            url: '/custom_reset_password/', // Update the URL with your registration URL
            type: 'GET',
            dataType: 'html',
            success: function (data) {
                $('#ModalWindow .modal-body').html(data);
                $("#ModalWindow").modal("show");
                $('body').addClass('modal-open');
            },
            error: function () {
                console.log('Failed to load registration form.');
            }
        });
    }

    // Attach click event handler to the registration button
    $("#resetPasswordButton").click(function () {
        openRegistrationModal();
    });

    // Attach click event handler to the "Save changes" button inside the modal
    $(document).on('click', '#saveChangesButton3', function () {
        // Serialize the form data
        var formData = $('#password-reset-form').serialize();
        // Submit the form data via AJAX
        $.ajax({
            url: $('#password-reset-form').attr('action'),
            type: 'POST',
            data: formData,
            dataType: 'json',
            complete: function(data) {
                if (data.status === 200) {
                    if ( data.responseJSON && data.responseJSON.status === "error") {


                        // Отобразите сгенерированный пароль на экране

                        alert("Form failed12");
                    }
                    else {
                        var generatedPassword = data.responseJSON.new_password;
                        console.log(generatedPassword)

                        $("#passwordResult").text("Сгенерированный пароль: " + generatedPassword);
                        alert("Copy generated password: " + generatedPassword)


                        $("#ModalWindow").modal("hide");
                        $('body').removeClass('modal-open');

                    }
                } else{
                    alert("Form failed");
                }

            },


        });
    });
});
