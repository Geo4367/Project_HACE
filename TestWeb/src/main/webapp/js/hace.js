function askHace() {
	
	
	
	var query_text = document.getElementById("haceInput").value;
	if (query_text) {
		$.ajax({
			type: "GET",
			url: "http://127.0.0.1:8000/ask_hace?q=" + query_text,


			success: function(msg) {
				

				openHacePopUp(msg);
				
				

			}
		});
	} else {

		const myNode = document.getElementById("haceResponse");
		while (myNode.lastElementChild) {
			myNode.removeChild(myNode.lastElementChild);
		}
	}


}




function Search() {
	
	
	
	var query_text = document.getElementById("myInput").value;
	if (query_text) {
		$.ajax({
			type: "GET",
			url: "http://127.0.0.1:8000/search?q=" + query_text,


			success: function(msg) {
				var response = document.getElementById("response");
				const obj = JSON.parse(msg);
				response.innerHTML = "";
				let table = document.createElement("table");
				table.style.padding = "10px";
				table.style.width = "100%";
				table.style.height = "200px";
				table.style.overflow = "scroll";
				table.style.background = "lightgrey";
				table.style.display = "block";

				obj.forEach((item) => {

					let tr = document.createElement("tr");
					tr.style.verticalAlign = "super";
					tr.style.width = "100%";

					let td1 = document.createElement("td");
					td1.innerText = item.filename;
					td1.style.width = "33%";
					tr.appendChild(td1);

					let a = document.createElement("a");
					a.innerText = "View PDF";
					a.href = item.view_url+"#page="+item.page;
					a.target = "_blank";
					a.style.width = "33%";
					tr.appendChild(a);

					let td3 = document.createElement("td");
					td3.innerText = "View Content";
					td3.style.cursor = "pointer";
					td3.style.fontWeight = "bold";
					td3.style.width = "33%";
					tr.addEventListener('click', function(event) {
						openPopUp(tr,item.text);
					});

					//tr.appendChild(td3);

					table.appendChild(tr);

					response.appendChild(table);
				})

			}
		});
	} else {

		const myNode = document.getElementById("response");
		while (myNode.lastElementChild) {
			myNode.removeChild(myNode.lastElementChild);
		}
	}


}

function openPopUp(tr,text) {
	var popup = document.getElementById("popup");
	popup.innerHTML = text;
	popup.classList.toggle("show");
	popup.style.display = "flex";
	tr.style.backgroundColor ="darkgray";
}

function openHacePopUp(text) {
	var popup = document.getElementById("hacePopup");
	popup.innerHTML = text;
	popup.classList.toggle("show");
	popup.style.display = "flex";
}


function switch_tab(evt, tab) {
	// Declare all variables
	var i, tabcontent, tablinks;

	// Get all elements with class="tabcontent" and hide them
	tabcontent = document.getElementsByClassName("tabcontent");
	for (i = 0; i < tabcontent.length; i++) {
		tabcontent[i].style.display = "none";
	}

	// Get all elements with class="tablinks" and remove the class "active"
	tablinks = document.getElementsByClassName("tablinks");
	for (i = 0; i < tablinks.length; i++) {
		tablinks[i].className = tablinks[i].className.replace(" active", "");
	}

	// Show the current tab, and add an "active" class to the button that opened the tab
	document.getElementById(tab).style.display = "block";
	evt.currentTarget.className += " active";
}