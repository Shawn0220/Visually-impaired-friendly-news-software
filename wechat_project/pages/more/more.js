// pages/more/more.js
import {creatTouchController,CONTROLSTATUS } from "../../utils/touch"
import { readController, initAudioController } from "../../utils/audio.js"
import { getVoice } from "../../utils/request"
const app = getApp()
Page({
  /* 页面的初始数据 */
  data: {
    activeId: 0,
    controlStatus: null,
    functionList: ["拍照阅读", "物体识别"],
    functionIcon: ["photo-o", "apps-o"],
    // , "实时翻译"
    functionVoice: [null, null]
  },
  /* 生命周期函数--监听页面加载 */
  onLoad(options) {
    // 创建触控处理对象
    creatTouchController(this, 'touchEvent', 'controlStatus')
    // 监控 controlStatus 的变化-左右滑动
    app.watch(this, {
      activeId: function(newVal) {
        if(newVal >= 0 && newVal < this.data.functionList.length) {
          if (this.data.functionVoice[newVal]) {
            readController(this.data.functionVoice[newVal],"voice")
          } else {
            getVoice("功能：" + this.data.functionList[newVal]).then(res=>{
              var voice = this.data.functionVoice
              voice[newVal] = res
              this.setData({ functionVoice: voice })
              readController(this.data.functionVoice[newVal],"voice")
            })
          }
          wx.pageScrollTo({
            selector: "#item" + parseInt(newVal),
            offsetTop: -300,
          })
        }
      },
      controlStatus: function(newVal) {
        if (newVal == CONTROLSTATUS.right) {
          wx.switchTab({
            url: '/pages/user/user',
          })
        } else if (newVal == CONTROLSTATUS.left) {
          wx.switchTab({
            url: '/pages/categories/categories',
          })
        } else if (newVal == CONTROLSTATUS.up && this.data.activeId > 0) {
          readController("voice/home/theLastArticle.mp3", "control")
          this.setData({activeId: this.data.activeId - 1})
        } else if (newVal == CONTROLSTATUS.up && this.data.activeId == 0) {
          readController("voice/more/wasTheFirst.mp3", "control")
        } else if (newVal == CONTROLSTATUS.down && this.data.activeId < this.data.functionList.length - 1) {
          readController("voice/home/nextArticle.mp3", "control")
          this.setData({activeId: this.data.activeId + 1})
        } else if (newVal == CONTROLSTATUS.down && this.data.activeId == this.data.functionList.length - 1) {
          readController("voice/more/wasTheLast.mp3", "control")
        } else if (newVal == CONTROLSTATUS.singleTap) {
          if (this.data.activeId == 0) {
            readController("voice/more/introduceOnPhotoRead.mp3", "voice")
          } else if (this.data.activeId == 1) {
            readController("voice/more/introduceOnIdentify.mp3", "voice")
          }
        } else if (newVal == CONTROLSTATUS.doubleTap) {
          if (this.data.activeId == 0) {
            wx.navigateTo({
              url: "/pages/more/photoRead/photoRead",
            })
          } else if (this.data.activeId == 1) {
            wx.navigateTo({
              url: "/pages/more/identification/identification",
            })
          } else if (this.data.activeId == 2) {
            console.log("在线翻译")
          }
        }
      }
    })
  },
  /* 生命周期函数--监听页面初次渲染完成 */
  onReady() {},
  /* 生命周期函数--监听页面显示 */
  onShow() {
    initAudioController()
    readController("voice/more/more.mp3", "control")
  },
  /* 生命周期函数--监听页面隐藏 */
  onHide() {},
  /* 生命周期函数--监听页面卸载 */
  onUnload() {},
  /* 用户点击右上角分享*/
  onShareAppMessage() {}
})