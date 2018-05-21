import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {Observable} from 'rxjs/Observable';

const httpOptions = {
  headers: new HttpHeaders({ 
    'Access-Control-Allow-Origin':'*',
    'Content-Type': 'application/json'})
};

@Injectable()
export class CitySearchService {

  constructor(private _http:HttpClient) { }

  getCityNames(search: string) {
    return this._http.get('http://localhost:5000/cities?like=' + search);
  }
}
