// pages/more/identification/identification.js
import { creatTouchController, CONTROLSTATUS} from "../../../utils/touch"
import {getIdentifyByPhoto} from "../../../utils/request"
import {readController} from "../../../utils/audio"
const app = getApp()
Page({
  /**
   * 页面的初始数据
   */
  data: {
    controlStatus: null,
    loading: false,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    // 创建触控处理对象
    creatTouchController(this, 'touchEvent', 'controlStatus')
    app.watch(this, {
      controlStatus: function(newVal) {
        if (newVal == CONTROLSTATUS.left || newVal == CONTROLSTATUS.right) {
          wx.navigateBack({
            success: res=>{
              readController("voice/return.mp3","control")
            }
          })
        } else if (newVal == CONTROLSTATUS.singleTap) {
          if (this.data.loading) {
            readController("voice/more/loadingForIdentify.mp3", "control")
          } else {
            readController("voice/more/identify.mp3", "control")
          }
        } else if (newVal == CONTROLSTATUS.doubleTap) {
          if (this.data.loading) {
            readController("voice/more/loadingForIdentify.mp3", "control")
          } else {
            readController("voice/more/loadingForIdentify.mp3", "control")
            const ctx = wx.createCameraContext()
            ctx.setZoom({
              zoom: 1
            })
            ctx.takePhoto({
              quality: 'high',
              success: (res) => {
                getIdentifyByPhoto(res.tempImagePath).then(res=>{
                  readController(res.voice, "voice")
                })
              },
              complete: res=> {
                this.setData({ loading: false })
              }
            })
          }
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
    readController("voice/more/identify.mp3", "control")
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
  cameraInitDone: function(event) {
    console.log(event.detail)
  }
})