// components/articleItem/articleItem.js
import {formatTimeByString} from "../../utils/time"
Component({
  /* 组件的属性列表 */
  properties: {
    articleData: {type: Object, value: {
      newId: String,	      // 文章唯一标识符
      newTitle: String,	    // 标题
      newAbstract: String,  // 摘要
      newContent: String,   // 文章内容
      author: {           // 作者信息
        writerId: String,
        writerAccount: String,
        nickname: String,
      },
      createDate: String,      // 文章的创建时间
      tags: Array,        // 标签数组
      category: {        // 分类
        categoryId: String,
        categoryName: String
      },
      views: Number,	    // 浏览量
      stars: Number,	    // 收藏量
      weight: Number,      // 推荐度
      titleVoice: String  // 标题语音文件
    }},
    myStyle:String
  },
  /* 组件的初始数据 */
  data: {
    loading: true,
  },
  methods: {}
})
