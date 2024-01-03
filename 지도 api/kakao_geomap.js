var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = { 
        center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심좌표
        level: 6 // 지도의 확대 레벨 
    }; 

var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

// 마커 이미지를 생성합니다
var imageSrc = 'https://youip.net/images/marker_kakao.png', // 마커이미지의 주소입니다    
    imageSize = new kakao.maps.Size(50, 65), // 마커이미지의 크기입니다
    imageOption = {offset: new kakao.maps.Point(27, 69)}; // 마커이미지의 옵션입니다. 마커의 좌표와 일치시킬 이미지 안에서의 좌표를 설정합니다.

var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imageOption);

// 마커를 생성합니다
var marker = new kakao.maps.Marker({
    position: mapOption.center,
    image: markerImage // 마커이미지 설정 
});

// 마커가 지도 위에 표시되도록 설정합니다
marker.setMap(map);

function getLocation() {
    // HTML5의 geolocation으로 사용할 수 있는지 확인합니다 
    if (navigator.geolocation) {
        // GeoLocation을 이용해서 접속 위치를 얻어옵니다
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat = position.coords.latitude, // 위도
                lon = position.coords.longitude; // 경도
            var locPosition = new kakao.maps.LatLng(lat, lon); // 마커가 표시될 위치를 geolocation으로 얻어온 좌표로 생성합니다
            // 마커 위치를 설정합니다
            marker.setPosition(locPosition);
            // 지도 중심좌표를 접속위치로 변경합니다
            map.setCenter(locPosition); 
        });
    } else { 
        // GeoLocation을 사용할 수 없을 때 기본 마커 위치를 설정합니다
        // 이미 생성한 마커를 지도 위에 표시합니다
        marker.setMap(map);
    } 
}
