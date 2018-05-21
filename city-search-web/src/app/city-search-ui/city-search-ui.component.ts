import { Component, OnInit } from '@angular/core';
import { CitySearchService } from '../city-search.service';

@Component({
  selector: 'city-search-ui',
  templateUrl: './city-search-ui.component.html',
  styleUrls: ['./city-search-ui.component.css']
})
export class CitySearchUiComponent implements OnInit {

  constructor(private _citySearch: CitySearchService) { }

  cities;
  searchCity;

  ngOnInit() {
    this.cities = [];
    this.searchCity = "";
  }

  getSearchCities(event) {
    console.log(event);
    if(event == "") {
      this.cities = [];
      return;
    }
    
    this._citySearch.getCityNames(event).subscribe(
      data => { this.cities = data },
      err => console.error(err),
      () => console.log("Gathered Cities")
    );
  }
}
