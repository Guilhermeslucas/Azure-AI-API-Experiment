import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';
import { Http } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';

const API_URL = environment.apiUrl;
const SUBMIT_ENDPOINT = environment.submitEndpoint;

@Injectable()
export class ApiService {

  constructor(private http: Http) { }

  public submitImage(image_link: string) {
    console.log('Entrei aqui');
    return this.http
    .post(API_URL + SUBMIT_ENDPOINT, image_link)
    .map(response => {
      return response;
    });
  }
}
