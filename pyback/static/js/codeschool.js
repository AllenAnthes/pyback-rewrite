const url = document.getElementById('new_school_form').action;

Dropzone.options.logoDropzone = {
    url: url,
    paramName: 'logo',
    autoProcessQueue: false,
    acceptedFiles: 'image/*',
    addRemoveLinks: true,
    hiddenInputContainer: '#new_school_form',
    init: function () {
        this.on("thumbnail", checkDimensions);
        this.on('sending', addFieldsToPayload);
        this.on('success', redirectToIssues);
        $('#new_school_form').submit(e => {
            e.preventDefault();
            this.processQueue();
        });
    },
    accept: bindCallback,
};

function bindCallback(file, done) {
    file.acceptDimensions = done;
    file.rejectDimensions = () => done("Logo must be 200x200");
}

function checkDimensions(file) {
    if (file.width !== 200 || file.height !== 200) {
        file.rejectDimensions()
    }
    else {
        file.acceptDimensions();
    }
}

function addFieldsToPayload(data, xhr, formData) {
    $('#new_school_form').serializeArray()
        .forEach(field => formData.append(field.name, field.value));
}

function redirectToIssues(file, response) {
    if (response.redirect !== undefined) {
        window.location.href = response.redirect;
    }
    else {
        console.log(response);
    }
}
