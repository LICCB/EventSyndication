var selectedMedia=[];

$('#publishCheckAll').on('click',function (e){
	if(e.target.checked)
	$(':input[name="platform"]').prop('checked',true);
else
	$(':input[name="platform"]').prop('checked',false);
});

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
