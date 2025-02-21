/**
 封装echarts在vue中使用
 **/

Vue.component('echarts',{
    props:['option','style'],
    data:function () {
        return {}
    },
    mounted:function () {
        this.$nextTick(function (){
            let el = this.$el;
            let chart = echarts.init(el,'macarons');
            chart.setOption(this.option);
            this.chart = chart;
        });
    },
    watch: {
        option: function (newValue,oldValue) {
            // option 发生改变就重新渲染
            this.chart.setOption(newValue);
        }
    },
    template:'<div :style="style">{{ option }}</div>'
})