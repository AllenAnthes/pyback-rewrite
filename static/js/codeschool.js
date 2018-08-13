Dropzone.options.logoDropzone = {
    url: "{{ url_for('school') }}",
    paramName: 'logo',
    autoProcessQueue: false,
    acceptedFiles: 'image/*',
    addRemoveLinks: true,
    init: function () {
        this.on('sending', addFieldsToPayload);
        this.on('success', redirectToIssues);
        this.on("thumbnail", checkDimensions);
        $('#new_school_form').submit(e => {
            e.preventDefault();
            this.processQueue();
        });
    },
    accept: bindCallback,
};

function redirectToIssues(file, response) {
    if (response.code === 302)
        window.location.href = response.redirect;
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

function bindCallback(file, done) {
    file.acceptDimensions = done;
    file.rejectDimensions = () => done("Logo must be 200x200");

}