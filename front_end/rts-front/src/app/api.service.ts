import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';
import { Http } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';

const API_URL = environment.apiUrl;
const SUBMIT_ENDPOINT = environment.submitEndpoint;

@Injectable()
export class ApiService {
  public data: Object;
  constructor(private http: Http) {
    this.data = {};
   }

  public submitImage(image: any): Observable<any> {
    this.data['image'] = image;
    return this.http
    .post(API_URL + SUBMIT_ENDPOINT, this.data)
    .map(response => {
      return response;
    });
  }
}
