// user.js
// 获取应用实例
import {creatTouchController,CONTROLSTATUS } from "../../utils/touch"
import { readController, initAudioController } from "../../utils/audio.js"
import { getUserInfo } from "../../utils/request"
const app = getApp()
Page({
  data: {
    activeId: 0,
    controlStatus: null,
    functionList: ["用户信息", "浏览记录", "收藏记录"],
    nickname: null,
  },
  onShow() {
    initAudioController()
    readController("voice/user/userIntroduce.mp3", "control")
    getUserInfo().then(res=>{
      this.setData({nickname: res.nickname})
    })
	},
  onLoad() {
    // 创建触控处理对象
    creatTouchController(this, 'touchEvent', 'controlStatus')
    // 监控 controlStatus 的变化-左右滑动
    app.watch(this, {
      activeId: function(newVal) {
        if(newVal >= 0 && newVal < this.data.functionList.length) {
          if (newVal == 0) {
            readController("voice/user/information.mp3", "control")
          } else if (newVal == 1) {
            readController("voice/user/browse.mp3", "control")
          } else if (newVal == 2) {
            readController("voice/user/star.mp3", "control")
          }
          wx.pageScrollTo({
            selector: "#item" + parseInt(newVal),
            offsetTop: -150,
          })
        }
      },
      controlStatus: function(newVal) {
        if (newVal == CONTROLSTATUS.right) {
          readController("voice/user/userRight.mp3", "control")
        } else if (newVal == CONTROLSTATUS.left) {
          wx.switchTab({
            url: '/pages/more/more',
          })
        } else if (newVal == CONTROLSTATUS.up && this.data.activeId > 0) {
          this.setData({activeId: this.data.activeId - 1})
        } else if (newVal == CONTROLSTATUS.up && this.data.activeId == 0) {
          readController("voice/user/wasTheFirst.mp3", "control")
        } else if (newVal == CONTROLSTATUS.down && this.data.activeId < this.data.functionList.length - 1) {
          this.setData({activeId: this.data.activeId + 1})
        } else if (newVal == CONTROLSTATUS.down && this.data.activeId == this.data.functionList.length - 1) {
          readController("voice/user/wasTheLast.mp3", "control")
        } else if (newVal == CONTROLSTATUS.singleTap) {
          if (this.data.activeId == 0) {
            readController("voice/user/information.mp3", "control")
          } else if (this.data.activeId == 1) {
            readController("voice/user/browse.mp3", "control")
          } else if (this.data.activeId == 2) {
            readController("voice/user/star.mp3", "control")
          }
        } else if (newVal == CONTROLSTATUS.doubleTap) {
          if (this.data.activeId == 0) {
            wx.navigateTo({
              url: "/pages/user/userInfo/userInfo",
            })
          } else if (this.data.activeId == 1) {
            wx.navigateTo({
              url: "/pages/user/browseHistory/browseHistory",
            })
          } else if (this.data.activeId == 2) {
            wx.navigateTo({
              url: "/pages/user/starHistory/starHistory",
            })
          }
        }
      }
    })
  },
})
