const white = [220, 255, 220];
const green = [0, 255, 0];
const dimrate = 25;

let textbox = document.getElementById("thanktext");
const text = textbox.innerHTML;  	// For debugging

// Create an array for each letter in the text.

let textarray = [];

for(i = 0; i < textbox.innerHTML.length; i++){
	textarray.push({letter: textbox.innerHTML.charAt(i), color: [220, 255, 220]});
}

let lightarray = [];

function drawtext(){

	let newHTMLstring = '';

	for(i = 0; i < textarray.length; i++){					// For dimming the letters. Ignores letters if they're black.

		if(textarray[i].color[0] == white[0]){ 				// is white
			textarray[i].color[0] = green[0];
			textarray[i].color[1] = green[1];
			textarray[i].color[2] = green[2];
		}
		else if(textarray[i].color[1] > 0){
			textarray[i].color[1] -= dimrate;

			if(textarray[i].color[1] < 0){
				textarray[i].color[1] = 0;
			}
		}
	}

	if(Math.floor(Math.random() * 8) == 0){
		lightarray.push(textarray.length);
	}

	for(i = lightarray.length; i >= 0; --i){				// Looping through every light.
		lightarray[i] -= 1;
		if(lightarray[i] >= 0){
			textarray[lightarray[i]].color[0] = white[0];
			textarray[lightarray[i]].color[1] = white[1];
			textarray[lightarray[i]].color[2] = white[2];
		}
		else{
			lightarray.splice(i, 1);
		}
	}

	for(i = 0; i < textarray.length; i++){					// Build the string to send to the html.
		newHTMLstring += '<span style="color: rgb(' + textarray[i].color[0].toString() + ', ' + textarray[i].color[1].toString() + ', ' + textarray[i].color[2].toString() + ')">' +
		textarray[i].letter + '</span>';
	}

	textbox.innerHTML = newHTMLstring;
}

setInterval(drawtext, 100);
