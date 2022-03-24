var my_vue_app = new Vue({
    el: "#main-container",
    delimiters: ['${', '}'],
    data: {
    },
    methods: {
        downloadVoucher: function () {
            print_card(null, true);
            this.calling_action = false;
        },
    },
    filters: {
        
    },

    mounted(){
    }
});
