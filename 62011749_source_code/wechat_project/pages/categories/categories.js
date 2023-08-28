// pages/categories/categories.js
const app = getApp()
import {getCategorys, getVoice} from "../../utils/request.js"
import {creatTouchController,CONTROLSTATUS } from "../../utils/touch"
import { readController, initAudioController } from "../../utils/audio.js"

Page({
  /* 页面的初始数据 */
  data: {
    categorys: [],
    controlStatus: null,
    activeId: 0,
    loading: false,
    
  },
  /* 生命周期函数--监听页面加载 */
  onLoad(options) {
    // 创建触控处理对象
    creatTouchController(this, 'touchEvent', 'controlStatus')
    // 获取所有的分组
    this.setData({loading: true})
    getCategorys().then(res=>{  
      this.setData({
        categorys: res.data,
        loading: false,
      })
    })
    app.watch(this, {
      activeId: function(newVal) {
        if(newVal >= 0 && newVal < this.data.categorys.length) {
          if (this.data.categorys[newVal].nameVoice) {
            readController(this.data.categorys[newVal].nameVoice,"voice")
          } else {
            getVoice("分类：" + this.data.categorys[newVal].categoryName).then(res=>{
              var categorys = this.data.categorys
              categorys[newVal].nameVoice = res
              this.setData({categorys: categorys})
              readController(res,"voice")
            })
          }
          // 滑动到指定位置
          wx.pageScrollTo({
            selector: "#item" + parseInt(newVal),
            offsetTop: -150,
          })
        }
      },
      controlStatus: function(newVal) {
        if (newVal == CONTROLSTATUS.up) {
          if (this.data.activeId > 0) {
            readController("voice/home/theLastArticle.mp3","control")
            this.setData({activeId: this.data.activeId - 1})
          } else if (this.data.activeId == 0) {
            readController("voice/categorys/wasTheFirst.mp3","control")
          }
        } else if (newVal == CONTROLSTATUS.down) {
          if (this.data.activeId < this.data.categorys.length - 1) {
            readController("voice/home/nextArticle.mp3","control")
            this.setData({activeId: this.data.activeId + 1})
          } else if (this.data.activeId == this.data.categorys.length - 1) {
            readController("voice/categorys/wasTheLast.mp3","control")
          }
        } else if (newVal == CONTROLSTATUS.left) {
          // 左滑
          wx.switchTab({
            url: '/pages/index/index',
          })
        } else if (newVal == CONTROLSTATUS.right) {
          wx.switchTab({
            url: '/pages/more/more',
          })
        } else if (newVal == CONTROLSTATUS.singleTap) {
          if (this.data.categorys[this.data.activeId].describeVoice) {
            readController(this.data.categorys[this.data.activeId].describeVoice,"voice")
          } else {
            getVoice("单击，简介：" + this.data.categorys[this.data.activeId].describe).then(res=>{
              var categorys = this.data.categorys
              categorys[newVal].describeVoice = res
              this.setData({categorys: categorys})
              readController(res,"voice")
            })
          }
        } else if (newVal == CONTROLSTATUS.doubleTap) {
          app.globalData.categoryData = this.data.categorys[this.data.activeId]
          wx.navigateTo({
            url: "/pages/categoryDetail/categoryDetail",
          })
        } else if (newVal == CONTROLSTATUS.longTapStart) {
          this.setData({activeId: -1})
          readController("voice/tapToTop.mp3", "control")
        }
      }
    })
  },
  /* 生命周期函数--监听页面初次渲染完成 */
  onReady() {},
  /* 生命周期函数--监听页面显示 */
  onShow() {
    initAudioController()
    readController("voice/categorys/categorys.mp3","control")
  },
  /* 生命周期函数--监听页面隐藏 */
  onHide() {},
  /* 生命周期函数--监听页面卸载 */
  onUnload() {},
  /* 用户点击右上角分享 */
  onShareAppMessage() {},
})