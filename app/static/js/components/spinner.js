// import Vue from '../vue'

Vue.component('component-spinner', {
    data: function () {
        return {
            show: false
        }
    },
    template: `
        <transition name="fade">
            <div v-if="show">
                <div class="spinner-overlay"></div>
                <div class="spinner-wrap">
                    <div class="spinner">Loading...</div>
                </div>
            </div>
        </transition>
    `,
    methods: {
        /**
         * くるくるの表示を切りかえる
         */
        spinnerToggle: function () {
            this.show = !this.show;
        },

        /**
         * くるくるを表示する
         */
        spinnerShow: function () {
            this.show = true;
        },

        /**
         * くるくるを見えなくする
         */
        spinnerHide: function () {
            this.show = false;
        }
    }
});
