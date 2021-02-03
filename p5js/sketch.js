

let CELL = 8;
let X_DIM = 125;
let Y_DIM = 60;
let WATER = 0;
let LAND = 1;
let VEHICLE = 2;

let earthquakes;
function preload() {
  // Get the most recent earthquake in the database
  let url =
   'http://localhost:5000/vehicles';
  httpGet(url, 'jsonp', false, function(response) {
    earthquakes = response;
    console.log(earthquakes)
  });
}

function setup() {
  console.log('Wa-Tor');
  X_DIM = Math.round((windowWidth - 20) / CELL);
  Y_DIM = Math.round((windowHeight - 20) / CELL);
  createCanvas(CELL * X_DIM, CELL * Y_DIM);
  setupWorld();
  textFont('monospace');
}

function setupWorld() {
  iteration = 0;
  background(0, 0, 0);
  data = new Array(X_DIM);
  for (x = 0; x < X_DIM; x++) {
    data[x] = new Array(Y_DIM);
    for (y = 0; y < Y_DIM; y++) {
      data[x][y] = WATER;
      if (Math.random() < 0.5) {
        data[x][y] = LAND;
      }
      if (Math.random() < 0.01) {
        data[x][y] = VEHICLE;
      }
    }
  }
}

function draw() {
  for (x = 0; x < X_DIM; x++) {
    for (y = 0; y < Y_DIM; y++) {
      switch (data[x][y]) {
        case WATER:
          // fill(0, 0, 200);
          // stroke(0, 0, 200);
          // break;
        case LAND:
          fill(200,200,200);
          stroke(200,200,200);
          break;
        case VEHICLE:
          fill(180, 0, 0);
          stroke(255, 0, 0);
          break;
      }
      rect(x * CELL, y * CELL, CELL, CELL);
    }
  }
}