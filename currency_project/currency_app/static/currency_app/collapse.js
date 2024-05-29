document.addEventListener('DOMContentLoaded', function() {
  var collapsibleTables = document.getElementsByClassName('collapsible-table');
  for (var i = 0; i < collapsibleTables.length; i++) {
    var table = collapsibleTables[i];
    var headerRow = table.rows[0];
    var headerCell = headerRow.cells[0];
    headerCell.addEventListener('click', function() {
      table.classList.toggle('collapsed');
    });
  }
});