import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  public imageUrl: string;
  public jobDone: boolean;
  constructor(private apiService: ApiService) { }

  ngOnInit() {
    this.imageUrl = '';
    this.jobDone = true;
  }

  onSubmit() {
    this.jobDone = false;
    this.apiService.submitImage(this.imageUrl)
      .subscribe(response => this.jobDone = true);
  }

}
