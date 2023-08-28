// pages/user/userInfo/userInfo.js
import {creatTouchController,CONTROLSTATUS } from "../../../utils/touch"
import {getUserInfo, getVoice, setUserInfo } from "../../../utils/request"
import { readController, initAudioController } from "../../../utils/audio.js"
const app = getApp()
Page({
  /**
   * 页面的初始数据
   */
  data: {
    nickname: null,
    userAge: null,
    userSex: null,
    userTel: null,
    userProvince: null,
    userCity: null,
    userMail: null,
    activeId: 1,
    controlStatus: null,
    inputStatus: false,
    introduction: null,
    updateStatus: false,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    // 创建触控处理对象
    creatTouchController(this, 'touchEvent', 'controlStatus')
    // 监控 controlStatus 的变化-左右滑动
    app.watch(this, {
      activeId: function(newVal) {
        if(newVal >= 0 && newVal <= 6) {
          this.singleTap(newVal)
          wx.pageScrollTo({
            selector: "#item" + parseInt(newVal),
            offsetTop: -300,
          })
        } else if (newVal == -1) {
          if (this.data.introduction) {
            readController(this.data.introduction, "voice")
          } else if (this.data.nickname) {
            getVoice("尊敬的用户：" + this.data.nickname + ", 您好！您现在在用户信息界面，您可以下滑收听信息项，左滑右滑返回个人信息").then(res=>{
              this.setData({introduction: res})
              readController(res, "voice")
            })
          } else {
            getVoice("尊敬的微信用户, 您好！您现在在用户信息界面，您可以下滑收听信息项，左滑右滑返回个人信息").then(res=>{
              this.setData({introduction: res})
              readController(res, "voice")
            })
          }
        } 
      },
      controlStatus: function(newVal) {
        if (newVal == CONTROLSTATUS.right || newVal == CONTROLSTATUS.left) {
          wx.navigateBack({
            success: res=>{
              readController("voice/return.mp3","control")
            }
          })
        } else if (newVal == CONTROLSTATUS.up && this.data.activeId > -1) {
          this.setData({activeId: this.data.activeId - 1})
        } else if (newVal == CONTROLSTATUS.up && this.data.activeId == -1) {
          if (this.data.introduction) {
            readController(this.data.introduction, "voice")
          } else if (this.data.nickname) {
            getVoice("尊敬的用户：" + this.data.nickname + ", 您好！").then(res=>{
              this.setData({introduction: res})
              readController(res, "voice")
            })
          } else {
            getVoice("尊敬的微信用户, 您好！").then(res=>{
              this.setData({introduction: res})
              readController(res, "voice")
            })
          }
        } else if (newVal == CONTROLSTATUS.down && this.data.activeId < 6) {
          this.setData({activeId: this.data.activeId + 1})
          console.log("down")
          console.log(this.data.activeId)
        } else if (newVal == CONTROLSTATUS.down && this.data.activeId == 6) {
          readController("voice/user/wasTheLastInfo.mp3","control")
        } else if (newVal == CONTROLSTATUS.singleTap) {
          this.singleTap(this.data.activeId)
        } else if (newVal == CONTROLSTATUS.doubleTap) {
          this.doubleTap(this.data.activeId)
        }
      }
    })
  },
  singleTap(index) {
    if (index == 0) {
      if (this.data.nickname) {
        getVoice("您的昵称为：" + this.data.nickname).then(res=>{
          readController(res, "voice")
        })
      } else {
        getVoice("您还没有设置您的昵称，双击或长按进入设置").then(res=>{
          readController(res, "voice")
        })
      }
    } else if (index == 1) {
      if (this.data.userAge) {
        getVoice("您的年龄为：" + this.data.userAge + "岁").then(res=>{
          readController(res, "voice")
        })
      } else {
        getVoice("您还没有设置您的年龄，双击或长按进入设置").then(res=>{
          readController(res, "voice")
        })
      }
    } else if (index == 2) {
      if (this.data.userSex) {
        getVoice("您的性别为：" + this.data.userSex).then(res=>{
          readController(res, "voice")
        })
      } else {
        getVoice("您还没有设置您的性别，双击或长按进入设置").then(res=>{
          readController(res, "voice")
        })
      }
    } else if (index == 3) {
      if (this.data.userTel) {
        getVoice("您的电话为：" + this.data.userTel).then(res=>{
          readController(res, "voice")
        })
      } else {
        getVoice("您还没有设置您的联系方式，双击或长按进入设置").then(res=>{
          readController(res, "voice")
        })
      }
    } else if (index == 4) {
      if (this.data.userProvince) {
        getVoice("您所在的省份为：" + this.data.userProvince).then(res=>{
          readController(res, "voice")
        })
      } else {
        getVoice("您还没有设置您所在的省份，双击或长按进入设置").then(res=>{
          readController(res, "voice")
        })
      }
    } else if (index == 5) {
      if (this.data.userCity) {
        getVoice("您所在的市为：" + this.data.userCity).then(res=>{
          readController(res, "voice")
        })
      } else {
        getVoice("您还没有设置您所在的地市，双击或长按进入设置").then(res=>{
          readController(res, "voice")
        })
      }
    } else if (index == 6) {
      if (this.data.userMail) {
        getVoice("您的邮箱地址为：" + this.data.userMail).then(res=>{
          readController(res, "voice")
        })
      } else {
        getVoice("您还没有设置您的邮箱地址，双击或长按进入设置").then(res=>{
          readController(res, "voice")
        })
      }
    }
  },
  doubleTap(index) {
    if (index != -1) {
      if (this.data.inputStatus) {
        readController("voice/user/successEdit.mp3", "control")
        this.setData({updateStatus: true})
      } else {
        readController("voice/user/onEdit.mp3", "control")
      }
      this.setData({inputStatus: !this.data.inputStatus})
    }
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
    getUserInfo().then(res=>{
      this.setData({
        nickname: res.nickname,
        userAge: res.userAge,
        userSex: res.userSex,
        userTel: res.userTel,
        userProvince: res.userProvince,
        userCity: res.userCity,
        userMail: res.userMail,
      })
    })
    initAudioController()
    readController("voice/user/userInfo.mp3", "control")
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
    if (this.data.updateStatus) {
      setUserInfo({
        nickname: this.data.nickname,
        userAge: this.data.userAge,
        userSex: this.data.userSex,
        userTel: this.data.userTel,
        userProvince: this.data.userProvince,
        userCity: this.data.userCity,
        userMail: this.data.userMail,
      }).then(res=>{
        console.log("修改完成")
      })
    }
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

  }
})