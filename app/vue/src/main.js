import Vue from 'vue'
import App from './App.vue'
// import router from './router'

// Vue.use(Router)
Vue.config.productionTip = false

new Vue({
    // router,
    render: h => h(App),
    delimiters: ["[[", "]]"],   // 変数展開用の区切り文字を変更
}).$mount('#app')
