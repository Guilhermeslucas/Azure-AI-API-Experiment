import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { ApiService } from '../api.service';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  @ViewChild('video') public video: ElementRef;
  @ViewChild('canvas') public canvas: ElementRef;
  public captures: Array<any>;
  public imageUrl: string;
  public statusMessage: string;
  constructor(private apiService: ApiService) { }

  ngOnInit() {
    this.imageUrl = '';
    this.statusMessage = '';
    this.captures = [];
  }

  // tslint:disable-next-line:use-life-cycle-interface
  public ngAfterViewInit() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
            this.video.nativeElement.src = window.URL.createObjectURL(stream);
            this.video.nativeElement.play();
        });
    }
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

  public capture() {
    this.captures.push(this.canvas.nativeElement.toDataURL('image/png'));
    console.log(this.captures[0]);
}

}
