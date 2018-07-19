import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  public imageUrl: string;
  constructor(private apiService: ApiService) { }

  ngOnInit() {
    this.imageUrl = '';
  }

  onSubmit() {
    console.log(this.imageUrl);
    this.apiService.submitImage(this.imageUrl)
      .subscribe(response => console.log(response));
  }

}
