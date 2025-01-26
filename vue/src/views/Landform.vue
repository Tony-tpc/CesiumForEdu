<template>
  <div>
    <div>
      <h1>欢迎来到智能地理微课平台</h1>
      <p>探索地形、气候与知识的奥秘</p>
    </div>
  </div>
</template>

<script setup>
import * as THREE from 'three';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

const geometry = new THREE.BoxGeometry( 1, 1, 1 );
const material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
const cube = new THREE.Mesh( geometry, material );
scene.add( cube );

camera.position.z = 5;

function animate() {
  requestAnimationFrame( animate );
  renderer.render( scene, camera );
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;
}
import WebGL from 'three/addons/capabilities/WebGL.js';

if ( WebGL.isWebGL2Available() ) {

  // Initiate function or other initializations here
  animate();

} else {

  const warning = WebGL.getWebGL2ErrorMessage();
  document.getElementById( 'container' ).appendChild( warning );

}

</script>

<style scoped>

</style>