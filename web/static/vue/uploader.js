const uploader = new Vue({
    el: '#uploader',
    delimiters: ["[[", "]]"],
    data: {
        errors: "",
        loading: false,
        progress: 0,
        version: '',
        model: ''
    },
    computed: {
        percentage: function () {
            return this.progress * 100
        }
    },
    methods: {
        filesUploader: function () {

            this.initLoading()

            const filesObject = this.$refs.selected.files;
            const fileDimension = filesObject.length;

            if (this.filesValidator(filesObject)) {

                for (let index = 0; index < filesObject.length; index++) {

                    file = filesObject[index];

                    const formData = new FormData();
                    formData.append('file', file);

                    axios.post('/upload',
                        formData,
                        {
                            headers: {
                                'Content-Type': 'multipart/form-data',
                                'X-CSRFToken': $('#csrf').data("value"),
                                'Version': this.version,
                                'Model': this.model
                            }
                        }).catch(error => {
                            this.errors += file.name + ' could not be uploaded! ';
                        });

                    // increment progress bar
                    this.progress = ((index + 1) / fileDimension);
                };

            } else {
                this.errors = "No duplicates allowed, and only files with extension .spold are supported!"
            }

            this.loading = false;
        },
        filesValidator: function (files) {

            let evaluator = true

            const names = []
            for (let index = 0; index < files.length; index++) {
                names.push(files[index].name);
            }

            // Check if there are duplicates
            if (new Set(names).size !== names.length) {
                evaluator = false;
            }

            // Check if all files are from the desired extension
            names.forEach(name => {
                if (name.split('.').pop() !== 'spold') {
                    evaluator = false;
                }
            });

            return evaluator;
        },
        initLoading: function () {
            this.errors = "";
            this.progress = 0;
            this.loading = true;
        }
    }
});

