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
