import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CitySearchUiComponent } from './city-search-ui.component';

describe('CitySearchUiComponent', () => {
  let component: CitySearchUiComponent;
  let fixture: ComponentFixture<CitySearchUiComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CitySearchUiComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CitySearchUiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
