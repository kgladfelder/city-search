import { Component, OnInit, ViewChild } from '@angular/core';
import { CitySearchService } from '../city-search.service';
import { } from '@types/googlemaps';

@Component({
  selector: 'city-search-ui',
  templateUrl: './city-search-ui.component.html',
  styleUrls: ['./city-search-ui.component.css']
})
export class CitySearchUiComponent implements OnInit {

  cities;
  searchCity;
  @ViewChild('gmap') gmapElement: any;
  map: google.maps.Map;
  markers = [];

  constructor(private _citySearch: CitySearchService) { }

  ngOnInit() {
    this.cities = [];
    this.searchCity = "";
    var mapProp = {
      center: new google.maps.LatLng(39.8283, -98.5795),
      zoom: 4,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    this.map = new google.maps.Map(this.gmapElement.nativeElement, mapProp);
  }

  getSearchCities(event) {
    if(event == "") {
      this.clearMapMarkers();
      this.cities = [];
      return;
    }
    
    this._citySearch.getCityNames(event).subscribe(
      data => {
        this.cities = data;
        this.clearMapMarkers(); 
        this.cities.forEach(city => {
          var cityLatLong = {lat: city.latitude, lng: city.longitude};
          var marker = new google.maps.Marker({
            map: this.map,
            position: cityLatLong,
            title: city.city + " " + city.state + " " + city.country
          });
          this.markers.push(marker);
        });
      },
      err => console.error(err),
      () => console.log("Gathered Cities")
    );
  }

  clearMapMarkers() {
    for (var i = 0; i < this.markers.length; i++) {
      this.markers[i].setMap(null);
    }
    this.markers = [];
  }
}
