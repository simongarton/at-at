

let CELL = 8;
let X_DIM = 125;
let Y_DIM = 60;
let WATER = 0;
let LAND = 1;
let VEHICLE = 2;

let vehicles;
let loaded = false;
let mapData;

function preload() {
  let url ='http://localhost:5000/vehicles';
  httpGet(url).then(function(vehicleData) {
    console.log("got vehicle data");
    setupWorld()
    processVehicles(vehicleData);
    loaded = true;
  })
}

function processVehicles(vehicleData) {
  jsonData = JSON.parse(vehicleData)
  print(jsonData.length + " vehicles")
  vehicles = jsonData
  // E 1,700,000 - 1,800,000 : 100,000
  // N 5,900,000 - 6,000,000 : 100,000
  const left = 1700000
  const bottom = 5900000
  const right = 1800000
  const top = 6000000
  const width = right - left
  const height = top - bottom
  for (const vehicle of vehicles) {
    let easting = ((vehicle.easting - left)/ width) * (CELL * X_DIM)
    let northing = ((vehicle.northing - bottom)/ height) * (CELL * Y_DIM)
    // console.log(vehicle.easting + "," + vehicle.northing);
    // console.log(easting + "," + northing);
    let cellx = int(easting / CELL)
    let celly = int(northing / CELL)
    // console.log(cellx + "," + celly);
    if (cellx >= 0 && cellx < X_DIM && celly > 0 && celly < Y_DIM) {
      console.log("setting " + cellx + "," + celly)
      data[cellx][celly] = VEHICLE
    }
  }
  console.log(data)
}

function setup() {
  console.log('Wa-Tor');
  X_DIM = Math.round((windowWidth - 20) / CELL);
  Y_DIM = Math.round((windowHeight - 20) / CELL);
  createCanvas(CELL * X_DIM, CELL * Y_DIM);
}

function setupWorld() {
  iteration = 0;
  background(0, 0, 0);
  data = new Array(X_DIM);
  for (x = 0; x < X_DIM; x++) {
    data[x] = new Array(Y_DIM);
    for (y = 0; y < Y_DIM; y++) {
      data[x][y] = LAND;
    }
  }
}

function draw() {
  if (!loaded) {
    return
  }
  for (x = 0; x < X_DIM; x++) {
    for (y = 0; y < Y_DIM; y++) {
      switch (data[x][y]) {
        case WATER:
          fill(0, 0, 200);
          stroke(0, 0, 200);
          break;
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