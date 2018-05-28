// autocomplete search field
$(function() {
    $("#q").autocomplete({
      source: "/api/get_categories/",
      select: function (event, ui) { //item selected
        AutoCompleteSelectHandler(event, ui)
      },
      minLength: 2,
    });
  });

function AutoCompleteSelectHandler(event, ui) {
  var selectedObj = ui.item;
}

// datepicker for start_date and end_date forms
$(function() {
  $( ".datepicker" ).datepicker({
    dateFormat: 'yy-mm-dd',
    changeMonth: true,
    changeYear: true,
    yearRange: "2018:2050",
  });
});