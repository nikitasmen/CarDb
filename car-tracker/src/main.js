import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // If you're using Vue Router
// import store from './store'; // If you're using Vuex

const app = createApp(App);

app.use(router); // Ensure router exists
// app.use(store);  // Ensure store exists

app.mount('#app');
