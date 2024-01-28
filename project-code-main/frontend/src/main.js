import Vue from "vue";
import App from "./App.vue";
import router from "./router";
// installing bootstrap
import "bootstrap/dist/css/bootstrap.css";
import BootstrapVue from "bootstrap-vue";
import VueCryptojs from "vue-cryptojs";
import axios from "axios";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core'
import {faEraser, faPencilAlt, faDownload, faUpload, faTimes} from '@fortawesome/free-solid-svg-icons';
import {faExchangeAlt} from "@fortawesome/free-solid-svg-icons/faExchangeAlt";
import { faSave, faLightbulb } from '@fortawesome/free-regular-svg-icons';

library.add(faEraser, faExchangeAlt, faSave, faPencilAlt, faSave, faLightbulb, faDownload, faUpload, faTimes);


// global variable
//Vue.prototype.$loggedIn = false;

Vue.config.productionTip = false;
// Vue.prototype.$hostname = 'http://localhost:27017';
Vue.prototype.$hostname = '/backend';
Vue.use(BootstrapVue);
Vue.use(VueCryptojs);
Vue.component('font-awesome-icon', FontAwesomeIcon);

new Vue({
  router,
  axios,
  render: (h) => h(App),
}).$mount("#app");
