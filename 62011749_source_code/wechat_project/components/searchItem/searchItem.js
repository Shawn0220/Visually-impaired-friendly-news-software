// components/searchItem/searchItem.js
import {CONTROLSTATUS} from "../../utils/touch"
import { searchArticlesByVoice,searchArticlesByText } from "../../utils/request.js"
import { readController } from "../../utils/audio.js"
const recorderManager = wx.getRecorderManager()
Component({
  /* 组件的属性列表 */
  properties: {
    controlStatus: Number,
    myStyle: String
  },
  /* 组件的初始数据 */
  data: { 
    animationData1: "",
    animationData2: "",
    animationStatus: false,
    showRecode: false,
    searchText: "",
    focusInput: false
  },
  /* 属性值监控 */
  observers: {
    'controlStatus': function(newVal) {
      if (newVal == CONTROLSTATUS.singleTap) {
        console.log("wzx")
        readController("voice/search/search.mp3","control")
        readController("voice/search/searchHelp.mp3","voice")
      } else if (newVal == CONTROLSTATUS.doubleTap) {
        console.log("controlStatus doubleTap")
        if (this.data.focusInput) {
          readController("voice/search/searching.mp3","control")
          searchArticlesByText(this.data.searchText).then(res=>{
            console.log(res)
            this.setData({
              searchText: res.text,
            });
            this.triggerEvent("updateArticles",{
              articles: res.data,
            },{})
            readController("voice/search/searchFinished.mp3","control")
            readController(res.voice,"voice")
          })
        } else {
          readController("voice/search/textInput.mp3","control")
        }
        this.setData({focusInput: !this.data.focusInput})
      } else if (newVal == CONTROLSTATUS.longTapStart) {
        this.recodeStart(this)
        this.recodeAnimationStart(this)
      } else if (newVal == CONTROLSTATUS.longTapEnd) {
        console.log("controlStatus longTapEnd")
        this.recodeStop(this)
        this.recodeAnimationEnd(this)
      } else if (newVal == CONTROLSTATUS.cancel) {
        console.log("controlStatus cancel")
        this.recodeStop(this)
        this.recodeAnimationEnd(this)
      }
    }
  },
  /* 组件的方法列表 */
  methods: {
    /* 录音动画开始 */
    recodeAnimationStart(that) {
      function animationFun(animationData){
        if(!that.data.animationStatus){
          return 
        }
        var animation = wx.createAnimation({
          duration: 1000
        })
        animation.opacity(0).scale(2, 2).step(); 
        that.setData({
          [`${animationData}`]: animation.export()
        })
      };
      function animationEnd(animationData) {
        var animation = wx.createAnimation({
          duration: 0
        })
        animation.opacity(1).scale(1, 1).step(); 
        that.setData({
          [`${animationData}`]: animation.export()
        })
      };
      function animationRest() {
        //动画重置
        animationEnd('animationData1')
        setTimeout(()=>{
          animationEnd('animationData2')
        },500)
        setTimeout(() => {
          if (that.data.animationStatus) {
            that.recodeAnimationStart(that)
          }
        }, 100)
      };
      that.setData({
        showRecode: true,
        animationStatus: true,
      })
      animationFun('animationData1')
      setTimeout(()=>{
        animationFun('animationData2')
      },500)
      setTimeout(() => {
        animationRest()
      }, 1000)
    },
    /* 录音动画结束 */
    recodeAnimationEnd(that) {
      //动画1结束
      var animation1 = wx.createAnimation({
        duration: 0
      })
      animation1.opacity(1).scale(1, 1).step(); 
      //动画2结束
      var animation2 = wx.createAnimation({
        duration: 0
      })
      animation2.opacity(1).scale(1, 1).step(); 
      that.setData({
        showRecode: false,
        animationData1: animation1.export(),
        animationData2: animation2.export(),
        animationStatus: false
      })
    },
    /* 开始录音 */
    recodeStart(that) {
      const options = {
        duration: 60000,//指定录音的时长，单位 ms
        sampleRate: 16000,//采样率
        numberOfChannels: 1,//录音通道数
        encodeBitRate: 96000,//编码码率
        format: 'PCM',//音频格式
        frameSize: 50,//指定帧大小，单位 KB
      }
      //开始录音
      readController("voice/search/recodeStart.mp3","control")
      setTimeout(()=>{
        recorderManager.start(options);
      }, 500)
      recorderManager.onStart(() => {
        console.log('recorder start')
      });
      //错误回调
      recorderManager.onError((res) => {
        console.log(res);
      })
    },
    /* 停止录音 */
    recodeStop(that) {
      readController("voice/search/recodeEnd.mp3","control")
      recorderManager.stop();
      recorderManager.onStop((res) => {
        this.searchArticles(res.tempFilePath)
      })
    },
    /* 文章搜索 */ 
    searchArticles(tempFilePath) {
      readController("voice/search/searching.mp3","control")
      searchArticlesByVoice(tempFilePath).then(res=>{
        this.setData({
          searchText: res.text,
        });
        this.triggerEvent("updateArticles",{
          articles: res.data,
        },{})
        readController("voice/search/searchFinished.mp3","control")
        readController(res.voice,"control")
      })
    },
    onChange(event) {
      this.setData({
        searchText: event.detail
      })
    }
  },
})
