import VueRouter from "vue-router";
import SfLogin from "../components/Auth/SfLogin";
import SfSignup from "../components/Auth/SfSignup";
import SfListPostWithToggleView from "../components/Post/ListPosts/SfListPostWithToggleView";
import SfDisplayPost from "../components/Post/SfDisplayPost";
import SfCreatePost from "../components/Post/CreatePost/SfCreatePost";
import SfHomePage from "../components/SfHomePage";
import SfErrorPage from "../components/SfErrorPage";
import SfUserProfile from "../components/UserProfile/SfUserProfile";
import SfMessageDialog from "../components/Chat/SfMessageDialog.vue";
import SfChatHistory from "../components/Chat/SfChatHistory.vue";
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
    path: "/chat_history",
    component: SfChatHistory,
    meta: { requiresAuth: true },
  },
  {
    path: "/profile/:id",
    component: SfUserProfile,
    meta: { requiresAuth: true },
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
    path: "/chat/:cid/:rid",
    component: SfMessageDialog,
    props: true, // Pass route params as props to the component
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
