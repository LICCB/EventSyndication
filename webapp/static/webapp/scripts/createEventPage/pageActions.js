var enableButtonsPreReqs = { nameEntered: false, dateEntered: false, eventTypeEntered: false, locationEntered: false, descriptionEntered: false };
var enableButtons = { saveButton: false, publishButton: false };
var dummyRoutes = [{ routeID: 1, routeName: 'TripA', eventType: 'Overnight', description: 'This is a description of this general route', location: 'Starting point A' },
{ routeID: 2, routeName: 'Very long Event Name', eventType: 'walkup', description: 'This is a description of this general walkup route', location: 'Starting point B' },
{ routeID: 3, routeName: 'Off shelf route 5', eventType: 'Overnight', description: 'This is a description of this overnight route', location: 'Starting point F' },
{ routeID: 4, routeName: 'Annual Fundraiser', eventType: 'Fundraiser', description: 'This is a description of the annual fundraiser', location: 'At location X' }
];


function populateDropDown() {
    var dropdown = document.getElementById("routeSelection");
    for (var i = 0; i < dummyRoutes.length; i++) {
        var listItem = document.createElement("li");
        //  listItem.className = "routeSelectionItem";
        listItem.textContent = dummyRoutes[i].routeName;
        listItem.setAttribute("value", i)
        dropdown.appendChild(listItem);
    }
}

function routeSelected(e) {
    //Set the Current route to selected Route
    $('#currentRoute').text(e.target.textContent);
    $('#currentRoute').val(e.target.value);
    $('#EventLoc').val(dummyRoutes[e.target.value].location);
    $('#Event_Description').val(dummyRoutes[e.target.value].description);
    $('#EventType').val(dummyRoutes[e.target.value].eventType);
    //Set the fields to true since they have been populated
    enableButtonsPreReqs.eventTypeEntered = true;
    enableButtonsPreReqs.locationEntered = true;
    enableButtonsPreReqs.descriptionEntered = true;

    checkToEnableButtons();
}

function checkToEnableButtons() {
    var publishButton = true;
    var saveButton;
    $.each(enableButtonsPreReqs, function (index, value) {
        publishButton = publishButton && value;
        if (index == 'nameEntered') {
            saveButton = value;
        }
    });
    enableButtons.publishButton = publishButton;
    enableButtons.saveButton = saveButton;
    enableButtonsIfValid();
}

function checkWetherToEnableButtons(eventDOM) {
    switch (eventDOM.id) {
        case "EventName":
            if (eventDOM.value.length > 5)//minimum of 5 characters for the event name
                enableButtonsPreReqs.nameEntered = true;
            else
                enableButtonsPreReqs.nameEntered = false;
            break;
        case "EventDate":
            if (eventDOM.value != "")
                enableButtonsPreReqs.dateEntered = true;
            else
                enableButtonsPreReqs.dateEntered = false;
            break;
        case "EventType":
            if (eventDOM.value.length > 5)//minimum of 5 characters for the event name
                enableButtonsPreReqs.eventTypeEntered = true;
            else
                enableButtonsPreReqs.eventTypeEntered = false;
            break;
        case "EventLoc":
            if (eventDOM.value.length > 5)//minimum of 5 characters for the event name
                enableButtonsPreReqs.locationEntered = true;
            else
                enableButtonsPreReqs.locationEntered = false;
            break;
        case "Event_Description":
            if (eventDOM.value.length > 5)//minimum of 5 characters for the event name
                enableButtonsPreReqs.descriptionEntered = true;
            else
                enableButtonsPreReqs.descriptionEntered = false;
            break;
    }
    checkToEnableButtons();

}

function enableButtonsIfValid() {
    // console.log('Should be published: ' + enableButtons.publishButton + '.   Sohuld be saved:' + enableButtons.saveButton)
    $('#CreateEvent_publish').prop('disabled', !enableButtons.publishButton);

    $('#CreateEvent_save').prop('disabled', !enableButtons.saveButton);

}

$('#CreateEvent_clear').on('click', function (e) {
    //Clear input fields
    $(':input').val('');
    $('#Event_Description').val('');
    //clear the checks for the buttons
    $.each(enableButtonsPreReqs, function (index, value) {
        enableButtonsPreReqs[index] = false;
    });
    //disable buttons
    checkToEnableButtons();
});
