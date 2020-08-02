<template>
  <div id="app">
    <div id="container" style="width:100%; height:600px"></div>
  </div>
</template>


<script>
  import BMap from 'BMap'
  import axios from 'axios'
  import echarts from 'echarts'
  import PytApi from '@/api/python'

  require('echarts/extension/bmap/bmap')

  export default {
    name: 'showEchart',
    comments: {},
    data() {
      return {
        utili_data: null,
        //timer : null,
        all_gps_data: null,
        index: 0,
        car_num: 0,

        option: {
          bmap: {
            //center: [118.860488, 32.068079],
            zoom: 0,
            roam: true,
            mapStyle: {
              'styleJson': [
                {
                  'featureType': 'water',
                  'elementType': 'all',
                  'stylers': {
                    'color': '#031628'
                  }
                },
                {
                  'featureType': 'land',
                  'elementType': 'geometry',
                  'stylers': {
                    'color': '#000102'
                  }
                },
                {
                  'featureType': 'highway',
                  'elementType': 'all',
                  'stylers': {
                    'visibility': 'off'
                  }
                },
                {
                  'featureType': 'arterial',
                  'elementType': 'geometry.fill',
                  'stylers': {
                    'color': '#000000'
                  }
                },
                {
                  'featureType': 'arterial',
                  'elementType': 'geometry.stroke',
                  'stylers': {
                    'color': '#0b3d51'
                  }
                },
                {
                  'featureType': 'local',
                  'elementType': 'geometry',
                  'stylers': {
                    'color': '#000000'
                  }
                },
                {
                  'featureType': 'railway',
                  'elementType': 'geometry.fill',
                  'stylers': {
                    'color': '#000000'
                  }
                },
                {
                  'featureType': 'railway',
                  'elementType': 'geometry.stroke',
                  'stylers': {
                    'color': '#08304b'
                  }
                },
                {
                  'featureType': 'subway',
                  'elementType': 'geometry',
                  'stylers': {
                    'lightness': -70
                  }
                },
                {
                  'featureType': 'building',
                  'elementType': 'geometry.fill',
                  'stylers': {
                    'color': '#000000'
                  }
                },
                {
                  'featureType': 'all',
                  'elementType': 'labels.text.fill',
                  'stylers': {
                    'color': '#857f7f'
                  }
                },
                {
                  'featureType': 'all',
                  'elementType': 'labels.text.stroke',
                  'stylers': {
                    'color': '#000000'
                  }
                },
                {
                  'featureType': 'building',
                  'elementType': 'geometry',
                  'stylers': {
                    'color': '#022338'
                  }
                },
                {
                  'featureType': 'green',
                  'elementType': 'geometry',
                  'stylers': {
                    'color': '#062032'
                  }
                },
                {
                  'featureType': 'boundary',
                  'elementType': 'all',
                  'stylers': {
                    'color': '#465b6c'
                  }
                },
                {
                  'featureType': 'manmade',
                  'elementType': 'all',
                  'stylers': {
                    'color': '#022338'
                  }
                },
                {
                  'featureType': 'label',
                  'elementType': 'all',
                  'stylers': {
                    'visibility': 'off'
                  }
                }
              ]
            }
          },


          series: [{
            type: 'lines',
            coordinateSystem: 'bmap',
            polyline: true,
            data: this.makeMapData,
            silent: true,
            lineStyle: {
              // color: '#c23531',
              // color: 'rgb(200, 35, 45)',
              opacity: 0.5,
              width: 1,
            },
            progressiveThreshold: 500,
            progressive: 200
          }, {
            type: 'lines',
            coordinateSystem: 'bmap',
            polyline: true,
            data: this.makeMapData,
            lineStyle: {
              width: 0,
            },
            effect: {
              constantSpeed: 50,
              show: true,
              trailLength: 0.1,
              symbolSize: 1.5,
              color: '#4a8fff',
            },
            zlevel: 1
          },
          ]
        }
      }
    },

    methods: {
      makeMapData() {
        let _this = this
        PytApi.get('/res_data/gps').then(response => {
          var hStep = 300 / (response.data.length - 1);
          if (response.status == 200) {
            var order_line = [].concat.apply([], response.data.map(function (order_line, idx) {
              let prevPt;
              let points = [];
              for (let i = 0; i < order_line.length; i += 2) {
                let pt = [order_line[i], order_line[i + 1]];
                if (i > 0) {
                  pt = [
                    prevPt[0] + pt[0],
                    prevPt[1] + pt[1]
                  ];
                }
                prevPt = pt;
                points.push([pt[0], pt[1]]);
              }

              return {
                coords: points,
                lineStyle: {
                  normal: {
                    //color: '#ffffff'
                    color: echarts.color.modifyHSL('#5A94DF', Math.round(hStep * idx))
                  }
                }
              };
            }));
          }

          _this.option.series[0].data = order_line;
          _this.option.series[1].data = order_line;
          let myChart = echarts.init(document.getElementById('container'))
          myChart.setOption(this.option)
        })
      },

      resizeMap() {
        this.resizefun = () => {
          this.$echarts.init(document.getElementById('container')).resize()
        }
        window.addEventListener('resize', this.resizefun)
      }
    },

    mounted() {
      this.resizeMap();
      this.makeMapData();
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2 {
    font-weight: normal;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  a {
    color: #42b983;
  }
</style>
