var selectedMedia=[];
var dummyEvents = [{ eventID: 1, eventName: 'Trip to Location A'},
{ eventID: 2, eventName: 'Annual Big Fundraiser' },
{ eventID: 3, eventName: 'Walkup on 6/17/17' },
{ eventID: 4, eventName: 'Unpublished Trip XYZ' },
];

$(document).ready(function () {
    populateDropDown();
    //$('.dropdown-content li').on('click', function (e) {
    //    routeSelected(e);
    //});
    //$('input').on('input', function (e) {
    //    checkWetherToEnableButtons(e.target);
    //});
    //$('#Event_Description').on('input', function (e) {
    //    checkWetherToEnableButtons(e.target);
    //})
}
);

function populateDropDown() {
    var dropdown = document.getElementById("routeSelection");
    for (var i = 0; i < dummyEvents.length; i++) {
        var listItem = document.createElement("li");
        //  listItem.className = "routeSelectionItem";
        listItem.textContent = dummyEvents[i].eventName;
        listItem.setAttribute("value", i)
        dropdown.appendChild(listItem);
    }
}
$('body').on('input','click', function(event){
	if(event.target.selected)
		selectedMedia.push(event.target.value);
	else{
		selectedMedia.splice(selectedMedia.indexOf(event.target.value,1));
	}
});

$('#PublishEvent_publish').on('click', function (event){
//Store selectedMedia in session storage
	
});

$('#PublishEvent_cancel').on('click', function(){
	$(':input[name="platform"]').prop('checked',false);
});