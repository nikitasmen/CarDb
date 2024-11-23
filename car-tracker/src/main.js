import Vue from "vue";
import Router from "vue-router";
import AddCar from "./components/AddCar.vue";
import CarList from "./components/CarList.vue";

Vue.use(Router);

export default new Router({
  routes: [
    { path: "/", component: CarList },
    { path: "/add", component: AddCar },
  ],
});
