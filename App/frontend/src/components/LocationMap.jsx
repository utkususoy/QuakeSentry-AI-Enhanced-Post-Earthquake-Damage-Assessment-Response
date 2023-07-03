import React, { useEffect, useState } from "react";
import axios from "axios";
import { MapContainer, TileLayer, Marker, Popup, GeoJSON } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import markerRed from './red_v2.png';
import markerBlue from './blue_v2.png';
import turkey from './turkey.geojson.json'; // path to the GeoJSON data
//import MarkerClusterGroup from 'react-leaflet-markercluster';
import MarkerClusterGroup from 'react-leaflet-markercluster';
import ReconnectingWebSocket from 'reconnecting-websocket';



export default function LocationMap() {
  const [locations, setLocations] = useState([]);
  const [selectedOption, setSelectedOption] = useState('');
  // ws deneme
  const [messages, setMessages] = useState([]);
  
  useEffect(() => {
    // TODO: Açılışta getLocations çalışmıyor datalar db den yüklenmiyor.
    getLocations();
    const socket = new ReconnectingWebSocket('ws://localhost:8000/ws');

    socket.onmessage = (event) => {
      const jsonData = JSON.parse(event.data);
      setLocations((prevMessages) => [...prevMessages, jsonData]);
    };

    // socket.onclose = () => {
    //   console.log("WebSocket connection closed");
    //   // Trigger the reconnection process
    //   socket.reconnect();
    // };

    return () => {
      socket.close();
    };
  }, []);

  console.log(locations)

  const handleChange = (event) => {
    setSelectedOption(event.target.value);
  };

  // TODO: Only webapp openning load data(not page load) otherwise get data only with websocket.
  const getLocations = async () => {
    const response = await axios.get(`http://localhost:8000/locations`);
  // TODO: AÇ Orjinalde 
    setLocations(response.data);
  };

  // Custom icon for the map marker
  const mapMarkerIcon = (color) =>
    L.divIcon({
      className: 'custom-icon',
      html: `<img src=${color == 'violent' ? markerRed : markerBlue} width="32" height="32">`,
      iconSize: [32, 32],
      iconAnchor: [16, 32],
    });

  const updateTweetType = async (tweetId, newType) => {
    console.log("hereeeeeeeeeee")
    console.log(tweetId)
    console.log(newType)
    setSelectedOption('');
    try {
      console.log(tweetId)
      await axios.post(`http://localhost:8000/change-tweet-type`, {
        tweet_uuid: tweetId,
        label: newType
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      // Update the locations array to reflect the removal
     
        setLocations(prevItems =>
        prevItems.map(item => {
          if (item.uuid === tweetId) {
            console.log(item);
            return { ...item, label: newType };
          }
          return item;
        }));


    } catch (error) {
      console.error('Error removing tweet:', error);
    }
  };

  // const handleRemoveTweet = async (tweetId) => {
  //   setSelectedOption('');
  //   try {
  //     console.log(tweetId)
  //     await axios.post(`http://localhost:8000/remove-tweet`, { tweet_uuid_: tweetId });
  //     console.log(`Tweet with index ${tweetId} removed successfully.`);
  //     // Update the locations array to reflect the removal
  //     setLocations((prevLocations) =>
  //       prevLocations.filter((item) => item.uuid !== tweetId)
  //     );
  //   } catch (error) {
  //     console.error('Error removing tweet:', error);
  //   }
  // };

  // const showRemoveConfirmation = (tweetIndex) => {
  //   if (window.confirm('Are you sure you want to remove this tweet?')) {
  //     handleRemoveTweet(tweetIndex);
  //   }
  // };

  return (
    <MapContainer center={[36.564232, 36.153983]} zoom={8} style={{ height: '100vh' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='Map data © <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
      />
      <GeoJSON data={turkey} />
      {/* Loop through the locations array and create a Marker component for each location */}
      {/* <MarkerClusterGroup> */}
      {locations.map((item, index) => {
      if (item.label !== "none") {
        return (
          <Marker
            key={index}
            position={[parseFloat(item.geo_code[0]), parseFloat(item.geo_code[1])]}
            icon={mapMarkerIcon(item.label)}
          >
            <Popup>
              <span style={{ fontWeight: 'bold', fontSize: '16px' }}>Tweet:</span> <span style={{fontSize: '16px'}}>{item.raw_tweet}</span> <br /><br />
              {/* p_tweet: {item.social_processed_tweet}<br /><br /> */}
              <span style={{ fontWeight: 'bold', fontSize: '16px' }}>Label:</span> <span style={{fontSize: '16px'}}>{item.label}</span> <br/>
              <span style={{ fontWeight: 'bold', fontSize: '16px' }}>NER-Address:</span> <span style={{fontSize: '16px'}}>{item.address}</span> <br/>
              <span style={{ fontWeight: 'bold', fontSize: '16px' }}>Address:</span> <span style={{fontSize: '16px'}}>{item.valid_address}</span> <br/><br/>
              <div>
                <select value={selectedOption === '' ? item.label : selectedOption} onChange={handleChange}>
                  <option value="none">None</option>
                  <option value="weak">Weak</option>
                  <option value="violent">Violent</option>
                </select>
              </div>
              {/* <button onClick={() => showRemoveConfirmation(item.uuid)}>Remove Tweet</button> */}
              <button onClick={() => updateTweetType(item.uuid, selectedOption)}>Change Label</button>
            </Popup>
          </Marker>
        );
      }
  return null;
})}
      {/* </MarkerClusterGroup> */}
      
    </MapContainer>
  );
}
