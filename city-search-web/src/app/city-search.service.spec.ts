import { TestBed, inject } from '@angular/core/testing';

import { CitySearchService } from './city-search.service';

describe('CitySearchService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [CitySearchService]
    });
  });

  it('should be created', inject([CitySearchService], (service: CitySearchService) => {
    expect(service).toBeTruthy();
  }));
});
