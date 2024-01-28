import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../components/Login.vue";
import Register from "../components/Register.vue";
import CreateSudoku from "../components/CreateSudoku.vue";
import Leaderboard from "../components/Leaderboard.vue";
import BootstrapVue from "bootstrap-vue";
import FederationLogin from "../components/FederationLogin.vue";
import PlaySudoku from "../components/PlaySudoku.vue";
import FederationRedirect from "../components/FederationRedirect.vue";
import SudokuSelector from "../components/SudokuSelector.vue";
import AccountPage from "../components/AccountPage.vue";
import PlayMineSweeper from "@/components/PlayMineSweeper";
import MineSweeperSelector from "@/components/MineSweeperSelector";
import ForgotPassword from "@/components/ForgotPassword";
import MiracleSudokuSelector from "@/components/MiracleSudokuSelector";

Vue.use(VueRouter);
Vue.use(BootstrapVue);

function routerGuard(to, from, next) {
  let isAuthenticated = !!localStorage.getItem("loggedIn");

  if (isAuthenticated) {
    next();
  } else {
    alert("You must login first!");
    next("/login");
  }
}

const routes = [
  {
    path: "/login",
    name: "Login",
    alias: "",
    get component(){
      let isAuthenticated = !!localStorage.getItem("loggedIn");
      if(isAuthenticated){
        //TODO: return user profile page?
        return SudokuSelector
      }else{
        return Login
      }
    }
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
  {
    path: "/create",
    name: "Create Sudoku",
    beforeEnter: routerGuard,
    component: CreateSudoku,
  },
  {
    path: "/leaderboard",
    name: "Leaderboard",
    beforeEnter: routerGuard,
    component: Leaderboard,
  },
  {
    path: "/oauth/authorize",
    name: "Federation Login",
    component: FederationLogin,
    meta: {
      hideNavBar: true,
    },
  },
  {
    path: "/oauth/redirect/:client_id",
    name: "Login Redirect",
    component: FederationRedirect,
    meta: {
      hideNavBar: true,
    },
  },
  {
    path: "/sudokus",
    beforeEnter: routerGuard,
    name: "Sudokus",
    component: SudokuSelector,
  },
  {
    path: "/miracle-sudokus",
    beforeEnter: routerGuard,
    name: "MiracleSudokus",
    component: MiracleSudokuSelector,
    props: true
  },
  {
    path: "/play-sudoku",
    beforeEnter: routerGuard,
    name: "Play Sudoku",
    component: PlaySudoku,
    props:true,
  },
  {
    path: "/user",
    beforeEnter: routerGuard,
    name: "AccountPage",
    component: AccountPage,
  },
  // {
  //   path: "/previewtest",
  //   name: "SudokuPreview",
  //   component: SudokuPreview,
  // },
  {
    path:"/playMinesweeper",
    beforeEnter: routerGuard,
    name:"PlayMineSweeper",
    component: PlayMineSweeper,
  },
  {
    path:"/minesweeper",
    beforeEnter: routerGuard,
    name:"MineSweeperSelector",
    component: MineSweeperSelector,
  },
  {
    path:"/forgotPassword",
    name:"ForgotPassword",
    component:ForgotPassword,
  },
  { path: "*", redirect: "/" },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

/*router.beforeEach((to, from, next) => {
  const publicPages = ['/login'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('user');

  if(authRequired && !loggedIn){
    return next({
      path: '/login',
      query: { returnUrl: to.path }
    });
  }
  next();
})*/

export default router;
