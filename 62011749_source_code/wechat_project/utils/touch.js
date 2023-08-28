import MinaTouch from './mina-touch/mina-touch.js';

const app = getApp()
export const CONTROLSTATUS = {
  null: 0,
  up: 1,
  down: 2,
  left: 3,
  right: 4,
  singleTap: 5,
  doubleTap: 6,
  longTapStart: 7,
  longTapEnd: 8,
  cancel: 9,
}

export function getDirection(x, y) {
  let dx = x - app.globalData.location.x;
  let dy = y - app.globalData.location.y;
  if (Math.abs(dy) >= wx.getSystemInfoSync().windowHeight * 0.05) {
    if (dy < 0){  // 上
      return "up"
    } else if (dy > 0) {  // 下
      return "down"
    } 
  } else if (Math.abs(dx) > wx.getSystemInfoSync().windowWidth * 0.2) {
    if (dx < 0) { // 左
      return "left"
    } else if (dx > 0) {  // 右
      return "right"
    }
  } else {
    return null
  }
}

export function creatTouchController(that, controller, status) {
    var longTap = false;
    return new MinaTouch(that, controller, {
      // 创建this.touch指向实例对象
      touchStart: function () {
        longTap = false;
      },
      touchMove: function () {},
      touchEnd: function () {
        if(longTap) {   // 长按结束
          that.setData({[status]: CONTROLSTATUS.longTapEnd})
          return
        }
      },
      touchCancel: function () {
        that.setData({[status]: CONTROLSTATUS.cancel})
      },
      //一个手指以上触摸屏幕触发
      multipointStart: function () {}, 
      //当手指离开，屏幕只剩一个手指或零个手指触发(一开始只有一根手指也会触发)
      multipointEnd: function () {}, 
      //点按触发，覆盖下方3个点击事件，doubleTap时触发2次
      tap: function () {}, 
      //双击屏幕触发
      doubleTap: function () {
        console.log('doubleTap' + 'touchtouchtouchtouchtouchtouchtouchtouch')
        that.setData({[status]: CONTROLSTATUS.doubleTap})
      },
      //长按屏幕750ms触发
      longTap: function () {
        longTap = true
        that.setData({[status]: CONTROLSTATUS.longTapStart})
      },
      //单击屏幕触发，不包括长按
      singleTap: function () {
        if(!longTap) {
          that.setData({[status]: CONTROLSTATUS.singleTap})
        }
      }, 
      //evt.angle代表两个手指旋转的角度
      rotate: function (evt) {},
      //evt.zoom代表两个手指缩放的比例(多次缩放的累计值),evt.singleZoom代表单次回调中两个手指缩放的比例
      pinch: function (evt) {},
      //evt.deltaX和evt.deltaY代表在屏幕上移动的距离,evt.target可以用来判断点击的对象
      pressMove: function (evt) {},
      //在touch结束触发，evt.direction代表滑动的方向 ['Up','Right','Down','Left']
      swipe: function (evt) {
        if(!longTap){
          if (evt.direction == 'Up') {
            that.setData({[status]: CONTROLSTATUS.up})
          } else if (evt.direction == 'Down') {
            that.setData({[status]: CONTROLSTATUS.down})
          } else if (evt.direction == 'Left') {
            that.setData({[status]: CONTROLSTATUS.left})
          } else if (evt.direction == 'Right') {
            that.setData({[status]: CONTROLSTATUS.right})
          }
        }
      },
    });
}

