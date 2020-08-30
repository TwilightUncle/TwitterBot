

// 共通の状態を管理(ログイン状態等)
export default {
    debug: true,
    state: {
        is_signin: false
    },
    signin: function () {
        if (this.debug) console.log('signin');
        this.state.is_signin = true;
    },
    signout: function () {
        if (this.debug) console.log('signout');
        this.state.is_signin = false;
    }
}
