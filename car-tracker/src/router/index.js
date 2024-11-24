import { createRouter, createWebHistory } from 'vue-router';
// import Vue from "vue";
// import Router from "vue-router";
import AddCar from "../components/AddCar.vue";
import CarList from "../components/CarList.vue";

// Vue.use(Router);
const routes =  [
  { 
    path: "/", 
    component: CarList 
  },
  { 
    path: "/add", 
    component: AddCar 
  },
]; 

// export default new Router({
//   routes: [
//     { path: "/", component: CarList },
//     { path: "/add", component: AddCar },
//   ],
// });


const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
