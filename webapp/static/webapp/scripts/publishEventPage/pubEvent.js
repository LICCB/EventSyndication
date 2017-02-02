var selectedMedia=[];

$(document).ready(function(){
	
	
	
	
});

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