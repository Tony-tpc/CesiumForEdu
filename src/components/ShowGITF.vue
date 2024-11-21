<template>
  <div id="cesiumContainer">
  </div>
</template>
<script setup>
import { onMounted } from "vue";
import * as Cesium from 'cesium';

onMounted(() => {
  const modelUrl = '/models/snowy_mountains.glb';
  // const modelUrl = '/models/canyon_and_mountains_gltf/scene.gltf';
  // "D:\Yang\html\models\canyon_and_mountains_gltf\scene.gltf"
  let viewer = new Cesium.Viewer('cesiumContainer', {
    homeButton: false, //主页按钮
    baseLayerPicker: false, //是否显示图层选择控件
    navigationHelpButton: true, //帮助信息按钮
    geocoder: true, //是否显示地名查找控件
    terrainProvider: new Cesium.EllipsoidTerrainProvider(), // 使用椭球地形
  });
  viewer._cesiumWidget._creditContainer.style.display = "none";
  viewer.scene.globe.show = false;
  viewer.scene.skyBox.destroy();
  viewer.scene.skyBox = undefined;
  viewer.scene.sun.destroy();
  viewer.scene.sun = undefined;
  viewer.scene.moon.destroy();
  viewer.scene.moon = undefined;
  viewer.scene.skyAtmosphere.destroy();
  viewer.scene.skyAtmosphere = undefined;
  viewer.scene.debugShowFramesPerSecond = true;
  viewer.scene.backgroundColor = new Cesium.Color(10, 10, 10, 1);

  // 设置模型的初始位置
  var position = Cesium.Cartesian3.fromDegrees(10, 10, 100); // 经度、纬度、海拔高度
  var heading = Cesium.Math.toRadians(45); // 头朝向
  var pitch = 0; // 俯仰角
  var roll = 0; // 滚动角
  var hpr = new Cesium.HeadingPitchRoll(heading, pitch, roll);
  // 获取正确的矩阵来定位模型
  var modelMatrix = Cesium.Transforms.headingPitchRollToFixedFrame(position, hpr);


  // 使用 Cesium.Model 加载 GLTF 模型
  Cesium.Model.fromGltfAsync({    // url: 'cesium/Specs/Data/Models/glTF-2.0/BoxWithCopyright/glTF/Box.gltf',  // 替换为本地GLTF文件的路径
    url: modelUrl,  // 替换为本地GLTF文件的路径
    modelMatrix: modelMatrix,
    scale: 5 // 调整模型的比例
  }).then(function (model) {


    if (model) {
      viewer.scene.primitives.add(model);

      // 使用 setTimeout 循环检查 model.ready
      function checkModelReady() {
        if (model.ready) {
          var boundingSphere = model.boundingSphere;

          // 自动飞到模型位置
          viewer.camera.flyToBoundingSphere(boundingSphere, {
            duration: 0.5,
            offset: new Cesium.HeadingPitchRange(
              0,
              Cesium.Math.toRadians(-30),
              boundingSphere.radius * 3.0
            )
          });
          viewer.camera.lookAt(position, new Cesium.HeadingPitchRange(
            0,  // 头朝向（heading）
            0,  // 俯仰角（pitch）
            -10,
          ));
        } else {
          // 如果模型还没准备好，继续等待
          setTimeout(checkModelReady, 100); // 每 100 毫秒检查一次
        }
      }

      // 启动检查模型是否准备好的过程
      checkModelReady();
    } else {
      console.error('模型未定义');
    }
  }).catch(function (error) {
    console.error('模型加载失败:', error);
  });
})
</script>
<style>
#cesiumContainer {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
</style>
