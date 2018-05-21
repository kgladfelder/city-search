import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http'; 

import { AppComponent } from './app.component';
import { CitySearchUiComponent } from './city-search-ui/city-search-ui.component';
import { CitySearchService } from './city-search.service';


@NgModule({
  declarations: [
    AppComponent,
    CitySearchUiComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule
  ],
  providers: [CitySearchService],
  bootstrap: [AppComponent]
})
export class AppModule { }
