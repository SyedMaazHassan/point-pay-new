var my_vue_app = new Vue({
    el: "#main-container",
    delimiters: ['${', '}'],
    data: {
        months: {
            '1': "Jan",
            '2': "Feb",
            '3': "Mar",
            '4': "Apr",
            '5': "May",
            '6': "Jun",
            '7': "July",
            '8': "Aug",
            '9': "Sep",
            '10': "Oct",
            '11': "Nov",
            '12': "Dec"
        },
        selected_voucher: null,
        head_section_spinner: true,
        api_error: null,
        page_data: null,
        calling_action: false,
        callAction_response: null
    },
    methods: {
        showDate: function(month_number, year){
            return `${this.months[month_number]}, ${year}`;
        },

        showDateDict: function (month_number, year) {
            return {
                "month": this.months[month_number],
                "year": year
            }
        },

        downloadVoucher: function () {
            console.log("abc");
            print_card(null, true);
            this.calling_action = false;
        },

        selectVoucher: function (voucher_index) {
            let voucher_details = this.page_data.voucher_history[voucher_index];
            let temp_dict = voucher_details.fields;
            temp_dict["id"] = voucher_details.pk;
 
            this.selected_voucher = {
                index: voucher_index,
                voucher: temp_dict
            }
            
            console.log(this.selected_voucher);
        }
    },
    filters: {
        
    },

    mounted(){

        axios
        .get(url.get_voucher_history)
        .then(response => {
                this.head_section_spinner = false;
                // console.log(response.data);
                if (response.data.status) {
                    this.api_error = null;
                    response.data.fields.voucher_history = JSON.parse(response.data.fields.voucher_history)
                    console.log(response.data.fields);
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
