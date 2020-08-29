import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false

new Vue({
    render: h => h(App),
    delimiters: ["[[", "]]"],   // 変数展開用の区切り文字を変更
}).$mount('#app')
