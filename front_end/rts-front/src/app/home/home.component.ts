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
      .subscribe(response => this.submitText(response['_body']));
  }

  submitText(text: string) {
    console.log(text);
    this.jobDone = true;
    const msg  = new SpeechSynthesisUtterance(text);
    msg.volume = 1; // 0 to 1
    msg.rate = 1.5; // 0.1 to 10
    msg.pitch = 1; // 0 to 2
    msg.lang = 'pt-BR';
    (<any>window).speechSynthesis.speak(msg);
  }

}
