import VueRouter from "vue-router";
import SfLogin from "../components/Auth/SfLogin";
import SfSignup from "../components/Auth/SfSignup";
import SfListPostWithToggleView from "../components/Post/ListPosts/SfListPostWithToggleView";
import SfDisplayPost from "../components/Post/SfDisplayPost";
import SfCreatePost from "../components/Post/CreatePost/SfCreatePost";
import SfHomePage from "../components/SfHomePage";
import SfErrorPage from "../components/SfErrorPage";
import { store } from "../store/index";

const routes = [
  {
    path: "/login",
    component: SfLogin,
    meta: { requiresAuth: false },
  },
  {
    path: "/signup",
    component: SfSignup,
    meta: { requiresAuth: false },
  },
  {
    path: "/list-posts",
    component: SfListPostWithToggleView,
    meta: { requiresAuth: true },
  },
  {
    path: "/post/:id",
    component: SfDisplayPost,
    meta: { requiresAuth: true },
  },
  {
    path: "/create-post",
    component: SfCreatePost,
    meta: { requiresAuth: true },
  },
  {
    path: "/",
    component: SfHomePage,
  },
  {
    path: "*",
    component: SfErrorPage,
  },
];

const router = new VueRouter({
  mode: "history",
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.user;

  if (
    to.matched.some((record) => record.meta.requiresAuth) &&
    !isAuthenticated
  ) {
    // Redirect to login if the route requires authentication and the user is not authenticated
    next("/login");
  } else if (
    to.matched.some((record) => record.meta.requiresAuth === false) &&
    isAuthenticated
  ) {
    // Redirect to login if the route requires authentication and the user is not authenticated
    next("/list-posts");
  } else {
    next();
  }
});

export default router;
