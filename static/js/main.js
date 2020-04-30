
function sortTable(sort_on, sort_criteria) {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById("myTable");
  switching = true;
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[sort_on];
      y = rows[i + 1].getElementsByTagName("TD")[sort_on];
      // Check if the two rows should switch place:
      if(sort_on==1){
        if(sort_criteria == 'ascending'){
          if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        }
        else{
          if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        }
      }
      else{
        if(sort_criteria == 'ascending'){
          if (parseInt(x.innerHTML) < parseInt(y.innerHTML)) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        }
        else{
          if (parseInt(x.innerHTML) > parseInt(y.innerHTML)) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}

$(document).ready(function(){

  var table = document.getElementById("myTable");
  for (var i = 0, row; row = table.rows[i]; i++) {
    
    if(i==0)  
      continue;

    total = row.cells[2].innerHTML;
    if(total > 100000)
      $(row).css("background-color", "rgba(255, 0, 0, 0.5)")
    else if(total > 50000)
      $(row).addClass('table-danger')
    else if(total > 10000)
      $(row).addClass('table-warning')  
    else if(total > 5000)
      $(row).css("background-color", "rgba(255, 255, 0, 0.3)")
    else if(total > 1000)
      $(row).css("background-color", "rgba(255, 255, 0, 0.1)")
    else
      $(row).addClass('table-success')  
  }

  $('.fas').click(function () {
    // modalLoading.init(true);
    console.log("started")
    th = $(this).parent();
    id = $(th).parent().children().index($(th));
    sort = $(this).attr('class');

    if (sort.includes('fa-sort-up')){
      sortTable(id, 'descending');
    }
    else{
      sortTable(id, 'ascending')
    }
    
    // modalLoading.init(true);
    // console.log("ended"); 
  });

  $('.nav-link').click(function (){
    $('.active').removeClass('active');
    $(this).addClass('active');
    $("tr").show()

    continent = $(this).html();

    if (continent != 'World')
      $("tr[name!='"+continent+"']").hide();
      $("tr[name='head']").show()
  });
});