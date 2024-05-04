import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import "./index.css";
import VueRouter from "vue-router";
import VueQuillEditor from "vue-quill-editor";
import "quill/dist/quill.core.css"; // import styles
import "quill/dist/quill.snow.css"; // for snow theme
import "quill/dist/quill.bubble.css"; // for bubble theme
import main from "./store";
import { store } from "./store";

await main(store);

Vue.use(VueQuillEditor /* { default global options } */);
Vue.config.productionTip = false;

Vue.use(VueRouter);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
