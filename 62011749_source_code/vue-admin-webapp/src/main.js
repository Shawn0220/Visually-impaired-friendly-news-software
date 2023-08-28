import Vue from 'vue'
import App from './App.vue'
import router from '@/router'
import store from './store'
import '@/style/index.scss' // glob scss
import './plugins/element.js'
import animated from 'animate.css'
import '@/assets/iconfont/iconfont.css'

Vue.use(animated)
// import SlideVerify from 'vue-monoplasty-slide-verify'

// Vue.use(SlideVerify)
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

const audio = new Audio();
function debounce(fn,delay){
  let timer;
  return function(){
    let _this = this;
    let args = arguments;
    if(timer){
      clearTimeout(timer)
    }
    timer = setTimeout(()=>{
      fn.apply(_this,args)
    },delay)
  }
}
function read (src){
  audio.pause();
  audio.src = src;
  audio.play().then(r => {});
}
Vue.prototype.audioRead = debounce(read,150);
Vue.prototype.$writerId = null;
