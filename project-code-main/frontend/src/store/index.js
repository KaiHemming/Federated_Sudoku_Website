/*import { createStore } from 'vuex'

export default createStore({
    state: {
        access_token: '',
        refresh_token: '',
        isAuthenticated: false
    },
    mutations: {
        initialiseStore(state){
            if(localStorage.getItem('access_token')){
                state.access_token = localStorage.getItem('access_token')
                state.isAuthenticated = true
            } else {
                state.access_token = ''

            }
        },
        setAccessToken(state, access_token){
            //localStorage.setItem('access_token', access_token)
            state.access_token = access_token
            state.isAuthenticated = true
        },
        setRefreshToken(state, refresh_token){
            state.refresh_token = refresh_token
        },
        removeAccessToken(state){
            localStorage.removeItem('token')
            state.access_token = ''
            state.isAuthenticated = false
        }
    },
    actions: {

    },
    modules: {

    }
})*/
