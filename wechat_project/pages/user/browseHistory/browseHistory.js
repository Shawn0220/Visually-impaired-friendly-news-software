// pages/user/browseHistory/browseHistory.js
import { getVoice,getBrowsingHistory } from "../../../utils/request.js"
import {creatTouchController,CONTROLSTATUS } from "../../../utils/touch"
import { readController, initAudioController } from "../../../utils/audio.js"
const app = getApp()
Page({
  /**
   * 页面的初始数据
   */
  data: {
    articles: [],
    activeId: 0,
    pageNumber: 1,
    pageSize: 10,
    controlStatus: null,
    loading: false,
    refreshView: false,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    // 创建触控处理对象
    creatTouchController(this, 'touchEvent', 'controlStatus')
    getBrowsingHistory(this.data.pageNumber, this.data.pageSize).then(res=>{
      this.setData({
        articles: res.data,
        pageNumber: this.data.pageNumber + 1,
      })
    })
    app.watch(this, {
      activeId: function(newVal) {
        if(newVal >= 0 && newVal < this.data.articles.length) {
          if (this.data.articles[newVal].titleVoice) {
            readController(this.data.articles[newVal].titleVoice,"voice")
          } else {
              getVoice("文章标题," + this.data.articles[newVal].newTitle).then(res=>{
                var articles = this.data.articles
                articles[newVal].titleVoice = res
                this.setData({articles: articles})
                readController(res,"voice")
              })
          }
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
            if (!this.data.refreshView) {
              readController("voice/home/refreshView.mp3","control")
              this.setData({refreshView: true})
            } else if (this.data.refreshView) {
              wx.reLaunch({
                url: '/pages/user/browseHistory/browseHistory',
              })
            }
          }
        } else if (newVal == CONTROLSTATUS.down) {
          if (this.data.activeId == 0) {
            this.setData({ refreshView: false})
          }
          if (this.data.activeId < this.data.articles.length - 1) {
            readController("voice/home/nextArticle.mp3","control")
            this.setData({activeId: this.data.activeId + 1})
          } else if (this.data.activeId == this.data.articles.length - 1) {
            if (this.data.loading) {
              readController("voice/home/loading.mp3","control")
            } else {
              readController("voice/home/loading.mp3","control")
              this.setData({loading: true})
              getBrowsingHistory(this.data.pageNumber, this.data.pageSize).then(res=>{
                if (res.data.length > 0) {
                  this.setData({ 
                    articles: this.data.articles.concat(res.data),
                    pageNumber: this.data.pageNumber + 1,
                    loading: false
                  })
                  readController("voice/home/loadedForMoreArticles.mp3","control")
                } else {
                  readController("voice/home/noMoreArticles.mp3","control")
                }
              })
            }
          }
        } else if (newVal == CONTROLSTATUS.left || newVal == CONTROLSTATUS.right) {
          wx.navigateBack({
            success: res=>{
              readController("voice/return.mp3","control")
            }
          })
        } else if (newVal == CONTROLSTATUS.singleTap) {
          var summary = this.data.articles[this.data.activeId].newAbstract
          var author =  this.data.articles[this.data.activeId].author.nickname
          readController("voice/singleTapArticle.mp3","control")
          getVoice("作者," + author + "。" + summary).then(res=>{
            readController(res,"voice")
          })
        } else if (newVal == CONTROLSTATUS.doubleTap) {
          readController("voice/doubleTapArticle.mp3","control")
          app.globalData.articleData = this.data.articles[this.data.activeId]
          wx.navigateTo({
            url: "/pages/articleView/articleView"
          })
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
    initAudioController()
    readController("voice/browse/browseHistory.mp3", "control")
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

  }
})