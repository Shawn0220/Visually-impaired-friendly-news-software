// index.js
// 获取应用实例
import { getArticles, getVoice } from "../../utils/request.js"
import {creatTouchController, CONTROLSTATUS } from "../../utils/touch"
import { readController, initAudioController } from "../../utils/audio.js"

const app = getApp()
Page({
  data: {
    articles: [],
    activeId: -1,
    pageNumber: 1,
    pageSize: 10,
    controlStatus: null,
    searchData: false,
    refreshView: false,
    loading: false
  },
  onShow() {
    // 初始化播放器
    initAudioController()
    readController("voice/home/index.mp3","control")
    if (this.data.activeId == -1) {
      readController("voice/home/locationOnSearch.mp3","control")
    } else {
      if (this.data.articles[this.data.activeId].titleVoice) {
        readController(this.data.articles[this.data.activeId].titleVoice,"voice")
      } else {
          getVoice("文章标题," + this.data.articles[this.data.activeId].newTitle).then(res=>{
            var articles = this.data.articles
            articles[this.data.activeId].titleVoice = res
            this.setData({articles: articles})
            readController(res,"voice")
          })
      }
    }
	},
  onLoad() {
    wx.getSavedFileList({
      success (res) {
        for (let index = 0; index < res.fileList.length - 1; index++) {
          wx.removeSavedFile({
            filePath: res.fileList[index].filePath,
          })
        }
      }
     })
    // 创建触控处理对象
    creatTouchController(this, 'touchEvent', 'controlStatus')
    if (!this.data.loading){
      this.setData({loading: true})
      getArticles(this.data.pageNumber, this.data.pageSize).then(res=>{
        this.setData({
          pageNumber: this.data.pageNumber + 1,
          articles: this.data.articles.concat(res.data),
          loading: false
        })
        readController("voice/home/loadedForMoreArticles.mp3","control")
      });
    }
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
            offsetTop: -300,
          })
        } else if (newVal == -1) {
          readController("voice/search/searchHelp.mp3","voice")
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
            readController("voice/search/search.mp3","control")
            this.setData({activeId: this.data.activeId - 1})
          } else if (!this.data.refreshView) {
            readController("voice/home/refreshView.mp3","control")
            this.setData({refreshView: true})
          } else if (this.data.refreshView) {
            wx.reLaunch({
              url: '/pages/index/index',
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
            if (this.data.searchData) {
              readController("voice/home/noMoreArticles.mp3","control")
            } else if (this.data.loading) {
              readController("voice/home/loading.mp3","control")
            } else {
              readController("voice/home/loading.mp3","control")
              this.setData({loading: true})
              getArticles(this.data.pageNumber, this.data.pageSize).then(res=>{
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
        } else if (newVal == CONTROLSTATUS.left) {
          // 首页左滑
          readController("voice/home/indexLeft.mp3","control")
        } else if (newVal == CONTROLSTATUS.right) {
          wx.switchTab({
            url: '/pages/categories/categories',
          })
        } else if (newVal == CONTROLSTATUS.singleTap && this.data.activeId != -1) {
          var summary = this.data.articles[this.data.activeId].newAbstract
          var author =  this.data.articles[this.data.activeId].author.nickname
          readController("voice/singleTapArticle.mp3","control")
          getVoice("作者," + author + "。" + summary).then(res=>{
            readController(res,"voice")
          })
        } else if (newVal == CONTROLSTATUS.doubleTap && this.data.activeId != -1) {
          app.globalData.articleData = this.data.articles[this.data.activeId]
          wx.navigateTo({
            url: "/pages/articleView/articleView",
          })
        } else if (newVal == CONTROLSTATUS.longTapStart) {
          this.setData({activeId: -1})
        }
      }
    })
  },
  searchArticles: function(event) {
    this.setData({
      searchData: true,
      articles: event.detail.articles
    })
  }
})
