// import Vue from './vue.js'
import './components/spinner.js';

// the root view model
let app = new Vue({
    el: '#app',
    delimiters: ["[[", "]]"],   // 変数展開用の区切り文字を変更
    methods: {
        /**
         * くるくるの表示切り替えを行う
         */
        spinnerToggle: function () {
            this.$refs.spinner.spinnerToggle();
        },

        /**
         * くるくるを表示する
         */
        spinnerShow: function () {
            this.$refs.spinner.spinnerShow();
        },

        /**
         * くるくるを見えなくする
         */
        spinnerHide: function () {
            this.$refs.spinner.spinnerHide();
        }
    }
});
