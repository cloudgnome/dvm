var lat;
var lng;
function initMap() {
	var map = new google.maps.Map(document.getElementById('map'), {
		center: {lat: lat ? lat : -33.8688, lng: lng ? lng : 151.2195},
		zoom: 13
	});
	var card = document.getElementById('pac-card');
	var input = document.getElementById('id_location_text');
	var types = document.getElementById('type-selector');
	var strictBounds = document.getElementById('strict-bounds-selector');

	map.controls[google.maps.ControlPosition.TOP_RIGHT].push(card);

	var autocomplete = new google.maps.places.Autocomplete(input);

	autocomplete.bindTo('bounds', map);

	autocomplete.setFields(
		['address_components', 'geometry', 'icon', 'name','place_id']);

	var infowindow = new google.maps.InfoWindow();
	var infowindowContent = document.getElementById('infowindow-content');
	infowindow.setContent(infowindowContent);
	var marker = new google.maps.Marker({
		map: map,
		anchorPoint: new google.maps.Point(0, -29)
	});

	autocomplete.addListener('place_changed', function() {
		infowindow.close();
		marker.setVisible(false);
		var place = autocomplete.getPlace();
		if (!place.geometry) {
			window.alert("No details available for input: '" + place.name + "'");
			return;
		}

		if (place.geometry.viewport) {
		map.fitBounds(place.geometry.viewport);
		} else {
		map.setCenter(place.geometry.location);
		map.setZoom(17);
		}
		marker.setPosition(place.geometry.location);
		marker.setVisible(true);

		var address = '';
		if (place.address_components) {
		address = [
			(place.address_components[0] && place.address_components[0].short_name || ''),
			(place.address_components[1] && place.address_components[1].short_name || ''),
			(place.address_components[2] && place.address_components[2].short_name || '')
		].join(' ');
		}

		infowindowContent.children['place-icon'].src = place.icon;
		infowindowContent.children['place-name'].textContent = place.name;
		infowindowContent.children['place-address'].textContent = address;
		infowindow.open(map, marker);

		log(place);

		if(!Array.isArray($('#id_place_id')))
			$('#id_place_id').value = place.place_id;

		if(!Array.isArray($('#id_location_lat')))
			$('#id_location_lat').value = place.geometry.location.lat();

		if(!Array.isArray($('#id_location_lng')))
			$('#id_location_lng').value = place.geometry.location.lng();
	});

	function setupClickListener(id, types) {
		var radioButton = document.getElementById(id);
		radioButton.addEventListener('click', function() {
		autocomplete.setTypes(types);
		});
	}

	setupClickListener('changetype-all', []);
	setupClickListener('changetype-address', ['address']);
	setupClickListener('changetype-establishment', ['establishment']);
	setupClickListener('changetype-geocode', ['geocode']);

	document.getElementById('use-strict-bounds')
		.addEventListener('click', function() {
			console.log('Checkbox clicked! New state=' + this.checked);
			autocomplete.setOptions({strictBounds: this.checked});
		});
	}