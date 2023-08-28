<template>
  <div class="dashbord">
    <el-row class="infoCrads">
      <el-col :span="6">
        <div class="cardItem">
          <div class="cardItem_txt">
            <count-to
              class="cardItem_p0 color-green1"
              :startVal="startVal"
              :endVal="release"
              :duration="2000"
            ></count-to>
            <p class="cardItem_p1">文章发布量</p>
          </div>
          <div class="cardItem_icon">
            <i class="el-icon-document color-green1"></i>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="cardItem">
          <div class="cardItem_txt">
            <count-to
              class="cardItem_p0 color-blue"
              :startVal="startVal"
              :endVal="views"
              :duration="2000"
            ></count-to>
            <p class="cardItem_p1">文章浏览量</p>
          </div>
          <div class="cardItem_icon">
            <i class="el-icon-time color-blue"></i>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="cardItem">
          <div class="cardItem_txt">
            <count-to
              class="cardItem_p0 color-red"
              :startVal="startVal"
              :endVal="stars"
              :duration="2000"
            ></count-to>
            <p class="cardItem_p1">文章收藏量</p>
          </div>
          <div class="cardItem_icon">
            <i class="el-icon-magic-stick color-red"></i>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="cardItem">
          <div class="cardItem_txt">
            <count-to
              class="cardItem_p0 color-green2"
              :startVal="startVal"
              :endVal="rank"
              :duration="2000"
            ></count-to>
            <p class="cardItem_p1">作者排名</p>
          </div>
          <div class="cardItem_icon">
            <i class="el-icon-medal color-green2"></i>
          </div>
        </div>
      </el-col>
    </el-row>
    <line-charts class="lCharts" :lineChartData="lineChartData"></line-charts>
  </div>
</template>

<script>
import CountTo from 'vue-count-to'
import LineCharts from './components/LineCharts'
import {getAuthorPreview, getMonthData} from "../../../api/utils";
import {getLineData} from "../../../api/dashboard";
export default {
  data() {
    return {
      startVal: 0,
      release: 0,
      views: 0,
      stars: 0,
      rank: 0,
      tableData: [],
      lineChartData: {},
      barData: {}
    }
  },
  created() {
    this._getAllData()
  },
  components: {
    CountTo,
    LineCharts,
  },
  methods: {
    _getAllData() {
      getMonthData(4).then(res=>{
        this.lineChartData = res.data.data;
      });
      getAuthorPreview().then(res => {
        this.release = res.data.data.release;
        this.views = res.data.data.views;
        this.stars = res.data.data.stars;
        this.rank = res.data.data.rank;
      });
    }
  }
}
</script>
<style scoped lang="scss">
$mgTop: 30px;
@mixin shadow {
  box-shadow: 0 0 10px #e2e2e2;
}
.color-green1 {
  color: #40c9c6 !important;
}
.color-blue {
  color: #36a3f7 !important;
}
.color-red {
  color: #f4516c !important;
}
.color-green2 {
  color: #34bfa3 !important;
}
.dashbord {
  background-color: #f0f3f4;
}
.infoCrads {
  margin: 0 -20px 0 -20px;
  .el-col {
    padding: 0 20px;
    .cardItem {
      height: 108px;
      background: #fff;
    }
  }
}
.cardItem {
  color: #666;
  @include shadow();
  .cardItem_txt {
    float: left;
    margin: 26px 0 0 20px;
    .cardItem_p0 {
      font-size: 20px;
      font-weight: bold;
    }
    .cardItem_p1 {
      font-size: 16px;
    }
  }
  .cardItem_icon {
    float: right;
    margin: 24px 20px 0 0;
    i {
      font-size: 55px;
    }
  }
}
.lCharts {
  background: #fff;
  margin-top: $mgTop;
  padding: 30px 0;
  @include shadow();
}
.barCharts {
  background: #fff;
  margin-top: $mgTop;
  padding: 30px 0;
  @include shadow();
}
.pieCharts {
  background: #fff;
  padding: 20px 0;
  @include shadow();
}
.tableChart {
  margin-top: $mgTop;
}
</style>
