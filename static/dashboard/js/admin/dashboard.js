var my_vue_app = new Vue({
    el: "#main-container",
    delimiters: ['${', '}'],
    data: {
        head_section_spinner: true,
        api_error: null,
        page_data: null,
        calling_action: false,
        callAction_response: null
    },
    methods: {

        callAction: function () {
            if (!(this.calling_action)) {
                this.calling_action = true;
                if (this.page_data.is_to_create_qr.status) {
                    this.createVoucher();
                }else{
                    this.downloadVoucher();
                }   
            }
        },

        downloadVoucher: function () {
            if (!(this.page_data.is_to_create_qr.status)) {
                let filename = `voucher-${this.page_data.is_to_create_qr.info.month}-${this.page_data.is_to_create_qr.info.year}.pdf`;
                setTimeout(() => {
                    print_card(filename);
                    this.calling_action = false;
                }, 1000);
            }
        },

        createVoucher: function () {
            axios
            .get(url.create_voucher)
            .then(response => {
                    // console.log(response.data);
                    setTimeout(() => {
                        if (response.data.status) {
                            this.page_data = response.data.fields
                        }

                        this.calling_action = false;
                        this.callAction_response = {
                            "status": response.data.status,
                            "message": response.data.message
                        }

                        setTimeout(() => {
                            this.callAction_response = null;
                        }, 4000);

                    }, 1000);  
                }
            )
        }
    },
    filters: {
        
    },

    mounted(){
        axios
        .get(url.dashboard_all_data)
        .then(response => {
                this.head_section_spinner = false;
                console.log(response.data);
                if (response.data.status) {
                    this.api_error = null;
                    this.page_data = response.data.fields
                }else{
                    this.api_error = response.data.message
                }                    
            }
        ).catch(error => {
            this.head_section_spinner = false;
            this.api_error = error;
            // console.log(error);
        });            
    }
});
