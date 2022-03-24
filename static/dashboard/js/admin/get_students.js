var my_vue_app = new Vue({
    el: "#main-container",
    delimiters: ['${', '}'],
    data: {
        selected_student: null,
        head_section_spinner: true,
        api_error: null,
        page_data: null,    
        calling_action: false,
        callAction_response: null
    },
    methods: {
        selectStudent: function (student_index) {
            let student_details = this.page_data.students[student_index];
            let temp_dict = student_details;
 
            this.selected_student = {
                index: student_index,
                student: temp_dict
            }
            
            console.log(this.selected_student);
        }
    },
    filters: {


        
    },

    mounted(){
        axios
        .get(url.get_students)
        .then(response => {
                this.head_section_spinner = false;
                console.log(response.data);
                if (response.data.status) {
                    this.api_error = null;
                    this.page_data = response.data.fields
                    // this.selected_student = {
                    //     index: 0,
                    //     student: this.page_data.students[0]
                    // }
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
