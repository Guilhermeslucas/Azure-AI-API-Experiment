import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  public imageUrl: string;
  public statusMessage: string;
  constructor(private apiService: ApiService) { }

  ngOnInit() {
    this.imageUrl = '';
    this.statusMessage = '';
  }

  onSubmit() {
    this.statusMessage = 'Loading. Please wait';
    this.apiService.submitImage(this.imageUrl)
      .subscribe(response => this.submitText(response));
  }

  submitText(response: object) {
    const text = response['_body'];
    console.log(text);
    if (response['status'] !== 200) {
      this.statusMessage = 'We had a problem during the process. Please try again.';
      return;
    }
    this.statusMessage = '';
    const msg  = new SpeechSynthesisUtterance(text);
    msg.volume = 1; // 0 to 1
    msg.rate = 1.5; // 0.1 to 10
    msg.pitch = 1; // 0 to 2
    msg.lang = 'pt-BR';
    (<any>window).speechSynthesis.speak(msg);
  }

}
