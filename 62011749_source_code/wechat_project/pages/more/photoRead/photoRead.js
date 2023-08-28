// pages/more/photoRead/photoRead.js
import {CONTROLSTATUS, creatTouchController} from "../../../utils/touch"
import {getVoiceByPhoto} from "../../../utils/request"
import { readController,contentStart,contentStop } from "../../../utils/audio"
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    controlStatus: null,
    src: null,
    showCamera: true,
    activeId: 0,
    textVoice: null,
    readingContent: false,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    // 创建触控处理对象
    creatTouchController(this, 'touchEvent', 'controlStatus')
    app.watch(this, {
      controlStatus : function(newVal) {
        if (newVal == CONTROLSTATUS.left || newVal == CONTROLSTATUS.right) {
          wx.navigateBack({
            success: res=>{
              readController("voice/return.mp3","control")
            }
          })
        } else if (newVal == CONTROLSTATUS.singleTap) {
          if (this.data.showCamera) {
            readController("voice/more/photoing.mp3", "control")
          } else {
            readController("voice/more/readIntroduce.mp3", "control")
          }
        } else if (newVal == CONTROLSTATUS.doubleTap) {
          if (this.data.showCamera) {
            console.log("controlStatus doubleTap")
            readController("voice/more/loading.mp3", "control")
            this.takePhoto()
          } else if (this.data.readingContent) {
            contentStop()
            this.setData({readingContent: false})
          } else {
            contentStart(this.data.textVoice, app.myAudioController.textStartTime)
            this.setData({readingContent: true})

          }
        } else if (newVal == CONTROLSTATUS.longTapStart) {
          readController("voice/more/photoing.mp3", "control")
          this.setData({showCamera:true})
        } else if (newVal == CONTROLSTATUS.longTapEnd) {
          console.log("controlStatus longTapEnd")
        } else if (newVal == CONTROLSTATUS.cancel) {
          console.log("controlStatus cancel")
        }
      }
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
    readController("voice/more/photoRead.mp3", "control")
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  },
  takePhoto: function() {
    const ctx = wx.createCameraContext()
    ctx.setZoom({
      zoom: 1
    })
    ctx.takePhoto({
      quality: 'high',
      success: (res) => {
        this.setData({
          src: res.tempImagePath,
          showCamera: false
        })
        getVoiceByPhoto(res.tempImagePath).then(res=>{
          this.setData({
            textVoice: res.voice,
          })
          readController("voice/more/loaded.mp3", "control")
        })
      }
    })
  },
  cameraInitDone: function(event) {
    console.log(event.detail)
  }
})