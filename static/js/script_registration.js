// script_registration.js
$(document).ready(function () {
    // Function to open the registration modal
    function openRegistrationModal() {
        $.ajax({
            url: '/register/', // Update the URL with your registration URL
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
    $("#registrationButton").click(function () {
        console.log("HI")
        openRegistrationModal();
    });

    // Attach click event handler to the "Save changes" button inside the modal
    $(document).on('click', '#saveChangesButton', function () {
        // Serialize the form data
        var formData = $('#registrationForm').serialize();
        // Submit the form data via AJAX
        $.ajax({
            url: $('#registrationForm').attr('action'),
            type: 'POST',
            data: formData,
            dataType: 'json',
            complete: function(data) {
                if (data.status === 200) {
                    if ( data.responseJSON && data.responseJSON.status === "error") {
                        alert("Form failed12");
                    }
                    else {

                        alert("Good work")


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
