const firebaseConfig = {
  apiKey: "AIzaSyBAWFGepKYfB24nTs8OBtRtFlKHBNwEqJY",
  authDomain: "point-pay-a430e.firebaseapp.com",
  databaseURL: "https://point-pay-a430e-default-rtdb.firebaseio.com",
  projectId: "point-pay-a430e",
  storageBucket: "point-pay-a430e.appspot.com",
  messagingSenderId: "328769959565",
  appId: "1:328769959565:web:ec32dd56ae45ce5f7ed4c4",
  measurementId: "G-RH6ZSWFPSH",
};
// Initialize Firebase
var point_location;
firebase.initializeApp(firebaseConfig);
var database = firebase.database();
var database_reference = database.ref("NED UET");
let point_list = {};

database_reference
  .get()
  .then((snapshot) => {
    if (snapshot.exists()) {
      data = snapshot.val();
      console.log(data);
      for (let item of Object.entries(data)) {
        let point_no = item[0];
        let object = item[1];
        point_list[point_no] = new google.maps.Marker({
          position: new google.maps.LatLng(object.lat, object.long),
          map: map,
          icon: Icon,
          title: point_no,
        });
      }
    } else {
      console.log("No data available");
    }
  })
  .catch((error) => {
    console.error(error);
  });

database_reference.on("value", (snapshot) => {
  const data = snapshot.val();
  console.log(data);

  for (let item of Object.entries(data)) {
    let point_no = item[0];
    let object = item[1];

    point_list[point_no].setPosition(
      new google.maps.LatLng(object.lat, object.long)
    );
  }
});
