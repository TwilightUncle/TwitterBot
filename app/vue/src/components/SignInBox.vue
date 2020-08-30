<template>
    <div class="sign-in">
        <div class="item">
            <label for="user_name">ユーザー名</label>
            <input type="text" name="user_name" v-model="input_user_name">
        </div>
        <div class="item">
            <label for="password">パスワード</label>
            <input type="password" name="password" v-model="input_password">
        </div>
        <div class="item">
            <button v-on:click="signIn">サインイン</button>
        </div>
    </div>
</template>

<script>
import api from "@/api";
import store from "@/store";

export default {
    data: function () {
        return {
            input_user_name: "",
            input_password: ""
        };
    },
    methods: {
        signIn: async function () {
            const result = await api.post('/auth/sign-in', {
                user_name: this.input_user_name,
                password: this.input_password
            });
            if (store.debug) console.log(result.data.is_login);

            // ログインに成功したときフロントでもログイン状態を保持する
            if (result.data.is_login == 'true')  store.signin();
            else                            store.signout();
        }
    }
}
</script>

<style scoped>
.sign-in {
    display: inline-block;
    padding: 16px;
    background-color: #8f8;
    border-radius: 16px;
}

.item {
    margin: 8px;
}

label::after {
	content: "\A" ;
	white-space: pre ;
}

button {
    background-color: #6b6;
    color: #fff;
}
button:hover {
    cursor: pointer;
}
</style>