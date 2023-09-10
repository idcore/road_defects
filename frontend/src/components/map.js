import React, {useState} from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap, ImageOverlay, AttributionControl, Tooltip } from "react-leaflet";
import {Form} from 'react-bootstrap';
import http from "../http-common";
import { useEffect } from 'react';

const test_markers = [
  { id: 1, lng: 37.388727, lat: 55.682072, text: 'Дефект: 55.682072, 37.388727'}
];


async function fetchData() {
  const apiUrl = '/image-data/potholes/all';

  const response = await  http.get(apiUrl).catch((error) => {
      console.error('Error fetching data:', error);
    });
    if (response)
    {
      return response.data;
    }
};

const _test_markers_and_texts = test_markers.map((obj) => ({
  ...obj, // Copy existing properties
  text: 'Дефект ' & obj.lng  & ',' & obj.lat, // Calculate the sum and add it as a new property
}));


export const Map = () => {


  const position = [55.455, 37.458]; // [latitude, longitude]
  const zoomLevel = 13;

  const [isCheckedId1, setIsCheckedId1] = useState(true);
  const [isCheckedId2, setIsCheckedId2] = useState(false);
  const [isCheckedId3, setIsCheckedId3] = useState(true);

  const [markers, setMarkers] = useState([]);

  // Your GPS setter function
  const setGps = (x, y) => {
    // Create a new mark object and append it to the marks array
    setMarkers([...markers, { x, y }]);
  };  



   // Define the useEffect to fetch data when the component mounts
  // Call fetchData when the component mounts and whenever you want to refresh
  // useEffect(() => {
  //   async function fetchDataAndUpdateMap() {
  //     const data = await fetchData();
  //     if (data) {
  //       // Process the images and call the setGps function for each image
  //       data.forEach((image) => {
  //         const [x, y] = image.gps; // Extract the GPS coordinates
  //         setGps(x, y); // Call the setter function
  //       });

  //     }

      
  //   }
  // fetchDataAndUpdateMap();
  // }, []);



  const handleSwitchChangeId1 = (e) => {
    setIsCheckedId1(e.target.checked);
    
    // You can perform additional actions here when the switch state changes
    // For example, make an API request, update other parts of your UI, etc.
    console.log('Switch state changed Id1:', e.target.checked);
  };

  const handleSwitchChangeId2 = (e) => {
    setIsCheckedId2(e.target.checked);
    
    // You can perform additional actions here when the switch state changes
    // For example, make an API request, update other parts of your UI, etc.
    console.log('Switch state changed Id2:', e.target.checked);
  };

  const handleSwitchChangeId3 = (e) => {
    setIsCheckedId3(e.target.checked);
    
    // You can perform additional actions here when the switch state changes
    // For example, make an API request, update other parts of your UI, etc.
    console.log('Switch state changed Id3:', e.target.checked);
  };



 
  return (
    <div>
    <Form>
    
    <Form.Check
      type="switch"
      id="custom-switch"
      label="Дефекты"
      checked={isCheckedId1}
      onChange={handleSwitchChangeId1}
      inline
    />
    
    
    <Form.Check
      type="switch"
      id="custom-switch"
      label="Контрольные процедуры"
      checked={isCheckedId2}
      
      onChange={handleSwitchChangeId2}
      inline
    />
    
    


  </Form>


    <MapContainer 
        center={position} 
        zoom={zoomLevel} 
        scrollWheelZoom={false}
        attributionControl={false}
    >
    {test_markers.map((marker) => (
    <Marker
      key={marker.id}
      position={[marker.lat, marker.lng]}
    >
      <Tooltip>{marker.text}</Tooltip> {/* Add a Tooltip component */}
      <Popup>
        <div>{marker.text}</div>
      </Popup>
    </Marker>
  ))}
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
      />
      <AttributionControl position="bottomright" prefix={false} />
    </MapContainer>
    </div>
  );
};