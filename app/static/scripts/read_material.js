// Init SpeechSynth API
const synth = window.speechSynthesis;

// DOM Elements
const textForm = document.querySelector('form');
const textInput = document.querySelector('#text-input');
const voiceSelect = document.querySelector('#voice-select');
const rate = document.querySelector('#rate');
const rateValue = document.querySelector('#rate-value');
const pitch = document.querySelector('#pitch');
const pitchValue = document.querySelector('#pitch-value');
const body = document.querySelector('body');
const media = document.querySelector('#media')

//Browser identifier
// Firefox 1.0+
var isFirefox = typeof InstallTrigger !== 'undefined';

// Chrome 1+
var isChrome = !!window.chrome && !!window.chrome.webstore;

// Init voices array
let voices = [];

const getVoices = () => {
  voices = synth.getVoices();

  // Loop through voices and create an option for each one
  voices.forEach(voice => {
    // Create option element
    const option = document.createElement('option');
    // Fill option with voice and language
    option.textContent = voice.name + '(' + voice.lang + ')';

    // Set needed option attributes
    option.setAttribute('data-lang', voice.lang);
    option.setAttribute('data-name', voice.name);
    // voiceSelect.appendChild(option);
  });
};

//Line 35, 36 causes voice list duplication
getVoices();
if (synth.onvoiceschanged !== undefined) {
  synth.onvoiceschanged = getVoices;
}

//Fix for duplication, run code depending on the browser
if (isFirefox) {
    getVoices();
}
if (isChrome) {
    if (synth.onvoiceschanged !== undefined) {
        synth.onvoiceschanged = getVoices;
    }
}

// Speak
const speak = () => {
  media.src="./img/stop.png"
  // Check if speaking
  if (synth.speaking) {
    console.log('Speech Canceled');
    synth.cancel();
    media.src="./img/play.png"
    return;
  }
  if (textInput.value !== '') {
    // Get speak text
    const speakText = new SpeechSynthesisUtterance(textInput.textContent);

    // Speak end
    speakText.onend = e => {
      console.log('Done speaking...');
    };

    // Speak error
    speakText.onerror = e => {
      console.error('Something went wrong');
    }; 

    // Selected voice
    // const selectedVoice = voiceSelect.selectedOptions[0].getAttribute(
    //   'data-name'
    // );

    // Loop through voices
    voices.forEach(voice => {
      if (voice.name == 'Microsoft Zira Desktop - English (United States)') {
        speakText.voice = voice;
      }
    });

    // Set pitch and rate
    // speakText.rate = rate.value;
    // speakText.pitch = pitch.value;
    // Speak
    synth.speak(speakText);
  }
};

// EVENT LISTENERS

// Text form submit
textForm.addEventListener('submit', e => {
  e.preventDefault();
  speak();
  textInput.blur();
});

// // Rate value change
// rate.addEventListener('change', e => (rateValue.textContent = rate.value));

// // Pitch value change
// pitch.addEventListener('change', e => (pitchValue.textContent = pitch.value));

// Voice select change
// voiceSelect.addEventListener('change', e => speak());
