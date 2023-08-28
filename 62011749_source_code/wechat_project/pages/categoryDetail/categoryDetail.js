// pages/categoryDetail/categoryDetail.js
const app = getApp()
import { getArticlesByCategory, getVoice } from "../../utils/request.js"
import {creatTouchController,CONTROLSTATUS } from "../../utils/touch"
import { readController, initAudioController } from "../../utils/audio.js"

Page({
  /* 页面的初始数据 */
  data: {
    categoryData: {type: Object, value: {
      categoryId: String,
      categoryName: String,
      imgUrl: String,
      describe: String,
    }},
    articles: [],
    activeId: -1,
    pageNumber: 1,
    pageSize: 10,
    controlStatus: null,
    loading: false,
    refreshView: false,
  },
  /* 生命周期函数--监听页面加载 */
  onLoad(options) {
    // 创建触控处理对象
    creatTouchController(this, 'touchEvent', 'controlStatus')
    // 监控 activeId controlStatus 的变化
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
        } else if (newVal == -1) {
          if (this.data.categoryData.categoryVoice) {
            readController(this.data.categoryData.categoryVoice,"voice")
          } else {
            getVoice("分类名：" + this.data.categoryData.categoryName + ", 分类简介：" + this.data.categoryData.describe).then(res=>{
              var category = this.data.categoryData
              category.categoryVoice = res
              this.setData({categoryData: category})
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
            console.log("上一篇文章")
            this.setData({activeId: this.data.activeId - 1})
          } else if (this.data.activeId == 0) {
            this.setData({activeId: this.data.activeId - 1})
          } else if (!this.data.refreshView) {
            readController("voice/home/refreshView.mp3","control")
            this.setData({refreshView: true})
          } else if (this.data.refreshView) {
            console.log("刷新界面")
            wx.reLaunch({
              url: '/pages/categoryDetail/categoryDetail',
            })
          }
        } else if (newVal == CONTROLSTATUS.down) {
          if (this.data.activeId == -1) {
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
              getArticlesByCategory(this.data.pageNumber, this.data.pageSize, this.data.categoryData.categoryId).then(res=>{
                if (res.data.length > 0) {
                  this.setData({
                    articles: this.data.articles.concat(res.data),
                    pageNumber: this.data.pageNumber + 1,
                    loading: false
                  })
                  readController("voice/home/loadedForMoreArticles.mp3","control")
                } else {
                  this.setData({loading: false})
                  readController("voice/home/noMoreArticles.mp3","control")
                }
              });
            }
          }
        } else if (newVal == CONTROLSTATUS.left || newVal == CONTROLSTATUS.right) {
          wx.navigateBack({
            success: res=>{
              readController("voice/return.mp3","control")
            }
          })
        } else if (newVal == CONTROLSTATUS.singleTap && this.data.activeId != -1) {
          var summary = this.data.articles[this.data.activeId].newAbstract
          var author =  this.data.articles[this.data.activeId].author.nickname
          readController("voice/singleTapArticle.mp3","control")
          getVoice("作者," + author + "。" + summary).then(res=>{
            readController(res,"voice")
          })
        } else if (newVal == CONTROLSTATUS.doubleTap && this.data.activeId != -1) {
          readController("voice/doubleTapArticle.mp3","control")
          app.globalData.articleData = this.data.articles[this.data.activeId]
          wx.navigateTo({
            url: "/pages/articleView/articleView"
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
    this.setData({
      categoryData: app.globalData.categoryData
    })
    initAudioController()
    if (this.data.categoryData.introduceVoice) {
      readController(this.data.categoryData.introduceVoice, "voice")
    } else {
      console.log(this.data.categoryData.categoryName)
      getVoice("您现在正在分类：" + this.data.categoryData.categoryName + ", 的检索界面，上下滑动收听文章，左右滑动返回分类检索").then(res=>{
        var category = this.data.categoryData
        category.introduceVoice = res
        this.setData({categoryData: category})
        readController(res,"voice")
      })
    }
    getArticlesByCategory(1, this.data.pageSize, this.data.categoryData.categoryId).then(res=>{
      this.setData({
        articles: res.data,
        pageNumber: 2,
      })
    });
  },
  /* 生命周期函数--监听页面隐藏 */
  onHide() {},
  /* 生命周期函数--监听页面卸载 */
  onUnload() {},
  /* 用户点击右上角分享*/
  onShareAppMessage() {}
})